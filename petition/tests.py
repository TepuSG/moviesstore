from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Petition


class PetitionViewTests(TestCase):
    def test_petition_index_loads(self):
        resp = self.client.get(reverse('petition.index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Petition')

    def test_create_petition_requires_login(self):
        resp = self.client.post(reverse('petition.create'), {'title': 'New Movie'})
        # should redirect to login
        self.assertEqual(resp.status_code, 302)

    def test_create_petition_success(self):
        user = User.objects.create_user(username='u1', password='p')
        self.client.login(username='u1', password='p')
        resp = self.client.post(reverse('petition.create'), {'title': 'New Movie'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Petition.objects.filter(title='New Movie', user=user).exists())

    def test_toggle_like(self):
        user = User.objects.create_user(username='u2', password='p')
        p = Petition.objects.create(title='Movie X', user=user)
        self.client.login(username='u2', password='p')
        resp = self.client.post(reverse('petition.toggle_like', kwargs={'id': p.id}), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        p.refresh_from_db()
        self.assertEqual(p.likes.count(), 1)
