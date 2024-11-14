from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import Profile, Event
from .signals import create_user_profile, save_user_profile 

class ProfileModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_save.disconnect(create_user_profile, sender=get_user_model())
        post_save.disconnect(save_user_profile, sender=get_user_model())

    @classmethod
    def tearDownClass(cls):
        post_save.connect(create_user_profile, sender=get_user_model())
        post_save.connect(save_user_profile, sender=get_user_model())
        super().tearDownClass()

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='JanTestowy', password='password')
        self.profile = Profile.objects.create(user=self.user, bio='Fan wspinaczki i podróży.')

    def test_profile_content(self):
        self.assertEqual(self.profile.user.username, 'JanTestowy')
        self.assertEqual(self.profile.bio, 'Fan wspinaczki i podróży.')


class EventModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='organizator', password='password')
        self.attendee = User.objects.create_user(username='uczestnik', password='password')
        self.event = Event.objects.create(
            name='Wejście na Rysy',
            description='Zapraszamy śmiałków chętnych na wejście na Rysy.',
            location='Tatry, Polska',
            date='2024-12-15 10:00:00',
            created_by=self.user
        )

    def test_event_creation(self):
        self.assertEqual(self.event.name, 'Wejście na Rysy')
        self.assertEqual(self.event.description, 'Zapraszamy śmiałków chętnych na wejście na Rysy.')
        self.assertEqual(self.event.location, 'Tatry, Polska')
        self.assertEqual(self.event.created_by.username, 'organizator')

    def test_event_attendees(self):
        # Dodanie uczestnika
        self.event.attendees.add(self.attendee)
        self.assertIn(self.attendee, self.event.attendees.all())
        # Usunięcie uczestnika
        self.event.attendees.remove(self.attendee)
        self.assertNotIn(self.attendee, self.event.attendees.all())
