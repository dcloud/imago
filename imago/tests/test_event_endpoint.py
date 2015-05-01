from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
from restless.http import HttpError
import pytest
import django; django.setup()

from imago.views import EventList


@pytest.mark.django_db
class EventEndpointTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.endpointpath = '/events/'

    def test_events_http200(self):
        endpoint = EventList()
        request = self.factory.get(self.endpointpath)
        response = endpoint.get(request)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")

    def test_events_defaults(self):
        endpoint = EventList()
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
            expected_fields = (
                'id',
                'name',
                'description',
                'classification',
                'start_time',
                'timezone',
                'end_time',
                'all_day',
                'status',
            )
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Dict should have key '{}'".format(field))

    def test_events_filter_by_jurisdiction_id(self):
        endpoint = EventList()
        ocd_id = 'ocd-jurisdiction/country:us/state:pa/government'
        path = '{}?jurisdiction_id={}'.format(self.endpointpath, ocd_id)
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

    def test_events_filter_by_participant_id(self):
        endpoint = EventList()
        ocd_id = 'ocd-organization/a29f9e71-0678-41d9-bfe9-f50299037158'
        path = '{}?participant_id={}'.format(self.endpointpath, ocd_id)
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

    def test_events_filter_by_related_bill(self):
        endpoint = EventList()
        ocd_id = 'ocd-bill/00001b02-94ac-4dc2-94f5-82f7e4cddc60'
        path = '{}?agenda__related_entities__bill_id={}'.format(self.endpointpath, ocd_id)
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

    def test_events_filter_by_related_organization(self):
        endpoint = EventList()
        ocd_id = 'ocd-organization/a29f9e71-0678-41d9-bfe9-f50299037158'
        path = '{}?agenda__related_entities__organization_id={}'.format(self.endpointpath, ocd_id)
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

    def test_events_filter_by_related_person(self):
        endpoint = EventList()
        ocd_id = 'ocd-person/000ecb6e-69a9-4761-bd50-8ad98a52624a'
        path = '{}?agenda__related_entities__person_id={}'.format(self.endpointpath, ocd_id)
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

    def test_events_filter_by_related_vote(self):
        endpoint = EventList()
        ocd_id = 'ocd-vote/1578dd40-d244-4edf-9bee-b640a9499dae'
        path = '{}?agenda__related_entities__vote_id={}'.format(self.endpointpath, ocd_id)
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

    def test_events_filter_by_when(self):
        endpoint = EventList()
        when = '2014-11-05'
        path = '{}?when={}'.format(self.endpointpath, when)
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

    def test_events_filter_by_updated_at(self):
        endpoint = EventList()
        when = '2014-04-13'
        path = '{}?updated_at={}'.format(self.endpointpath, when)
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

    def test_events_filter_by_created_at(self):
        endpoint = EventList()
        when = '2014-04-13'
        path = '{}?created_at={}'.format(self.endpointpath, when)
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


