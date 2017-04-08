# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SITE_NAME = 'CORE'

TEST = 'production'

USER_LOG_PATH = '/var/log/user-log/user_log.log'

UPLOAD_FOLDER = basedir + '/tmp/'
ALLOWED_IMG_EXTENSIONS = ['png','jpg','jpeg','gif','PNG','JPG','JPEG','GIF']

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# email server


# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = ''  # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = ''  # enter your MS translator app secret here

# administrator list
ADMINS = ['noreply@coreplatform.org']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50

