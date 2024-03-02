from django.contrib import admin
from .models import Article, ArticleSeries

class ArticleSeriesAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'subtitle',
        'slug',
        'pid',
        'author',
        'image'
        # 'published'
    ]
    prepopulated_fields = {"slug": ("title",)}

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Header", {"fields": ['title', 'subtitle', 'article_slug', 'series','author','image']}),
        ("Content", {"fields": ['content', 'notes']}),
        ("Date", {"fields": ['modified']})
    ]
    prepopulated_fields = {"article_slug": ("title",)}

# Register your models here.
admin.site.register(ArticleSeries, ArticleSeriesAdmin)
admin.site.register(Article, ArticleAdmin)