from django.urls import reverse

from app.models import Newspaper, Redactor, Topic
from app.tests.base import AppTestCase


class TopicViewPermissionTests(AppTestCase):
    def setUp(self):
        self.topic = self.create_topic("Politics")
        self.viewer = self.create_user("viewer")
        self.editor = self.create_user(
            "editor",
            permissions=["add_topic", "change_topic", "delete_topic"],
        )

    def test_anonymous_user_is_redirected_from_topic_create(self):
        response = self.client.get(reverse("app:topic-create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_user_without_permission_cannot_create_topic(self):
        self.login_user(self.viewer)

        response = self.client.post(reverse("app:topic-create"), {"name": "Business"})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Topic.objects.filter(name="Business").exists())

    def test_editor_can_create_topic(self):
        self.login_user(self.editor)

        response = self.client.post(reverse("app:topic-create"), {"name": "Business"})

        self.assertRedirects(response, reverse("app:topic-list"))
        self.assertTrue(Topic.objects.filter(name="Business").exists())

    def test_user_without_permission_cannot_update_topic(self):
        self.login_user(self.viewer)

        response = self.client.post(
            reverse("app:topic-update", args=[self.topic.id]),
            {"name": "World"},
        )

        self.assertEqual(response.status_code, 403)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Politics")

    def test_editor_can_update_topic(self):
        self.login_user(self.editor)

        response = self.client.post(
            reverse("app:topic-update", args=[self.topic.id]),
            {"name": "World"},
        )

        self.assertRedirects(response, reverse("app:topic-list"))
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "World")

    def test_user_without_permission_cannot_delete_topic(self):
        self.login_user(self.viewer)

        response = self.client.post(reverse("app:topic-delete", args=[self.topic.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Topic.objects.filter(id=self.topic.id).exists())

    def test_editor_can_delete_topic(self):
        self.login_user(self.editor)

        response = self.client.post(reverse("app:topic-delete", args=[self.topic.id]))

        self.assertRedirects(response, reverse("app:topic-list"))
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())


class NewspaperViewPermissionTests(AppTestCase):
    def setUp(self):
        self.topic = self.create_topic("Politics")
        self.extra_topic = self.create_topic("Business")
        self.viewer = self.create_user("viewer")
        self.editor = self.create_user(
            "editor",
            permissions=["add_newspaper", "change_newspaper", "delete_newspaper"],
        )
        self.publisher = self.create_user("publisher")
        self.newspaper = self.create_newspaper(
            title="Daily News",
            content="Initial content",
            published_date=self.sample_date(10),
            topic=self.topic,
            publishers=[self.publisher],
        )

    def test_anonymous_user_is_redirected_from_newspaper_create(self):
        response = self.client.get(reverse("app:newspaper-create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_user_without_permission_cannot_create_newspaper(self):
        self.login_user(self.viewer)

        response = self.client.post(
            reverse("app:newspaper-create"),
            {
                "title": "Business Weekly",
                "content": "Business content",
                "published_date": self.sample_date(11),
                "topic": self.topic.id,
                "publishers": [self.publisher.id],
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Newspaper.objects.filter(title="Business Weekly").exists())

    def test_editor_can_create_newspaper(self):
        self.login_user(self.editor)

        response = self.client.post(
            reverse("app:newspaper-create"),
            {
                "title": "Business Weekly",
                "content": "Business content",
                "published_date": self.sample_date(11),
                "topic": self.extra_topic.id,
                "publishers": [self.editor.id, self.publisher.id],
            },
        )

        self.assertRedirects(response, reverse("app:newspaper-list"))
        newspaper = Newspaper.objects.get(title="Business Weekly")
        self.assertEqual(newspaper.topic, self.extra_topic)
        self.assertCountEqual(
            newspaper.publishers.values_list("id", flat=True),
            [self.editor.id, self.publisher.id],
        )

    def test_user_without_permission_cannot_update_newspaper(self):
        self.login_user(self.viewer)

        response = self.client.post(
            reverse("app:newspaper-update", args=[self.newspaper.id]),
            {
                "title": "Updated Daily News",
                "content": "Updated content",
                "published_date": self.sample_date(11),
                "topic": self.extra_topic.id,
                "publishers": [self.editor.id],
            },
        )

        self.assertEqual(response.status_code, 403)
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Daily News")
        self.assertEqual(self.newspaper.topic, self.topic)

    def test_editor_can_update_newspaper(self):
        self.login_user(self.editor)

        response = self.client.post(
            reverse("app:newspaper-update", args=[self.newspaper.id]),
            {
                "title": "Updated Daily News",
                "content": "Updated content",
                "published_date": self.sample_date(11),
                "topic": self.extra_topic.id,
                "publishers": [self.editor.id],
            },
        )

        self.assertRedirects(response, reverse("app:newspaper-list"))
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Daily News")
        self.assertEqual(self.newspaper.topic, self.extra_topic)
        self.assertCountEqual(
            self.newspaper.publishers.values_list("id", flat=True),
            [self.editor.id],
        )

    def test_user_without_permission_cannot_delete_newspaper(self):
        self.login_user(self.viewer)

        response = self.client.post(
            reverse("app:newspaper-delete", args=[self.newspaper.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Newspaper.objects.filter(id=self.newspaper.id).exists())

    def test_editor_can_delete_newspaper(self):
        self.login_user(self.editor)

        response = self.client.post(
            reverse("app:newspaper-delete", args=[self.newspaper.id])
        )

        self.assertRedirects(response, reverse("app:newspaper-list"))
        self.assertFalse(Newspaper.objects.filter(id=self.newspaper.id).exists())


class RedactorViewPermissionTests(AppTestCase):
    def setUp(self):
        self.owner = self.create_user(
            "owner",
            permissions=["change_redactor", "delete_redactor"],
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            years_of_experience=5,
        )
        self.other_editor = self.create_user(
            "other-editor",
            permissions=["change_redactor", "delete_redactor"],
        )
        self.viewer = self.create_user("viewer")

    def test_anonymous_user_is_redirected_from_redactor_update(self):
        response = self.client.get(
            reverse("app:redactor-update", args=[self.owner.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_redactor_without_permission_cannot_update_own_profile(self):
        self.login_user(self.viewer)

        response = self.client.post(
            reverse("app:redactor-update", args=[self.viewer.id]),
            {
                "username": self.viewer.username,
                "first_name": "Viewer",
                "last_name": "User",
                "email": "",
                "years_of_experience": 1,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_other_redactor_cannot_update_profile_even_with_permission(self):
        self.login_user(self.other_editor)

        response = self.client.post(
            reverse("app:redactor-update", args=[self.owner.id]),
            {
                "username": "owner",
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
                "years_of_experience": 7,
            },
        )

        self.assertEqual(response.status_code, 403)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.first_name, "Jane")

    def test_redactor_can_update_own_profile(self):
        self.login_user(self.owner)

        response = self.client.post(
            reverse("app:redactor-update", args=[self.owner.id]),
            {
                "username": "owner",
                "first_name": "Janet",
                "last_name": "Doe",
                "email": "janet@example.com",
                "years_of_experience": 6,
            },
        )

        self.assertRedirects(
            response,
            reverse("app:redactor-detail", args=[self.owner.id]),
        )
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.first_name, "Janet")
        self.assertEqual(self.owner.years_of_experience, 6)

    def test_other_redactor_cannot_delete_profile_even_with_permission(self):
        self.login_user(self.other_editor)

        response = self.client.post(
            reverse("app:redactor-delete", args=[self.owner.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Redactor.objects.filter(id=self.owner.id).exists())

    def test_redactor_can_delete_own_profile(self):
        self.login_user(self.owner)

        response = self.client.post(
            reverse("app:redactor-delete", args=[self.owner.id])
        )

        self.assertRedirects(response, reverse("app:index"))
        self.assertFalse(Redactor.objects.filter(id=self.owner.id).exists())
