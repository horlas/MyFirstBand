from django.contrib import admin

from band.models import Band, Membership
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm



# class MusicalGenreForm(ModelForm):
#     class Meta:
#         model = MusicalGenre
#         exclude = ['band']




# Register your models here.
@admin.register(Band)
class BandAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),

        (_('Information du Groupe'), {'fields':('bio','code', 'county_name', 'town', 'type', 'avatar', )}),

        (_('Propriétaire du Groupe'), {'fields': ('owner',)}),
        # (_('Slug du Groupe'), {'fields': ('slug',)}),

    )


# @admin.register(MusicalGenre)
# class MusicalGenreAdmin(admin.ModelAdmin):
#
#     fieldsets =  (
#         (None, {'fields':('band',)
#                 }),
#         (_('Genre musical'),{'fields': ('musical_genre', )}),
#
#     )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    # fields = ('musician', 'band')

    fieldsets =  (
        (None, {'fields':('band',)}),
        (_('Membre'),{'fields': ('musician', 'invite_reason', )}
                    ,),

    )
    readonly_fields = ("date_joined",)


# Register your models here.
