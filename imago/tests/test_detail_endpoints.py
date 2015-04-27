from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
from restless.http import HttpError
import pytest
import django; django.setup()

from imago.views import (BillDetail, DivisionDetail, EventDetail, JurisdictionDetail, PersonDetail)


@pytest.mark.django_db
class BillDetailTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.ocd_id = 'ocd-bill/36ebab81-71b1-476f-9f4a-a565621968e4'

    def test_bill_object_retrievable(self):
        endpoint = BillDetail()
        path = '/{}/'.format(self.ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

    def test_bill_object_custom_fields(self):
        endpoint = BillDetail()
        path = '/{}/'.format(self.ocd_id)
        expected_fields = ('title', 'legislative_session', 'from_organization_id', 'classification')
        possible_fields = expected_fields + ('debug',)
        path = '{}?fields={}'.format(path, ','.join(expected_fields))
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        expected_field_msg = "Bill dict should only have keys '{}' (or 'debug')".format(','.join(possible_fields))
        for field in expected_fields:
            self.assertIn(field, content, "Bill dict should have key '{}'".format(field))
        for r_field in content.keys():
            self.assertIn(r_field, possible_fields, expected_field_msg)


@pytest.mark.django_db
class DivisionDetailTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.ocd_id = 'ocd-division/country:us/state:nc'

    def test_division_object_retrievable(self):
        endpoint = DivisionDetail()
        path = '/{}/'.format(self.ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

    def test_division_object_custom_fields(self):
        endpoint = DivisionDetail()
        path = '/{}/'.format(self.ocd_id)
        expected_fields = ('id', 'country', 'name')
        possible_fields = expected_fields + ('debug',)
        path = '{}?fields={}'.format(path, ','.join(expected_fields))
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        expected_field_msg = "Division dict should only have keys '{}' (or 'debug')".format(','.join(possible_fields))
        for field in expected_fields:
            self.assertIn(field, content, "Division dict should have key '{}'".format(field))
        for r_field in content.keys():
            self.assertIn(r_field, possible_fields, expected_field_msg)


@pytest.mark.django_db
class EventDetailTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.ocd_id = 'ocd-event/001e7b51-2ccc-4f60-a83e-9172ae127a39'

    def test_event_object_retrievable(self):
        endpoint = EventDetail()
        path = '/{}/'.format(self.ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

    def test_event_object_custom_fields(self):
        endpoint = EventDetail()
        path = '/{}/'.format(self.ocd_id)
        expected_fields = ('id', 'name', 'classification', 'start_time', 'timezone')
        possible_fields = expected_fields + ('debug',)
        path = '{}?fields={}'.format(path, ','.join(expected_fields))
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        expected_field_msg = "Event dict should only have keys '{}' (or 'debug')".format(','.join(possible_fields))
        for field in expected_fields:
            self.assertIn(field, content, "Event dict should have key '{}'".format(field))
        for r_field in content.keys():
            self.assertIn(r_field, possible_fields, expected_field_msg)


@pytest.mark.django_db
class JurisdictionDetailTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.ocd_id = 'ocd-jurisdiction/country:us/state:nc/government'

    def test_jurisdiction_object_retrievable(self):
        endpoint = JurisdictionDetail()
        path = '/{}/'.format(self.ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

    def test_jurisdiction_object_custom_fields(self):
        endpoint = JurisdictionDetail()
        path = '/{}/'.format(self.ocd_id)
        expected_fields = ('id', 'name', 'url', 'classification')
        possible_fields = expected_fields + ('debug',)
        path = '{}?fields={}'.format(path, ','.join(expected_fields))
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        expected_field_msg = "Jurisdiction dict should only have keys '{}' (or 'debug')".format(','.join(possible_fields))
        for field in expected_fields:
            self.assertIn(field, content, "Jurisdiction dict should have key '{}'".format(field))
        for r_field in content.keys():
            self.assertIn(r_field, possible_fields, expected_field_msg)


@pytest.mark.django_db
class PersonDetailTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()
        self.ocd_id = 'ocd-person/0006efa7-70bf-41a0-8b0b-4bf8f999e7c1'

    def test_person_object_retrievable(self):
        endpoint = PersonDetail()
        path = '/{}/'.format(self.ocd_id)
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

    def test_person_object_custom_fields(self):
        endpoint = PersonDetail()
        path = '/{}/'.format(self.ocd_id)
        expected_fields = ('id', 'name', 'image', 'gender')
        possible_fields = expected_fields + ('debug',)
        path = '{}?fields={}'.format(path, ','.join(expected_fields))
        request = self.factory.get(path)
        response = endpoint.get(request, self.ocd_id)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")
        expected_field_msg = "Person dict should only have keys '{}' (or 'debug')".format(','.join(possible_fields))
        for field in expected_fields:
            self.assertIn(field, content, "Person dict should have key '{}'".format(field))
        for r_field in content.keys():
            self.assertIn(r_field, possible_fields, expected_field_msg)
