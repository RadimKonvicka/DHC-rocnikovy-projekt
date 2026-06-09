from django.contrib import admin
from .models import Artist, Release, Track

# Tohle umožní přidávat tracky přímo v detailu alba (vypadá to profi)
class TrackInline(admin.TabularInline):
    model = Track
    extra = 1

class ReleaseAdmin(admin.ModelAdmin):
    inlines = [TrackInline]
    list_display = ('title', 'artist', 'release_date')

admin.site.register(Artist)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Track)