import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'admin_panel_new'),
        'USER': os.environ.get('DB_USER', 'admin_panel'),
        'PASSWORD': os.environ.get('DB_PASSWORD',),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
           'options': '-c search_path=content,public'
        }
    }
}
