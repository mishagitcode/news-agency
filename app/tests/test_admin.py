from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from app.admin import NewspaperAdmin, RedactorAdmin, TopicAdmin
from app.models import Newspaper, Redactor, Topic


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.topic_admin = TopicAdmin(Topic, self.site)
        self.redactor_admin = RedactorAdmin(Redactor, self.site)
        self.newspaper_admin = NewspaperAdmin(Newspaper, self.site)

        self.topic = Topic.objects.create(name="Politics")
        self.redactor = Redactor.objects.create_user(
            username="editor",
            password="StrongPass123!",
        )
        self.newspaper = Newspaper.objects.create(
            title="Daily Bulletin",
            content="Lead story",
            published_date="2026-03-10",
            topic=self.topic,
        )
        self.newspaper.publishers.add(self.redactor)

    def test_models_are_registered_in_admin(self):
        self.assertIsInstance(admin.site._registry[Topic], TopicAdmin)
        self.assertIsInstance(admin.site._registry[Redactor], RedactorAdmin)
        self.assertIsInstance(admin.site._registry[Newspaper], NewspaperAdmin)

    def test_topic_admin_configuration(self):
        self.assertEqual(self.topic_admin.list_display, ("id", "name"))
        self.assertEqual(self.topic_admin.search_fields, ("name",))
        self.assertEqual(self.topic_admin.ordering, ("name",))
        self.assertEqual(self.topic_admin.list_per_page, 25)

    def test_redactor_admin_published_newspapers_returns_placeholder_when_empty(self):
        other_redactor = Redactor.objects.create_user(
            username="author",
            password="StrongPass123!",
        )

        self.assertEqual(
            self.redactor_admin.published_newspapers(other_redactor),
            "-",
        )

    def test_redactor_admin_published_newspapers_returns_links(self):
        html = self.redactor_admin.published_newspapers(self.redactor)

        self.assertIn(
            f'/admin/app/newspaper/{self.newspaper.id}/change/',
            html,
        )
        self.assertIn(self.newspaper.title, html)
        self.assertIn("published_newspapers", self.redactor_admin.readonly_fields)

    def test_newspaper_admin_publishers_count_returns_related_total(self):
        self.assertEqual(self.newspaper_admin.publishers_count(self.newspaper), 1)
