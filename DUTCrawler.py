from bs4 import BeautifulSoup
import json
import requests
import numpy as np

from constants import DUTConstants

constants = DUTConstants()

class DUTCrawler:
    def __init__(self, username, password):
        self.sess = requests.session()
        self.session_id = username

        self.username = username
        self.password = password
        if self.login():
            print('DUT Crawler initialized')
        else:
            print('DUT Crawler failed to initialized')
            self.session_id = None

        self.last_response = None

    def get_session_id(self):
        return self.session_id

    def sess_get(self, url, force_get=False):
        if force_get or not self.last_response:
            return self.sess.get(url)
        elif self.last_response and url != self.last_response.url:
            response = self.sess.get(url)
            self.last_response = last_response
            return response
        else:
            return self.last_response

    def login(self):
        response = self.sess.get(constants.URL_LOGIN_PAGE)
        payload = constants.SAMPLE_LOGIN_PAYLOAD

        soup = BeautifulSoup(response.text)
        view_states = soup.find_all('input', {'type': 'hidden'})
        for vs in view_states:
            payload[vs.get('name')] = vs.get('value')
        payload[constants.PAYLOAD_USERNAME_FIELD] = self.username
        payload[constants.PAYLOAD_PASSWORD_FIELD] = self.password

        response = self.sess.post(constants.URL_LOGIN_PAGE, payload)
        if response.url == constants.URL_MAIN_STUDENT_INFO:
            return True
        else:
            return False

    def parse_row_info(self, schedule_item, key_binding, post_process = None):
        tds = schedule_item.find_all('td')
        result = {}
        for idx, td in enumerate(tds):
            if idx in key_binding.keys():
                result[key_binding[idx]] = td.text
        if post_process:
            result = post_process(result, tds)
        return result

    def get_study_time(self, time_text):
        nums = time_text.split('-')
        start = int(nums[0])
        end = int(nums[-1])
        return np.arange(start, end+1)

    def refine_schedule(self, schedule_text):
        target_schedule = {
            'raw': schedule_text,
            'schedules': []
        }
        
        schedules = schedule_text.split(';')
        for schedule in schedules:
            schedule = schedule.split(',')
            if len(schedule) < 3:
                target_schedule['schedules'].append({
                    'weekday': -1,
                    'room': '',
                    'study_time': []
                })
            else:
                target_schedule['schedules'].append({
                    'weekday': constants.KEY_BINDINGS_WEEKDAYS[schedule[0].strip()],
                    'room': schedule[2],
                    'study_time': self.get_study_time(schedule[1]).tolist()
                })
        return target_schedule

    def get_schedule(self, semester_id = None):
        print('SEMID: ', semester_id)
        if semester_id is None:
            response = self.sess_get(constants.URL_SCHEDULE_PAGE)
        else:
            response = self.sess.post(constants.URL_SCHEDULE_PAGE_AJAX_SAMPLE.format(semester_id))
        soup = BeautifulSoup(response.text)
        schedule_table = soup.find('table', {
            'id': 'TTKB_GridInfo'
        })
        schedule_items = schedule_table.find_all('tr', {
            'class': 'GridRow'
        })[:-1]

        def post_process_schedule(result, tds):
            result['weekly_schedule'] = self.refine_schedule(result['weekly_schedule'])
            return result
        
        return [self.parse_row_info(si, constants.KEY_BINDINGS_SCHEDULE, post_process_schedule) for si in schedule_items]

    def get_tests(self, semester_id = None):
        if semester_id is None:
            response = self.sess_get(constants.URL_SCHEDULE_PAGE)
        else:
            response = self.sess.post(constants.URL_SCHEDULE_PAGE_AJAX_SAMPLE.format(semester_id))
        soup = BeautifulSoup(response.text)
        schedule_table = soup.find('table', {
            'id': 'TTKB_GridLT'
        })
        schedule_items = schedule_table.find_all('tr', {
            'class': 'GridRow'
        })[:-1]

        def post_process_tests(result, tds):
            result['test_grouping'] = 'GridCheck' in tds[4].get('class')
            return result
        
        return [self.parse_row_info(si, constants.KEY_BINDINGS_TEST, post_process_tests) for si in schedule_items]

    def parse_semester_option(self, option):
        return {
            'value': option.get('value'),
            'name': option.text
        }
        
    def get_semester_list(self):
        response = self.sess_get(constants.URL_SCHEDULE_PAGE)
        soup = BeautifulSoup(response.text)
        options = soup.find('select', {
            'id': 'TTKB_cboHocKy'
        }).find_all('option')[1:]
        return [self.parse_semester_option(o) for o in options]

    def get_study_result(self):
        response = self.sess_get(constants.URL_STUDY_RESULT)
        soup = BeautifulSoup(response.text)
        study_results = soup.find('table', {'id': 'KQRLGridKQHT'}).find_all('tr', {'class': 'GridRow'})

        return [self.parse_row_info(res, constants.KEY_BINDINGS_STUDY_RESULT) for res in study_results]

    def get_moral_result(self):
        response = self.sess_get(constants.URL_STUDY_RESULT)
        soup = BeautifulSoup(response.text)
        study_results = soup.find('table', {'id': 'KQRLGridTH'}).find_all('tr', {'class': 'GridRow'})

        return [self.parse_row_info(res, constants.KEY_BINDINGS_MORAL_RESULT) for res in study_results]

    def get_notifications(self, response):
        soup = BeautifulSoup(response.text,)
        noti_boxes = soup.find_all('div', {
            'class': 'tbBox'
        })

        notifications = []

        for nb in noti_boxes:
            notifications.append({
                'title': nb.find('div', {'class':'tbBoxCaption'}).text,
                'content': nb.find('div', {'class':'tbBoxContent'}).text
            })
        return notifications

    def get_personal_information(self):
        response = self.sess_get(constants.URL_MAIN_STUDENT_INFO)
        soup = BeautifulSoup(response.text)
        
        return {
            'student_name': soup.find('input', {'id': 'CN_txtHoTen'}).get('value'),
            'sutdent_id': soup.find('span', {'id': 'Main_lblHoTen'}).text.split('(')[-1].split(')')[0],
            'class_name': soup.find('input', {'id': 'CV_txtLop'}).get('value'),
            'personal_email': soup.find('input', {'id': 'CN_txtMail2'}).get('value'),
            'phone': soup.find('input', {'id': 'CN_txtPhone'}).get('value'),
            'birthday': soup.find('input', {'id': 'CN_txtNgaySinh'}).get('value'),
            'school_mail': soup.find('input', {'id': 'CN_txtMail1'}).get('value'),
            'medical_id': soup.find('input', {'id': 'CN_txtSoBHYT'}).get('value'),
            'medical_id_end': soup.find('input', {'id': 'CN_txtHanBHYT'}).get('value'),
            'personal_image': soup.find('img', {'class': 'imgCB'}).get('src')
        }

    def get_overall_notifications(self):
        response = self.sess_get(constants.URL_LANDING_PAGE)
        return self.get_notifications(response)

    def get_classes_notifications(self):
        response = self.sess.post(constants.URL_NOTIFICATION_BY_CLASS)
        return self.get_notifications(response)


if __name__ == '__main__':
    bot = DUTCrawler('102170077', 'Mrwy0561999')
    # print(bot.get_semester_list())
    # print(bot.get_tests('2010'))
    # print(bot.get_moral_result())
    print(bot.get_personal_information())