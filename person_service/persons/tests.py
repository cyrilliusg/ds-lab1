import json
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from .models import Person


@override_settings(APPEND_SLASH=False)
class PersonApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("persons-list-create")

    def test_list_returns_empty_array_initially(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"].split(";")[0], "application/json")
        data = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(data, [])

    def test_create_returns_201_empty_body_and_location_header(self):
        payload = {"name": "Alice", "age": 30, "address": "Main St", "work": "Engineer"}
        resp = self.client.post(
            self.list_url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)

        # Пустое тело
        self.assertEqual(resp.content, b"")

        # В БД есть запись
        self.assertEqual(Person.objects.count(), 1)
        person = Person.objects.first()
        self.assertEqual(person.name, "Alice")
        self.assertEqual(person.age, 30)
        self.assertEqual(person.address, "Main St")
        self.assertEqual(person.work, "Engineer")

        expected_location = f"{self.list_url}/{person.id}"
        self.assertEqual(resp["Location"], expected_location)

    def test_get_detail_returns_404_when_not_found(self):
        detail_url = reverse("persons-detail", kwargs={"pk": 9999})
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, 404)

    def test_patch_updates_person_and_returns_response_schema(self):
        person = Person.objects.create(name="Bob", age=20, address="", work="")
        detail_url = reverse("persons-detail", kwargs={"pk": person.id})

        patch_payload = {"age": 21, "work": "Student"}
        resp = self.client.patch(
            detail_url,
            data=json.dumps(patch_payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"].split(";")[0], "application/json")

        data = json.loads(resp.content.decode("utf-8"))

        self.assertIn("id", data)
        self.assertEqual(data["id"], person.id)
        self.assertEqual(data["name"], "Bob")
        self.assertEqual(data["age"], 21)
        self.assertEqual(data["work"], "Student")

        person.refresh_from_db()
        self.assertEqual(person.age, 21)
        self.assertEqual(person.work, "Student")

    def test_delete_returns_204_and_then_404_on_get(self):
        person = Person.objects.create(name="Carol", age=None, address=None, work=None)
        detail_url = reverse("persons-detail", kwargs={"pk": person.id})

        resp_delete = self.client.delete(detail_url)
        self.assertEqual(resp_delete.status_code, 204)
        self.assertFalse(Person.objects.filter(pk=person.id).exists())

        resp_get = self.client.get(detail_url)
        self.assertEqual(resp_get.status_code, 404)
