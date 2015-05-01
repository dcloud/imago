from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
from restless.http import HttpError
import pytest
import django; django.setup()

from imago.views import DivisionList


@pytest.mark.django_db
class DivisionEndpointTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.endpointpath = '/divisions/'

    def test_divisions_http200(self):
        endpoint = DivisionList()
        request = self.factory.get(self.endpointpath)
        response = endpoint.get(request)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")

    def test_divisions_defaults(self):
        endpoint = DivisionList()
        request = self.factory.get(self.endpointpath)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn("meta", content, "Content dictionary should contain a meta object")
        self.assertIn("results", content, "Content dictionary should contain a results object")
        if 'results' in content:
            results = content.get('results')
            self.assertIsInstance(results, list, "JSON results should be a list")
            expected_fields = ('id', 'name', 'country', 'jurisdictions', 'children', 'geometries')
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Dict should have key '{}'".format(field))

    def test_divisions_filter_by_date(self):
        endpoint = DivisionList()
        date_str = '2015-01-01'
        request = self.factory.get('{}?date={}'.format(self.endpointpath, date_str))
        response = endpoint.get(request)
        self.assertLess(response.status_code, 500,
                        msg="Endpoint should return a non-500 response for date lookup (but could be a 404)")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)

    def test_divisions_filter_by_lat_lon(self):
        endpoint = DivisionList()
        raleigh_point = ('35.780556', '-78.638889')
        request = self.factory.get('{}?lat={point[0]}&lon={point[1]}'.format(self.endpointpath, point=raleigh_point))
        response = endpoint.get(request)
        self.assertLess(response.status_code, 500,
                        msg="Endpoint should return a non-500 response for lat/lon lookup (but could be a 404)")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
