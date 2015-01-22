from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings


def check_network_connection():
    try:
        requests.get('https://djangoproject.com')
    except requests.exceptions.ConnectionError:
        return False
    return True


has_network_connection = check_network_connection()


@override_settings(AKISMET_TESTING=True)
class ContactFormTests(TestCase):
    def test_foundation_contact(self):
        data = {
            'name': 'A. Random Hacker',
            'email': 'a.random@example.com',
            'message_subject': 'Hello',
            'body': 'Hello, World!'
        }
        resp = self.client.post('/contact/foundation/', data)
        self.assertRedirects(resp, '/contact/sent/')
        self.assertEqual(mail.outbox[-1].subject, '[Contact form] Hello')
