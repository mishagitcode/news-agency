from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from app.models import Newspaper, Topic


class AppTestCase(TestCase):
    password = "StrongPass123!"

    def create_user(self, username, permissions=(), **kwargs):
        user = get_user_model().objects.create_user(
            username=username,
            password=self.password,
            **kwargs,
        )
        if permissions:
            user.user_permissions.set(
                Permission.objects.filter(codename__in=permissions)
            )
        return user

    def login_user(self, user):
        self.client.login(username=user.username, password=self.password)

    @staticmethod
    def create_topic(name):
        return Topic.objects.create(name=name)

    @staticmethod
    def create_newspaper(
        *,
        title,
        content,
        published_date,
        topic,
        publishers=(),
    ):
        newspaper = Newspaper.objects.create(
            title=title,
            content=content,
            published_date=published_date,
            topic=topic,
        )
        if publishers:
            newspaper.publishers.set(publishers)
        return newspaper

    @staticmethod
    def sample_date(day):
        return date(2026, 3, day)
