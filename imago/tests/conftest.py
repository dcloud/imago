from django.conf import settings
import dj_database_url

# DATABASE_TEST_URL should be point to a (read-only) db with valid ocd objects.
DATABASES_CONFIG = {
    'default': dj_database_url.config(env='DATABASE_TEST_URL')
}
DATABASES_CONFIG['default']['TEST'] = dj_database_url.config(env='DATABASE_TEST_URL')


def pytest_configure():
    print("Running using db host: '{}'".format(DATABASES_CONFIG['default']['TEST']['HOST']))
    settings.configure(
        SECRET_KEY='testit',
        DATABASES=DATABASES_CONFIG
    )
