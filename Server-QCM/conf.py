from os import path, environ
####====####
## SERVER ##
if environ.get('BIND_ADDRESS_QCM') is None:
    BIND_ADDRESS = '0.0.0.0'
else:
    BIND_ADDRESS = environ['BIND_ADDRESS_QCM']

if environ.get('BIND_PORT_QCM') is None:
    BIND_PORT = 5000
else:
    BIND_PORT = int(environ['BIND_PORT_QCM'])

## ADDRESS_SERVER_AUTHENTICATION
if environ.get('ADDRESS_SERVER_AUTHENTICATION') is None:
    ADDRESS_SERVER_AUTHENTICATION = 'localhost'
else:
    ADDRESS_SERVER_AUTHENTICATION = environ['ADDRESS_SERVER_AUTHENTICATION']

if environ.get('PORT_SERVER_AUTHENTICATION') is None:
    PORT_SERVER_AUTHENTICATION = '5001'
else:
    PORT_SERVER_AUTHENTICATION = environ['PORT_SERVER_AUTHENTICATION']

## ADDRESS_SERVER_CORRECTOR
if environ.get('ADDRESS_SERVER_CORRECTOR') is None:
    ADDRESS_SERVER_CORRECTOR = 'localhost'
else:
    ADDRESS_SERVER_CORRECTOR = environ['ADDRESS_SERVER_CORRECTOR']

if environ.get('PORT_SERVER_CORRECTOR') is None:
    PORT_SERVER_CORRECTOR = '5001'
else:
    PORT_SERVER_CORRECTOR = environ['PORT_SERVER_CORRECTOR']


####========####
## SECRET KEY ##
SECRET_KEY_APP = 'J84z0UH06f8gy*fg8vHg'
SECRET_SHARED_KEY = "jx5E4dx5fsSGb1fF12jqCn"

####=####
## URL ##
SERVER_AUTHENTICATION = 'http://' + ADDRESS_SERVER_AUTHENTICATION + ':' + PORT_SERVER_AUTHENTICATION + '/authentication'
SERVER_CORRECTOR = 'http://' + ADDRESS_SERVER_CORRECTOR + ':' + PORT_SERVER_CORRECTOR
SERVER_CORRECTOR_PUSH_QCM = SERVER_CORRECTOR + '/push_qcm'
SERVER_CORRECTOR_DELETE = SERVER_CORRECTOR + '/delete_qcm'


####======####
## PATH DIR ##
PATH_DIR = path.dirname(path.realpath(__file__)) + "/"
PATH_QCM = PATH_DIR + "xml/qcm/"
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
