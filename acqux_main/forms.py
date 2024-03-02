from django import forms
from .models import Article, ArticleSeries
import shortuuid
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.template.defaultfilters import slugify
from tinymce.widgets import TinyMCE

class SeriesCreateForm(forms.ModelForm):
    class Meta:
        model = ArticleSeries

        fields = [
            "title",
            "subtitle",
            # "slug",
            "image",
        ]

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = [
            "title",
            "subtitle",
            # "article_slug",
            "content",
            "notes",
            "series",
            "image",
        ]

        def save(self, commit=True, *args, **kwargs):
            instance = super().save(commit=False)

            if not instance.article_slug:
                uuid_key = shortuuid.uuid()
                unique_id = uuid_key[:4]
                instance.article_slug = slugify(instance.title) + "-" + str(unique_id.lower())

            if commit:
                instance.save()
            return instance

class SeriesUpdateForm(forms.ModelForm):
    class Meta:
        model = ArticleSeries

        fields = [
            "title",
            "subtitle",
            "image",
        ]

class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = [
            "title",
            "subtitle",
            "content",
            "notes",
            "series",
            "image",
        ]


class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Email content")