from django.test import TestCase
from messaging.models import *
from messaging.services import MessageService
from django.contrib.auth.models import User

class MessageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('john1', 'lennon1@thebeatles.com', 'johnpassword')
        User.objects.create_user('john2', 'lennon2@thebeatles.com', 'johnpassword')

    def test_send_message(self):
        """Animals that can speak are correctly identified"""
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        s1,m1=MessageService.send_message(user1, user2, 'naber')
        s2,m2=MessageService.send_message(user2, user1, 'iyi')
        
        assert m1.content=='naber', 'mesaj yanlış gitti'
        assert m1.to_user.username==user2.username, 'mesaj yanlış kişiye gitti'
        assert m1.from_user.username==user1.username, 'mesaj yanlış kişiden gitti'

        assert m2.content=='iyi', 'mesaj yanlış gitti'
        assert m2.to_user.username==user1.username, 'mesaj yanlış kişiye gitti'
        assert m2.from_user.username==user2.username, 'mesaj yanlış kişiden gitti'

class MessageTestCase2(TestCase):
    def setUp(self):
        user1=User.objects.create_user('john1', 'lennon1@thebeatles.com', 'johnpassword')
        user2=User.objects.create_user('john2', 'lennon2@thebeatles.com', 'johnpassword')
        MessageService.send_message(user1, user2, 'naber')
        MessageService.send_message(user1, user2, 'naber2')
        MessageService.send_message(user2, user1, 'iyi')


    def test_get_sent_messages(self):
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        messages=MessageService.get_sent_messages(user2, user1)
        print(messages)
        assert len(messages)==2, f'wrong length: {len(messages)} | expected: 2'
        assert messages[0].content== 'naber', f'wrong content: {messages[0].content} | expected: naber'
        assert messages[1].content== 'naber2', f'wrong content: {messages[1].content} | expected: naber2'

