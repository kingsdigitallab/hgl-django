DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.fb.backends.mysql",
        "NAME": "django_irt_geo",
        "USER": "app_irt_data_rw",
        "PASSWORD": "u6$5HKy7EytjuHGy",
        "HOST": "db-data.inslib.cch.kcl.ac.uk",
        "PORT": "",
    },
}

INTERNAL_IPS = ("0.0.0.0", "127.0.0.1", "::1")

SECRET_KEY = "12345"

FABRIC_USER = "njakeman"

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
