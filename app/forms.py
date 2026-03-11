from django import forms

from app.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]
