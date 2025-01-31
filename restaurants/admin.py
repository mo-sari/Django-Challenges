from django.contrib import admin
from .models import (
    Restaurant,
    Sale,
    Rating,
    Comment
)


class CommentAdmin(admin.ModelAdmin):
    list_display = [
                    'text',
                    'content_type',
                    'object_id',
                    'content_object'
                    ]


class RatingAdmin(admin.ModelAdmin):
    list_display = [
                    'id',
                    'restaurant__name',
                    'rating'
                     ]


# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Sale)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment, CommentAdmin)
