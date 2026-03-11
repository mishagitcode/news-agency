from django import forms

from app.models import Topic, Newspaper


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ["title", "content", "published_date", "topic", "publishers"]
