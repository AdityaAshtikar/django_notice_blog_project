from django.contrib import admin

# Register your models here.
from posts.models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']
    list_display_links = ['title', 'timestamp', 'updated']
    list_filter = ['updated', 'timestamp', 'category']
    search_fields = ['title', 'content', 'category']
    readonly_fields = ('slug',)

    class Meta:
        model = Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['topic']
    list_display_links = ['topic']
    search_fields = ['topic']
    list_filter = ['topic']
    readonly_fields = ('slug',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
