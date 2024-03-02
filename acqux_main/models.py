from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
import shortuuid
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth import get_user_model

from django.template.defaultfilters import slugify
import os


class ArticleSeries(models.Model):

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("ArticleSeries", slugify(self.slug), instance)
        return None

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True)
    slug = models.SlugField("Series slug", null=False, blank=False, unique=True)
    published = models.DateTimeField("Date published", default=timezone.now)
    pid = ShortUUIDField(
        length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123"
    )
    author = models.ForeignKey(
        get_user_model(), default=1, on_delete=models.SET_DEFAULT
    )
    image = models.ImageField(
        default="default/no_image.jpg", upload_to=image_upload_to, max_length=255
    )

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(ArticleSeries, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Series"
        ordering = ["-published"]


class Article(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join(
                "ArticleSeries",
                slugify(self.series.slug),
                slugify(self.article_slug),
                instance,
            )
        return None

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True)
    article_slug = models.SlugField(
        "Article slug", null=False, blank=False, unique=True
    )
    content = HTMLField(blank=True, default="")
    notes = HTMLField(blank=True, default="")
    published = models.DateTimeField("Date published", default=timezone.now)
    modified = models.DateTimeField("Date modified", default=timezone.now)
    series = models.ForeignKey(
        ArticleSeries, default="", verbose_name="Series", on_delete=models.SET_DEFAULT
    )
    author = models.ForeignKey(
        get_user_model(), default=1, on_delete=models.SET_DEFAULT
    )
    image = models.ImageField(
        default="default/no_image.jpg", upload_to=image_upload_to, max_length=255
    )

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.article_slug == "" or self.article_slug == None:
            self.article_slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return self.series.slug + "/" + self.article_slug

    class Meta:
        verbose_name_plural = "Article"
        ordering = ["-published"]
