from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from app.models import Topic, Newspaper, Redactor


def index(request):
    context = {
        "num_topics": Topic.objects.count(),
        "num_newspapers": Newspaper.objects.count(),
        "num_redactors": Redactor.objects.count(),
    }
    return render(request, "app/index.html", context)


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 10
    queryset = Topic.objects.annotate(
        newspapers_count=Count("newspapers")
    ).order_by("name")
    template_name = "app/topic_list.html"
    context_object_name = "topic_list"


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 10
    queryset = Redactor.objects.all().order_by("username")
    template_name = "app/redactor_list.html"
    context_object_name = "redactor_list"


class RedactorDetailView(generic.DetailView):
    model = Redactor
    template_name = "app/redactor_detail.html"
    context_object_name = "redactor"

    def get_queryset(self):
        return (
            Redactor.objects
            .prefetch_related("newspapers")  # related_name
        )


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 10
    template_name = "app/newspaper_list.html"
    context_object_name = "newspaper_list"

    def get_queryset(self):
        return (
            Newspaper.objects
            .select_related("topic")
            .prefetch_related("publishers")
            .order_by("-published_date")
        )


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    template_name = "app/newspaper_detail.html"
    context_object_name = "newspaper"

    def get_queryset(self):
        return (
            Newspaper.objects
            .select_related("topic")
            .prefetch_related("publishers")
        )
