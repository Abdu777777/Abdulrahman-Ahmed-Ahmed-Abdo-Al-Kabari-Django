import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import RoundRecord

class AnalyzerApiTests(TestCase):
    def test_home_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CB Analyzer")

    def test_register_rejects_non_object_json(self):
        response = self.client.post(reverse("register"), data=json.dumps(["bad"]), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_login_and_round_persistence(self):
        response = self.client.post(reverse("register"), data=json.dumps({"username":"tester01","password":"StrongPass123!"}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="tester01").exists())
        predictions = [0] * 50
        predictions[0] = 1
        response = self.client.post(reverse("rounds"), data=json.dumps({"session_name":"test round","row_number":1,"predictions":predictions,"actuals":[0]*50}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RoundRecord.objects.filter(user__username="tester01").count(), 1)
        response = self.client.get(reverse("rounds"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["rounds"]), 1)

    def test_round_api_requires_authentication(self):
        response = self.client.get(reverse("rounds"))
        self.assertEqual(response.status_code, 302)

    def test_rejects_boolean_cell_values(self):
        self.client.force_login(User.objects.create_user(username="tester02", password="StrongPass123!"))
        predictions = [0] * 50
        predictions[0] = True
        response = self.client.post(reverse("rounds"), data=json.dumps({"predictions":predictions,"actuals":[0]*50}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
