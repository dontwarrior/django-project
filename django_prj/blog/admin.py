from django.contrib import admin

from blog.models import Post, Like


class LikeInLine(admin.TabularInline):
    model = Like


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'author', 'content', 'date_posted']
    list_filter = ['date_posted', 'author']
    inlines = [
        LikeInLine,
    ]


admin.site.register(Post, PostAdmin)
# admin.site.register(Like)
