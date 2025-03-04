from django.contrib import admin
from .models import Tag, Content, Shortform, Message


class ExcludeSpamFilter(admin.SimpleListFilter):
    title = "exclude spam"

    parameter_name = "exclude"

    def lookups(self, request, model_admin):
        return [
            ("exclude", "exclude"),
        ]

    def queryset(self, request, queryset):
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "exclude":
            return queryset.exclude(
                from_content__url="accounts-announcement",
            )


class TagAdmin(admin.ModelAdmin):
    list_display = ('url', 'name')
    search_fields = ('url__icontains', 'name__icontains')


class ContentAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'timestamp', 'primary_tag', 'group_needed')
    list_filter = ('tags__name', 'group_needed')
    search_fields = ('url__icontains', 'title__icontains')
    exclude = ('markup',)


class ShortformAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'timestamp', 'primary_tag', 'group_needed')
    list_filter = ('primary_tag__name', 'group_needed')
    search_fields = ('url__icontains', 'title__icontains', 'body__icontains')
    exclude = ('markup',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_content', 'from_shortform', 'timestamp', 'body')
    list_filter = (ExcludeSpamFilter, 'user', 'from_content')
    search_fields = ('body__icontains',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Shortform, ShortformAdmin)
admin.site.register(Message, MessageAdmin)