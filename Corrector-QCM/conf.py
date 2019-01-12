####====####
## SERVER ##
BIND_ADDRESS = '0.0.0.0'
BIND_PORT = 5002

####========####
## SECRET KEY ##
SECRET_KEY_APP = 'J84z0UH06f8gy*fg8vHg'
SECRET_SHARED_KEY = "jx5E4dx5fsSGb1fF12jqCn"

####======####
## PATH DIR ##
PATH_QCM = "./xml/qcm/"
PATH_QCM_CORRECTION = "./xml/correction/"

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
