from django.contrib import admin
from .models import ShortenedLink


# Register your models here.
class ShortenedLinkAdmin(admin.ModelAdmin):
    fields = [
        'user', 'special_name', 'original_link', 'shortened_link'
    ]
    list_display = [
        'original_link', 'shortened_link'
    ]
    search_fields = [
        'user', 'special_name'
    ]


admin.site.register(ShortenedLink, ShortenedLinkAdmin)
