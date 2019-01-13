from os import path, environ
####====####
## SERVER ##
if environ.get('BIND_ADDRESS_CORRECTOR') is None:
    BIND_ADDRESS = '0.0.0.0'
else:
    BIND_ADDRESS = environ['BIND_ADDRESS_CORRECTOR']

if environ.get('BIND_PORT_CORRECTOR') is None:
    BIND_PORT = 5002
else:
    BIND_PORT = int(environ['BIND_PORT_CORRECTOR'])


if environ.get('PORT_SERVER_QCM') is None:
    PORT_SERVER_QCM = 5000
else:
    PORT_SERVER_QCM = environ['PORT_SERVER_QCM']


if environ.get('NGINX_USE') is None:
    if environ.get('ADDRESS_SERVER_QCM') is None:
        ADDRESS_SERVER_QCM = 'localhost'
        URL_SERVER_QCM = 'http://localhost:' + str(PORT_SERVER_QCM)
    else:
        ADDRESS_SERVER_QCM = environ['ADDRESS_SERVER_QCM']
        URL_SERVER_QCM = 'http://' + environ['ADDRESS_SERVER_QCM'] + ':' + str(PORT_SERVER_QCM)
else:
    ADDRESS_SERVER_QCM = 'localhost'
    URL_SERVER_QCM = '/corrector'


####========####
## SECRET KEY ##
SECRET_KEY_APP = 'J84z0UH06f8gy*fg8vHg'
SECRET_SHARED_KEY = "jx5E4dx5fsSGb1fF12jqCn"

####======####
## PATH DIR ##
PATH_DIR = path.dirname(path.realpath(__file__)) + "/"
PATH_QCM_CORRECTION = PATH_DIR + "xml/correction/"

####====####
## REGEXP ##
## Création de QCM
REGEXP_NAME_QCM = r'[A-Za-z0-9-]+'
REGEXP_NAME_FORMATION = r'[A-Z]+'
REGEXP_NAME_MATIERE = r'[A-Z0-9]+'
REGEXP_NUMBER_QUESTION = r'[1-9][0-9]?'
REGEXP_NUMBER_ANSWER = r'[1-9]{1}'

## Validation du QCM
REGEXP_INPUT_QUESTION = r'[A-Za-z0-9 ?_-]+'
REGEXP_INPUT_ANSWER = r'[A-Za-z0-9 _?]+'

## delete, faire, correction QCM
REGEXP_REF_QCM = REGEXP_NAME_QCM
