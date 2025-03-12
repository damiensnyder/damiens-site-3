from django.contrib import admin
from .models import Flag, Vote, Pin, Report


class FlagAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_url', 'width', 'height', 'source', 'total_score', 'num_votes')
    list_filter = ('num_votes', 'total_score')
    search_fields = ('name__icontains',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'flag', 'user', 'score')
    list_filter = ('score',)
    search_fields = ('flag__name__icontains', 'user__username__icontains')


class PinAdmin(admin.ModelAdmin):
    list_display = ('user', 'flag')
    list_filter  = ('user',)
    search_fields = ('user__username__icontains', 'flag__name__icontains')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'flag')
    list_filter  = ('user',)
    search_fields = ('user__username__icontains', 'flag__name__icontains')


admin.site.register(Flag, FlagAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Pin, PinAdmin)
admin.site.register(Report, ReportAdmin)

