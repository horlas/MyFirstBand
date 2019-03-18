from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import MusicianAnnouncement, MusicianAnswerAnnouncement

# Register your models here.
@admin.register(MusicianAnnouncement)
class MusicianAnnouncementAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),

        (_("Corps de l'annonce"), {'fields':('content','author','code', 'county_name', 'town', 'is_active' )}),
    )

@admin.register(MusicianAnswerAnnouncement)
class MusicianAnswerAnnouncementAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('musician_announcement',)
        }),

        (_("Corps du message"), {'fields':('content','author', 'parent_id', 'recipient')}),
    )