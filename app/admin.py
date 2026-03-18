from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from app.models import Topic, Redactor, Newspaper


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "years_of_experience",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    list_per_page = 25

    fieldsets = UserAdmin.fieldsets + (
        (_("Additional info"), {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Additional info"), {"fields": ("years_of_experience",)}),
    )

    readonly_fields = UserAdmin.readonly_fields + ("published_newspapers",)

    def published_newspapers(self, obj: Redactor):
        qs = obj.newspapers.all().only("id", "title")[:30]  # related_name="newspapers"
        if not qs:
            return "-"
        return format_html_join(
            "\n",
            '<a href="/admin/app/newspaper/{}/change/">{}</a>',
            ((n.id, n.title) for n in qs),
        )

    published_newspapers.short_description = "Newspapers (first 30)"


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "topic", "published_date", "publishers_count")
    list_select_related = ("topic",)
    list_filter = ("topic", "published_date")
    search_fields = ("title", "content", "topic__name", "publishers__username", "publishers__email")
    date_hierarchy = "published_date"
    ordering = ("-published_date", "title")
    list_per_page = 25

    filter_horizontal = ("publishers",)
    autocomplete_fields = ("topic",)

    fieldsets = (
        (None, {"fields": ("title", "topic", "published_date")}),
        (_("Content"), {"fields": ("content",)}),
        (_("Publishers"), {"fields": ("publishers",)}),
    )

    @admin.display(description="Publishers")
    def publishers_count(self, obj: Newspaper) -> int:
        return obj.publishers.count()
