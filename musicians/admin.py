from django.contrib import admin

from musicians.models import UserProfile, Instrument
from authentication.models import User
from django.utils.translation import ugettext_lazy as _


# class UserProfilAdmin(admin.TabularInline):
#     model = UserProfile
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     inlines = [UserProfilAdmin]
#
#




# Register your models here.
@admin.register(UserProfile)
class UserProfilAdmin(admin.ModelAdmin):


    fieldsets = (
        (None, {
            'fields': ('user',)
        }),

        (_('Information du Profil'), {'fields':('gender','username', 'bio', 'code', 'county_name', 'town', 'birth_year', 'avatar', )}),


    )
    # readonly_fields = ['created_at', 'update_at']


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):

    fieldsets =  (
        (None, {'fields':('musician',)
                }),
        (_('Instrument joué'),{'fields': ('instrument', 'level', )}),

    )