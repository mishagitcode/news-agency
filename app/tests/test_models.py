from app.models import Newspaper, Redactor, Topic
from app.tests.base import AppTestCase


class TopicModelTests(AppTestCase):
    def test_str_returns_topic_name(self):
        topic = self.create_topic("Politics")

        self.assertEqual(str(topic), "Politics")

    def test_topics_are_ordered_by_name(self):
        self.create_topic("World")
        self.create_topic("Business")

        self.assertEqual(
            list(Topic.objects.values_list("name", flat=True)),
            ["Business", "World"],
        )


class RedactorModelTests(AppTestCase):
    def test_str_returns_full_name_when_available(self):
        redactor = self.create_user(
            "editor",
            first_name="Jane",
            last_name="Doe",
        )

        self.assertEqual(str(redactor), "Jane Doe")

    def test_str_falls_back_to_username_when_name_is_missing(self):
        redactor = self.create_user("editor")

        self.assertEqual(str(redactor), "editor")

    def test_redactors_are_ordered_by_username(self):
        self.create_user("zoe")
        self.create_user("anna")

        self.assertEqual(
            list(Redactor.objects.values_list("username", flat=True)),
            ["anna", "zoe"],
        )


class NewspaperModelTests(AppTestCase):
    def test_str_returns_newspaper_title(self):
        topic = self.create_topic("Politics")
        newspaper = self.create_newspaper(
            title="Daily Bulletin",
            content="Lead story",
            published_date=self.sample_date(10),
            topic=topic,
        )

        self.assertEqual(str(newspaper), "Daily Bulletin")

    def test_newspapers_are_ordered_by_date_desc_then_title(self):
        topic = self.create_topic("Politics")
        self.create_newspaper(
            title="B Story",
            content="Text",
            published_date=self.sample_date(10),
            topic=topic,
        )
        self.create_newspaper(
            title="A Story",
            content="Text",
            published_date=self.sample_date(10),
            topic=topic,
        )
        self.create_newspaper(
            title="Newest Story",
            content="Text",
            published_date=self.sample_date(11),
            topic=topic,
        )

        self.assertEqual(
            list(Newspaper.objects.values_list("title", flat=True)),
            ["Newest Story", "A Story", "B Story"],
        )
