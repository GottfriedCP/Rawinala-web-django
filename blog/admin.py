from django.contrib import admin
from .models import Tag, Article

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_created')
    ordering = ('name', 'time_created')

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }
    list_display = ('title', 'time_created', 'publish_status', 'views')
    ordering = ('-time_created', )
    list_filter = ('publish_status', 'tag')
    actions = ['publish_article', 'unpublish_article', 'reset_view_count']

    def publish_article(self, request, queryset):
        queryset.update(publish_status=True)
    publish_article.short_description = 'Publish selected articles'

    def unpublish_article(self, request, queryset):
        queryset.update(publish_status=False)
    unpublish_article.short_description = 'Unpublish selected articles'

    def reset_view_count(self, request, queryset):
        queryset.update(views=0)
    reset_view_count.short_description = 'Reset view count to 0'

# Register your models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)