from django.test import TestCase
from messaging.models import *
from messaging.services import MessageService
from django.contrib.auth.models import User

def generate_user(count=1):
    for i in range(1, count+1):
        User.objects.create_user(f'john{i}', f'lennon{i}@thebeatles.com', 'johnpassword')

def generate_messages(count):
    return [f'message-{i}' for i in range(count)]

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
        generate_user(4)
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        user3=User.objects.get(username='john3')

        MessageService.send_message(user1, user2, 'message1')
        MessageService.send_message(user1, user2, 'message2')
        MessageService.send_message(user2, user1, 'message3')
        MessageService.send_message(user1, user3, 'message4')


    def test_get_sent_messages(self):
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        messages=MessageService.get_sent_messages(user1, user2)

        assert len(messages)==2, f'wrong length: {len(messages)} | expected: 2'
        assert messages[0].content== 'message1', f'wrong content: {messages[0].content} | expected: message1'
        assert messages[1].content== 'message2', f'wrong content: {messages[1].content} | expected: message2'

        messages=MessageService.get_sent_messages(user2, user1)
        assert len(messages)==1, f'wrong length: {len(messages)} | expected: 1'
        assert messages[0].content== 'message3', f'wrong content: {messages[0].content} | expected: message3'

    def test_get_received_messages(self):
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        messages=MessageService.get_received_messages(user2, user1)
        assert len(messages)==2, f'wrong length: {len(messages)} | expected: 2'
        assert messages[0].content== 'message1', f'wrong content: {messages[0].content} | expected: message1'
        assert messages[1].content== 'message2', f'wrong content: {messages[1].content} | expected: message2'

        messages=MessageService.get_received_messages(user1, user2)
        assert len(messages)==1, f'wrong length: {len(messages)} | expected: 1'
        assert messages[0].content== 'message3', f'wrong content: {messages[0].content} | expected: message3'

    def test_get_conversations(self):
        user1=User.objects.get(username='john1')
        users = [user.username for user in MessageService.get_conversations(user1)]

        assert len(users)==2, f'wrong length: {len(users)} | expected: 2'
        assert 'john2' in users, f'john1 is missing'
        assert 'john3' in users, f'john2 is missing'

class BlacklistTestCase(TestCase):
    def setUp(self):
        generate_user(3)
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
    
        # only user1 blocks user2
        # every other message direction is possible
        MessageService.block_user(user1, user2)
    
    def test_is_user_blocked(self):
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        user3=User.objects.get(username='john3')

        res1=MessageService.is_user_blocked(user2, user1)
        res2=MessageService.is_user_blocked(user2, user3)
        assert res1==True
        assert res2==False
    
    def test_blacklist(self):
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
        user3=User.objects.get(username='john3')

        s,m = MessageService.send_message(user1, user3, 'naber')
        assert s==True, f'user1 should be able to send a message to user3'
        
        s,m = MessageService.send_message(user2, user3, 'naber')
        assert s==True, f'user2 should be able to send a message to user3'

        s,m = MessageService.send_message(user2, user1, 'naber')
        assert s==False, f'user1 should not be able to send a message to user2'

    def test_block_user(self):
        user1=User.objects.get(username='john1')
        user2=User.objects.get(username='john2')
    
        # only user1 blocks user2
        # every other message direction is possible
        res=MessageService.block_user(user1, user2)

        assert res is None, 'user blocked twice'