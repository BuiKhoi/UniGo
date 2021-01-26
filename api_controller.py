from flask import Flask
from flask_restful import Resource, Api, reqparse
from DUTCrawler import DUTCrawler
import time
from threading import Thread

app = Flask(__name__)
api = Api(app)

bots = {}
BOT_TIMEOUT = 120
Thread(target=auto_clean_thread).start()

def millis():
    return int(time.time())

def auto_clean_thread():
    global bots
    print('Start auto cleaner')
    while True:
        mil = millis()
        bot_keys = list(bots.keys())
        for bot_key in bot_keys:
            if mil - bots[bot_key]['last_access'] > BOT_TIMEOUT:
                bots.pop(bot_key, None)
                print('Autoclean removed bot with session id: ', bot_key)
        time.sleep(BOT_TIMEOUT / 10)

class CrawlerHandler(Resource):
    pass

class DUTCrawlerHandler(CrawlerHandler):
    def post(self):
        global bots
        parser = reqparse.RequestParser()
        
        parser.add_argument('command', required=True)
        parser.add_argument('session_id')
        args = parser.parse_args()

        if args['command'] == 'register':
            parser.add_argument('username', required=True)
            parser.add_argument('password', required=True)
            args = parser.parse_args()
            
            handler = DUTCrawler(args['username'], args['password'])
            sess_id = handler.get_session_id()
            if sess_id:
                bots[sess_id] = {
                    'handler': handler,
                    'last_access': millis()
                }
                return {
                    'status': True,
                    'sess_id': sess_id
                }
            else:
                return {
                    'status': False
                }
            
        elif args['session_id']:
            command = args['command']
            if args['session_id'] in bots.keys():
                bots[args['session_id']]['last_access'] = millis()
                handler = bots[args['session_id']]['handler']
            else:
                return {
                    'status': False,
                    'message': 'Crawler ran out of time, please register again'
                }

            if command == 'get_overall_noti':
                return handler.get_overall_notifications()

            elif command == 'get_class_noti':
                return handler.get_classes_notifications()
                
            elif command == 'get_schedule':
                parser.add_argument('semester_id')
                args = parser.parse_args()
                return handler.get_schedule(args['semester_id'])

            elif command == 'get_tests':
                parser.add_argument('semester_id')
                args = parser.parse_args()
                return handler.get_tests(args['semester_id'])

            elif command == 'get_study_result':
                return handler.get_study_result()

            elif command == 'get_moral_result':
                return handler.get_moral_result()

            elif command == 'get_personal_information':
                return handler.get_personal_information()

            else:
                return {
                    'status': False,
                    'message': 'This command is not supported by our system, please check it again'
                }
            
        return {
            'status': False,
            'message': 'You have to register for a session id, or specify a session id of your own'
        }

    def get(self):
        return {
            'status': 'check ok'
        }

api.add_resource(DUTCrawlerHandler, '/dut/')

if __name__ == '__main__':
    print('Starting server')
    Thread(target=auto_clean_thread).start()
    app.run(debug=False, use_reloader=False)