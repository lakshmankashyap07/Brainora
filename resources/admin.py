from django.contrib import admin
from .models import Resource

class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_by', 'downloads', 'total_likes', 'total_bookmarks', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'uploaded_by__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    def total_likes(self, obj):
        return obj.total_likes()
    total_likes.short_description = 'Likes'

    def total_bookmarks(self, obj):
        return obj.total_bookmarks()
    total_bookmarks.short_description = 'Bookmarks'

admin.site.register(Resource, ResourceAdmin)
