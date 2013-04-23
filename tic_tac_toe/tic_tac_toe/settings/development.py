DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tic_tac_toe',
        'USER': 'tic_tac_toe',
        'PASSWORD': 'tic_tac_toe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}