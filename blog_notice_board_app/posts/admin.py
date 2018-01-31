from django.contrib import admin

# Register your models here.
from posts.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']
    list_display_links = ['title', 'timestamp', 'updated']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    readonly_fields = ('slug',)

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
