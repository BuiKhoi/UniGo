class DUTConstants:
    URL_LANDING_PAGE = 'http://sv.dut.udn.vn/Default.aspx'
    URL_LOGIN_PAGE = 'http://sv.dut.udn.vn/PageDangNhap.aspx'
    URL_SCHEDULE_PAGE = 'http://sv.dut.udn.vn/PageLichTH.aspx'
    URL_SCHEDULE_PAGE_AJAX_SAMPLE = 'http://sv.dut.udn.vn/WebAjax/evLopHP_Load.aspx?E=TTKBLoad&Code={}'
    URL_COLAB_PAGE_AJAX_SAMPLE = 'http://sv.dut.udn.vn/WebAjax/evLopHP_Load.aspx?E=TTKBView&MaLop={}'
    URL_MAIN_STUDENT_INFO = 'http://sv.dut.udn.vn/PageCaNhan.aspx'
    URL_STUDY_RESULT = 'http://sv.dut.udn.vn/PageKQRL.aspx'
    URL_NOTIFICATION_BY_CLASS = 'http://sv.dut.udn.vn/WebAjax/evLopHP_Load.aspx?E=CTRTBGV&PAGETB=1&COL=TieuDe&NAME=&TAB=1'
    URL_CLASS_FRIEND_PAGE = 'http://sv.dut.udn.vn/PageLopSH.aspx'

    PAYLOAD_USERNAME_FIELD = '_ctl0:MainContent:DN_txtAcc'
    PAYLOAD_PASSWORD_FIELD = '_ctl0:MainContent:DN_txtPass'
    
    SAMPLE_LOGIN_PAYLOAD = {
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        '_ctl0:MainContent:DN_txtAcc': '',
        '_ctl0:MainContent:DN_txtPass': '',
        '_ctl0:MainContent:QLTH_btnLogin': 'Đăng nhập'
    }

    KEY_BINDINGS_SCHEDULE = {
        0: 'index',
        1: 'course_code',
        2: 'course_name',
        3: 'credit',
        5: 'teacher',
        6: 'weekly_schedule',
        7: 'study_weeks',
        10: 'class_code'
    }

    KEY_BINDINGS_TEST = {
        0: 'index',
        1: 'course_code',
        2: 'course_name',
        3: 'test_group',
        4: 'test_grouping',
        5: 'test_schedule'
    }

    KEY_BINDINGS_WEEKDAYS = {
        'Thứ 2': 1,
        'Thứ 3': 2,
        'Thứ 4': 3,
        'Thứ 5': 4,
        'Thứ 6': 5,
        'Thứ 7': 6,
        'CN': 0
    }

    KEY_BINDINGS_STUDY_RESULT = {
        0: 'index',
        1: 'semester',
        3: 'course_code',
        4: 'course_name',
        5: 'credit',
        6: 'point_formular',
        7: 'BT',
        8: 'BV',
        9: 'CC',
        10: 'CK',
        11: 'DA',
        12: 'GK',
        13: 'LT',
        14: 'TH',
        15: 'T10',
        16: 'T4',
        17: 'as_text'
    }

    KEY_BINDINGS_MORAL_RESULT = {
        0: 'semester',
        1: 'registered_credit',
        2: 'relearn_credit',
        3: 'avg_b4',
        4: 'avg_scholar',
        5: 'avg_b10',
        6: 'study_classify',
        7: 'moral_points',
        8: 'warnings',
        9: 'saved_credits',
        10: 'avg_saved_credit_b4',
        11: 'avg_moral'
    }

    KEY_BINDING_COLAB_INFO = {
        1: 'sutdent_id',
        2: 'student_name',
        3: 'class_name',
        4: 'phone'
    }

    KEY_BINDING_FRIEND_INFO = {
        1: 'sutdent_id',
        2: 'student_name',
        4: 'phone',
        5: 'mail',
        6: 'parent_phone'
    }
