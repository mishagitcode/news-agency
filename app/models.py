from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        full_name = self.get_full_name().strip()
        return full_name or self.username


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="newspapers",
    )
    publishers = models.ManyToManyField(
        Redactor,
        related_name="newspapers",
        blank=True,
    )

    class Meta:
        ordering = ["-published_date", "title"]

    def __str__(self) -> str:
        return self.title
