from django.contrib import admin

from musicians.models import UserProfile, Instrument
from django.utils.translation import ugettext_lazy as _



# Register your models here.
@admin.register(UserProfile)
class UserProfilAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user',)
        }),

        (_('Information du Profil'), {'fields':('gender','username', 'bio', 'code', 'county_name', 'town', 'birth_year', 'avatar', )}),

    )


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):

    fieldsets =  (
        (None, {'fields':('musician',)
                }),
        (_('Instrument joué'),{'fields': ('instrument', 'level', )}),

    )