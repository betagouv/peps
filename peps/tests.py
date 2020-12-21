import datetime
import pytz
from unittest import skip
from unittest.mock import patch
from freezegun import freeze_time
import django.core.mail as mail
from django.test import TestCase, Client
from .tasks import remind_recipients
from django.contrib.auth import get_user_model
from data.models import Farmer, Message

class TestTasks(TestCase):

    def setUp(self):
        _populate_database()

    @skip
    @patch('django.core.mail.send_mail')
    @freeze_time('2020-01-15')
    def test_remind_recipients(self, mocked_send_mail):
        """
        It's January 20th in this test. We should remind the following messages:
        - Philippe to Pierre
        - Philippe to Agnès

        We should NOT remind:
        - Philippe and Jean (A conversation has already taken place)
        - Philippe to Marie (Too soon)
        - Philippe to Sophie (Message has been seen)
        """
        remind_recipients()
        philippe = Farmer.objects.get(name="Philippe")
        pierre = Farmer.objects.get(name="Pierre")
        agnes = Farmer.objects.get(name="Agnès")
        marie = Farmer.objects.get(name="Marie")
        jean = Farmer.objects.get(name="Jean")
        sophie = Farmer.objects.get(name="Sophie")

        reminded_messages = [
            Message.objects.get(sender=philippe, recipient=pierre),
            Message.objects.get(sender=philippe, recipient=agnes),
        ]

        for message in Message.objects.all():
            if message in reminded_messages:
                self.assertTrue(message.notified)
            else:
                self.assertFalse(message.notified)

        # In total, two emails should have been sent
        mocked_send_mail.assert_called()
        self.assertEqual(mocked_send_mail.call_count, 2)

        # One to Pierre and one Agnes
        recipients = [
            mocked_send_mail.mock_calls[0][2].get('recipient_list')[0],
            mocked_send_mail.mock_calls[1][2].get('recipient_list')[0],
        ]
        self.assertTrue('Pierre@example.com' in recipients)
        self.assertTrue('Agnès@example.com' in recipients)

        # If we run the task again no new emails should be sent
        mocked_send_mail.reset_mock()
        remind_recipients()
        mocked_send_mail.assert_not_called()


def _populate_database():
    # Farmers
    for farmer_name in ('Philippe', 'Pierre', 'Agnès', 'Marie', 'Jean', 'Sophie'):
        email = farmer_name + "@example.com"
        get_user_model().objects.create_user(farmer_name, email=email, password="12345")
        farmer = Farmer(
            name=farmer_name,
            lat=45.1808,
            lon=1.893,
            email=email,
            approved=True,
            can_send_messages=True,
        )
        farmer.save()

    philippe = Farmer.objects.get(name="Philippe")
    pierre = Farmer.objects.get(name="Pierre")
    agnes = Farmer.objects.get(name="Agnès")
    marie = Farmer.objects.get(name="Marie")
    jean = Farmer.objects.get(name="Jean")
    sophie = Farmer.objects.get(name="Sophie")
    # -----------------------------------
    # Message sent from Philippe to Pierre on Jan 1, 2020
    Message(
        sender=philippe,
        recipient=pierre,
        subject="Hello Pierre",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 1, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
    # -----------------------------------
    # Message sent from Philippe to Agnès on Jan 1, 2020
    Message(
        sender=philippe,
        recipient=agnes,
        subject="Hello Agnès",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 1, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
    # -----------------------------------
    # Conversation between Philippe and Jean (1, 2 and 3 Jan, 2020)
    Message(
        sender=philippe,
        recipient=jean,
        subject="Hello Jean",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 1, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
    Message(
        sender=jean,
        recipient=philippe,
        subject="Hello Philippe",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 2, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
    Message(
        sender=philippe,
        recipient=jean,
        subject="Hello Jean",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 3, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
    # -----------------------------------
    # Message sent from Philippe to Marie on Jan 10, 2020
    Message(
        sender=philippe,
        recipient=marie,
        subject="Hello Marie",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 10, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
    # -----------------------------------
    # Message sent from Philippe to Sophie on Jan 1, 2020. Sophie sees it the next day.
    Message(
        sender=philippe,
        recipient=sophie,
        subject="Hello Sophie",
        body=":)",
        sent_at=datetime.datetime(2020, 1, 1, 1, tzinfo=pytz.timezone('Europe/Paris')),
        read_at=datetime.datetime(2020, 1, 2, 1, tzinfo=pytz.timezone('Europe/Paris')),
    ).save()
