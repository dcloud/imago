from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
from restless.http import HttpError
import pytest
import django; django.setup()

from imago.views import PeopleList


@pytest.mark.django_db
class PersonEndpointTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.endpointpath = '/people/'

    def test_events_http200(self):
        endpoint = PeopleList()
        request = self.factory.get(self.endpointpath)
        response = endpoint.get(request)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")

    def test_events_defaults(self):
        endpoint = PeopleList()
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
            expected_fields = ('name', 'id', 'sort_name', 'image', 'gender', 'memberships')
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Dict should have key '{}'".format(field))

    def test_people_filter_by_name(self):
        endpoint = PeopleList()
        name = 'stephen r. archambault'
        path = '{}?name={}'.format(self.endpointpath, name.lower())
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])
        self.assertEqual(len(content['results']), content['meta']['count'])

    def test_people_filter_by_gender(self):
        endpoint = PeopleList()
        name = 'female'
        path = '{}?gender={}'.format(self.endpointpath, name)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_birth_date(self):
        endpoint = PeopleList()
        birth_date = '1978-12-19'
        path = '{}?birth_date={}'.format(self.endpointpath, birth_date)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_death_date(self):
        endpoint = PeopleList()
        death_date = '1865-04-15'
        path = '{}?death_date={}'.format(self.endpointpath, death_date)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_created_at(self):
        endpoint = PeopleList()
        date = '2015-04-29'
        path = '{}?created_at={}'.format(self.endpointpath, date)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_updated_at(self):
        endpoint = PeopleList()
        date = '2015-04-29'
        path = '{}?updated_at={}'.format(self.endpointpath, date)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_member_of(self):
        endpoint = PeopleList()
        ocd_id = 'ocd-organization/50b0bdf1-6c55-4986-a54d-014938db8046'
        path = '{}?member_of={}'.format(self.endpointpath, ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_ever_member_of(self):
        endpoint = PeopleList()
        ocd_id = 'ocd-organization/50b0bdf1-6c55-4986-a54d-014938db8046'
        path = '{}?ever_member_of={}'.format(self.endpointpath, ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn('results', content)
        self.assertIn('meta', content)
        self.assertIn('count', content['meta'])

    def test_people_filter_by_lat_lon(self):
        endpoint = PeopleList()
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
