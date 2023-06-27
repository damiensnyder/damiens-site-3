from django.db import models

import markdown
import markdown.extensions.codehilite
import markdown.extensions.footnotes
import markdown.extensions.smarty
import markdown.extensions.tables
import markdown.extensions.fenced_code
import markdown.extensions.sane_lists
import markdown.extensions.admonition
import markdown_katex
import customblocks
from . import damiens_md
from accounts.models import User
from django.contrib.auth.models import Group


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.url


class Shortform(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200, blank=True)
    timestamp = models.DateField(null=True)
    primary_tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=100000, default="")
    markup = models.TextField(max_length=100000, blank=True)
    group_needed = models.ForeignKey(Group, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.url

    def save(self, *args, **kwargs):
        self.markup = markdown.markdown(
            self.body,
            extensions=[
                'markdown_katex',
                'customblocks',
                'codehilite',
                'smarty',
                'sane_lists',
                damiens_md.DelExtension()
            ],
            extension_configs={
                'customblocks': {
                    'generators': {
                        'soundcloud': damiens_md.soundcloud_embed,
                        'audio': damiens_md.audio_embed,
                        'summary': damiens_md.summary_details
                    }
                },
            }
        )
        models.Model.save(self)


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200, blank=True)
    timestamp = models.DateField(null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="all_tags")
    primary_tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=100000, default="")
    markup = models.TextField(max_length=100000, blank=True)
    group_needed = models.ForeignKey(Group, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.url

    def save(self, *args, **kwargs):
        if (self.thumbnail is None) or (self.thumbnail == "") or (self.thumbnail == "logo.svg"):
            self.thumbnail = "logo.svg"
        elif "/" not in self.thumbnail:
            self.thumbnail = f"thumbs/{self.thumbnail}"
        self.markup = markdown.markdown(
            self.body,
            extensions=[
                'markdown_katex',
                'customblocks',
                'codehilite',
                'footnotes',
                'smarty',
                'tables',
                'fenced_code',
                'sane_lists',
                'admonition',
                damiens_md.DelExtension()
            ],
            extension_configs={
                'customblocks': {
                    'generators': {
                        'soundcloud': damiens_md.soundcloud_embed,
                        'audio': damiens_md.audio_embed,
                        'summary': damiens_md.summary_details
                    }
                },
            }
        )
        models.Model.save(self)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    from_content = models.ForeignKey(Content, on_delete=models.SET_NULL, null=True, blank=True)
    from_shortform = models.ForeignKey(Shortform, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateField()
    body = models.TextField(max_length=10000)

    def save(self, *args, **kwargs):
        models.Model.save(self)

    def __str__(self) -> str:
        return f"{self.user} ({self.timestamp}): {self.body[:100]}"