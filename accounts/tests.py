from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from cart.models import Order


class SubscriptionViewTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')

	def _login(self):
		self.client.login(username='tester', password='pass')

	def test_basic_under_15(self):
		Order.objects.create(user=self.user, total=14)
		self._login()
		resp = self.client.get(reverse('accounts.subscription'))
		self.assertContains(resp, 'Basic')

	def test_medium_between_15_and_30(self):
		Order.objects.create(user=self.user, total=15)
		Order.objects.create(user=self.user, total=10)
		self._login()
		resp = self.client.get(reverse('accounts.subscription'))
		self.assertContains(resp, 'Medium')

	def test_premium_over_30(self):
		Order.objects.create(user=self.user, total=31)
		self._login()
		resp = self.client.get(reverse('accounts.subscription'))
		self.assertContains(resp, 'Premium')

# Create your tests here.
