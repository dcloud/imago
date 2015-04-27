from django.test import RequestFactory


class ApiRequestFactory(RequestFactory):
    """Need to patch request objects since DjangoRestless patches them as well"""

    def get(self, path, data=None, secure=False, **extra):
        request = super(ApiRequestFactory, self).get(path, data, secure, **extra)
        request.params = request.GET.copy()
        request.data = None
        request.raw_data = request.body
        return request
