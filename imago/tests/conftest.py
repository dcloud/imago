from django.conf import settings
import dj_database_url

# DATABASE_TEST_URL should be point to a (read-only) db with valid ocd objects.
DATABASES_CONFIG = {
    'default': dj_database_url.config(default='postgis://opencivicdata:test@10.42.2.101/opencivicdata')
}
DATABASES_CONFIG['default']['TEST'] = dj_database_url.config(env='DATABASE_TEST_URL')


def pytest_configure():
    settings.configure(
        SECRET_KEY='testit',
        DATABASES=DATABASES_CONFIG
    )
