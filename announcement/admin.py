from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import MusicianAnnouncement, MusicianAnswerAnnonucement

# Register your models here.
@admin.register(MusicianAnnouncement)
class MusicianAnnouncementAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),

        (_("Corps de l'annonce"), {'fields':('content','author', 'county_name', 'town', 'is_active' )}),
    )