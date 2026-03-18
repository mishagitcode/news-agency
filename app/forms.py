from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission

from app.models import Topic, Newspaper, Redactor


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ["title", "content", "published_date", "topic", "publishers"]


class RedactorForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        ]


class RedactorCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user.user_permissions.add(
                *Permission.objects.filter(
                    codename__in=[
                        "add_topic",
                        "change_topic",
                        "delete_topic",
                        "add_newspaper",
                        "change_newspaper",
                        "delete_newspaper",
                        "change_redactor",
                        "delete_redactor",
                    ]
                )
            )

        return user

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = [
            "username",
            "password1",
            "password2",
        ]
