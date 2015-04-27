from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
import pytest
import django; django.setup()

from imago.views import BillList


class BillSearchTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()

    @pytest.mark.django_db
    def test_bills_http200(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        response = endpoint.get(request)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")

    @pytest.mark.django_db
    def test_bills_defaults(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
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
            expected_fields = ('id', 'identifier', 'title', 'classification', 'subject')
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Bill dict should have key '{}'".format(field))

    @pytest.mark.django_db
    def test_bills_custom_fields(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?fields=title,legislative_session,from_organization_id,classification')
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
            expected_fields = ('title', 'legislative_session', 'from_organization_id', 'classification')
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Bill dict should have key '{}'".format(field))

    @pytest.mark.django_db
    def test_bills_search(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?q=Wisconsin')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")

    @pytest.mark.django_db
    def test_bills_sponsorships(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?sponsorships__person__id=ocd-person/8f8aacb2-0ff7-41b9-9c69-91db22cfa818')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
