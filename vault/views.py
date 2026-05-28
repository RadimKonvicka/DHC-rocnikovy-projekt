from django.shortcuts import render, get_object_or_404
from .models import Artist, Release

def index(request):
    # Úvodní stránka - spočítáme celkový počet věcí v databázi
    total_artists = Artist.objects.count()
    total_releases = Release.objects.count()
    return render(request, 'vault/index.html', {
        'total_artists': total_artists,
        'total_releases': total_releases,
    })

def release_list(request):
    # Seznam všech alb
    releases = Release.objects.all().order_by('-release_date')
    return render(request, 'vault/release_list.html', {'releases': releases})

def release_detail(request, pk):
    # Detail jednoho alba + automaticky se vytáhnou tracky díky related_name
    release = get_object_or_404(Release, pk=pk)
    return render(request, 'vault/release_detail.html', {'release': release})