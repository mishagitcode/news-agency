from django.urls import reverse

from app.models import Redactor
from app.tests.base import AppTestCase


class PublicViewTests(AppTestCase):
    def setUp(self):
        self.topic_business = self.create_topic("Business")
        self.topic_politics = self.create_topic("Politics")
        self.owner = self.create_user(
            "owner",
            permissions=["change_redactor", "delete_redactor"],
            first_name="Ann",
            last_name="Lee",
            email="ann@example.com",
            years_of_experience=5,
        )
        self.publisher = self.create_user("publisher", years_of_experience=2)
        self.alpha = self.create_user("alpha", years_of_experience=1)
        self.newspaper_old = self.create_newspaper(
            title="Morning Brief",
            content="Older story",
            published_date=self.sample_date(10),
            topic=self.topic_politics,
            publishers=[self.publisher],
        )
        self.newspaper_new = self.create_newspaper(
            title="Evening Brief",
            content="Newer story",
            published_date=self.sample_date(11),
            topic=self.topic_business,
            publishers=[self.owner, self.publisher],
        )

    def test_index_view_displays_dashboard_counts(self):
        response = self.client.get(reverse("app:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_topics"], 2)
        self.assertEqual(response.context["num_newspapers"], 2)
        self.assertEqual(response.context["num_redactors"], 3)

    def test_topic_list_shows_topics_in_name_order_with_newspaper_counts(self):
        self.create_newspaper(
            title="Politics Extra",
            content="Another story",
            published_date=self.sample_date(12),
            topic=self.topic_politics,
        )

        response = self.client.get(reverse("app:topic-list"))

        topics = list(response.context["topic_list"])
        self.assertEqual([topic.name for topic in topics], ["Business", "Politics"])
        self.assertEqual(
            {topic.name: topic.newspapers_count for topic in topics},
            {"Business": 1, "Politics": 2},
        )

    def test_newspaper_list_orders_items_by_published_date_descending(self):
        response = self.client.get(reverse("app:newspaper-list"))

        self.assertEqual(
            [newspaper.title for newspaper in response.context["newspaper_list"]],
            ["Evening Brief", "Morning Brief"],
        )

    def test_newspaper_detail_shows_publishers_without_editor_actions_for_public_user(self):
        response = self.client.get(
            reverse("app:newspaper-detail", args=[self.newspaper_new.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.owner.username)
        self.assertContains(response, self.publisher.username)
        self.assertNotContains(
            response,
            reverse("app:newspaper-update", args=[self.newspaper_new.id]),
        )
        self.assertNotContains(
            response,
            reverse("app:newspaper-delete", args=[self.newspaper_new.id]),
        )

    def test_redactor_list_orders_users_by_username(self):
        response = self.client.get(reverse("app:redactor-list"))

        self.assertEqual(
            list(response.context["redactor_list"].values_list("username", flat=True)),
            ["alpha", "owner", "publisher"],
        )

    def test_redactor_detail_shows_publications_and_self_service_actions_for_owner(self):
        self.login_user(self.owner)

        response = self.client.get(reverse("app:redactor-detail", args=[self.owner.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newspaper_new.title)
        self.assertContains(response, reverse("app:redactor-update", args=[self.owner.id]))
        self.assertContains(response, reverse("app:redactor-delete", args=[self.owner.id]))

    def test_redactor_detail_hides_self_service_actions_for_other_user(self):
        self.login_user(self.publisher)

        response = self.client.get(reverse("app:redactor-detail", args=[self.owner.id]))

        self.assertNotContains(response, reverse("app:redactor-update", args=[self.owner.id]))
        self.assertNotContains(response, reverse("app:redactor-delete", args=[self.owner.id]))

    def test_register_view_creates_redactor_and_redirects_to_login(self):
        response = self.client.post(
            reverse("app:register"),
            {
                "username": "new-hire",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("login"))
        new_hire = Redactor.objects.get(username="new-hire")
        self.assertTrue(new_hire.check_password("StrongPass123!"))
        self.assertTrue(new_hire.user_permissions.filter(codename="add_topic").exists())
