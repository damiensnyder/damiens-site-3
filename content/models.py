from django.db import models

import markdown
import markdown.extensions.codehilite
import markdown.extensions.footnotes
import markdown.extensions.smarty
import markdown_katex
import customblocks
from . import damiens_md


class Tag(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)


class Shortform(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    timestamp = models.DateField(null=True)
    primary_tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=100000, default="")
    markup = models.TextField(max_length=100000, blank=True)

    def save(self, *args, **kwargs):
        self.markup = markdown.markdown(
            self.body,
            extensions=[
                'markdown_katex',
                'customblocks',
                'codehilite',
                'smarty'
            ],
            extension_configs={
                'customblocks': {
                    'generators': {
                        'soundcloud': damiens_md.soundcloud_embed,
                        'audio': damiens_md.audio_embed
                    }
                },
            }
        )
        models.Model.save(self)


class Content(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200, blank=True)
    timestamp = models.DateField(null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="all_tags")
    primary_tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=100000, default="")
    markup = models.TextField(max_length=100000, blank=True)

    def save(self, *args, **kwargs):
        if (self.thumbnail is None) or (self.thumbnail == ""):
            self.thumbnail = "content/logo.svg"
        elif "/" not in self.thumbnail:
            self.thumbnail = f"content/thumbs/{self.thumbnail}"
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
                damiens_md.CaptionExtension()
            ],
            extension_configs={
                'customblocks': {
                    'generators': {
                        'soundcloud': damiens_md.soundcloud_embed,
                        'audio': damiens_md.audio_embed
                    }
                },
            }
        )
        models.Model.save(self)