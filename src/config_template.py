import os

config = {
    # Авторизационные данные для Firebase по login\password
    'authorFirebase': {
        'email': '',
        'password': '',
    },
    # Авторизационный сертификат для Firebase
    'serviceAccount': {
        'type': '',
        'project_id': '',
        'private_key_id': '',
        'private_key': '',
        'client_email': '',
        'client_id': '',
        'auth_uri': '',
        'token_uri': '',
        'auth_provider_x509_cert_url': '',
        'client_x509_cert_url': '',
        'universe_domain': ''
    },
    # Настройка БД в Firebase
    'firebase': {
        'apiKey': '',
        'authDomain': '',
        'projectId': '',
        'storageBucket': '',
        'messagingSenderId': '',
        'appId': '',
        'databaseURL': '',
    },
    # Токен чат бота из telegram
    'botToken': '',
    'storagePath': f'{os.path.dirname(os.path.realpath(__file__))}/files/',
}
