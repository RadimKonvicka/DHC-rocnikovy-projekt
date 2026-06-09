from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Artist, Release
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth

def index(request):
    total_artists = Artist.objects.count()
    total_releases = Release.objects.count()

    spotify_user = None
    top_artists_data = []
    dhc_match_percentage = 0
    matched_artists = []
    recommendations = []

    token_info = request.session.get('token_info', None)
    
    if token_info:
        try:
            sp = spotipy.Spotify(auth=token_info['access_token'])
            spotify_user = sp.current_user()
            
            # Vytáhneme TOP 10 interpretů ze Spotify
            artists_results = sp.current_user_top_artists(limit=10, time_range='medium_term')
            
            # Načteme lokální umělce
            local_artists = Artist.objects.all()
            local_artists_lower = {a.name.lower(): a for a in local_artists}

            # Sbírka žánrů, které uživatel reálně poslouchá na Spotify
            user_spotify_genres = set()

            match_count = 0
            for item in artists_results['items']:
                artist_name = item['name']
                artist_img = item['images'][0]['url'] if item['images'] else None
                
                # Uložíme si žánry tohoto umělce ze Spotify pro pozdější doporučování
                for g in item.get('genres', []):
                    user_spotify_genres.add(g.lower())
                
                is_matched = artist_name.lower() in local_artists_lower
                if is_matched:
                    match_count += 1
                    matched_artists.append(artist_name)

                top_artists_data.append({
                    'name': artist_name,
                    'image': artist_img,
                    'url': item['external_urls']['spotify'],
                    'is_matched': is_matched
                })
            
            if top_artists_data:
                dhc_match_percentage = int((match_count / len(top_artists_data)) * 100)

            # --- SYSTÉM DOPORUČOVÁNÍ PODLE ŽÁNRŮ ---
            if dhc_match_percentage < 100:
                for local_art in local_artists:
                    if local_art.name in matched_artists:
                        continue
                    
                    local_genres = [g.strip().lower() for g in local_art.genres.split(',') if g.strip()]
                    has_genre_match = any(lg in user_spotify_genres for lg in local_genres)
                    
                    if has_genre_match:
                        random_release = local_art.releases.first()
                        recommendations.append({
                            'artist': local_art.name,
                            'reason': f"Posloucháš podobné žánry ({local_art.genres})",
                            'release': random_release.title if random_release else "Připravované album"
                        })
        except Exception:
            request.session['token_info'] = None

    context = {
        'total_artists': total_artists,
        'total_releases': total_releases,
        'spotify_user': spotify_user,
        'top_artists': top_artists_data,
        'dhc_match': dhc_match_percentage,
        'matched_artists': matched_artists,
        'recommendations': recommendations,
    }
    return render(request, 'vault/index.html', context)


def release_list(request):
    # 1. Načteme lokální alba z databáze
    local_releases = Release.objects.all()
    
    # 2. Pokusíme se vytáhnout Spotify token ze session přihlášeného uživatele
    spotify_token = request.session.get('spotify_token')
    spotify_releases = []

    if spotify_token:
        # Pokud token máme, pošleme real-time požadavek na Spotify API pro novinky
        headers = {'Authorization': f'Bearer {spotify_token}'}
        url = 'https://api.spotify.com/v1/browse/new-releases?limit=10'
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Vytáhneme data ze Spotify struktury
                spotify_releases = response.json().get('albums', {}).get('items', [])
        except Exception as e:
            print(f"Chyba při komunikaci se Spotify API: {e}")

    # 3. Předáme oboje do šablony
    context = {
        'releases': local_releases,          # Pro spodní sekci (lokální Vault)
        'spotify_releases': spotify_releases # Pro horní sekci (Real-time trendy)
    }
    return render(request, 'vault/release_list.html', context)

def release_detail(request, pk):
    release = get_object_or_404(Release, pk=pk)
    return render(request, 'vault/release_detail.html', {'release': release})


def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-top-read"
    )


def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def spotify_callback(request):
    # Sem se uživatel vrátí ze Spotify, zpracujeme token
    sp_oauth = get_spotify_oauth()
    session_code = request.GET.get('code')
    
    if session_code:
        token_info = sp_oauth.get_access_token(session_code)
        request.session['token_info'] = token_info
        # TADY TO JE: Změněno zpět na spotify_stats, aby tě to po loginu hodilo na tu stránku s písničkami
        return redirect('spotify_stats')
    
    return redirect('index')


def spotify_stats(request):
    token_info = request.session.get('token_info', None)
    if not token_info:
        return redirect('spotify_login')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Vytáhneme TOP 10 skladeb uživatele
    results = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    
    top_tracks = []
    for item in results['items']:
        # Získání obrázku alba (bereme ten střední rozměr, obvykle index 1)
        album_covers = item['album']['images']
        cover_url = album_covers[1]['url'] if len(album_covers) > 1 else album_covers[0]['url'] if album_covers else None
        
        top_tracks.append({
            'name': item['name'],
            'artist': item['artists'][0]['name'],
            'url': item['external_urls']['spotify'],
            'preview_url': item.get('preview_url'),  # 30s ukázka (může být někdy None, ošetříme v HTML)
            'cover_url': cover_url  # Obrázek alba/interpreta
        })
        
    return render(request, 'vault/spotify_stats.html', {'top_tracks': top_tracks})

def spotify_logout(request):
    # Kompletně vymaže uložené Spotify informace ze session
    if 'token_info' in request.session:
        del request.session['token_info']
    return redirect('index')

from django.shortcuts import render
from .models import Artist, Release  # Ověř, že máš tyto modely správně pojmenované

# ... (tvoje staré views zde zůstávají)

def db_artists_list(request):
    artists = Artist.objects.all().order_by('name')
    return render(request, 'vault/db_artists.html', {'artists': artists})

def db_releases_list(request):
    releases = Release.objects.all().order_by('title')
    return render(request, 'vault/db_releases.html', {'releases': releases})