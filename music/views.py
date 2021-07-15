import json
from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Band, Album, Song


def favourites(request):
    data = {
        band.name: {
            album.name: [
                (
                    song.id,
                    song.name,
                    song.favourite,
                    '+'.join(band.name.split() + song.name.split())
                )
                for song in album.get_favourites()
            ]
            for album in band.get_albums()
        }
        for band in Band.objects.all()
    }

    favourite_music = {}
    for band_name, albums in data.items():
        favourite_albums = defaultdict(list)
        for album, songs in albums.items():
            if songs:
                favourite_albums[album].extend(songs)
        if favourite_albums:
            favourite_music[band_name] = favourite_albums.items()

    return render(request, 'music/favourites.html', {'data': favourite_music.items()})


@csrf_exempt
def bands(request):
    if request.method == 'GET':
        alphabetical = defaultdict(list)
        all_bands = Band.objects.all()
        for band in all_bands:
            alphabetical[band.name[0]].append(band)

        total_bands = all_bands.count()
        total_albums = Album.objects.all().count()
        total_songs = Song.objects.all().count()

        return render(request, 'music/all-bands.html', {
            'data': alphabetical.items(),
            'total_bands': total_bands,
            'total_albums': total_albums,
            'total_songs': total_songs,
        })

    elif request.method == 'POST':
        band_name = request.POST['band']
        try:
            band = Band(name=band_name)
            band.save()
        except:
            band = Band.objects.get(name=band_name)

        return JsonResponse({'band_id': band.id})


def get_band(request, band_id):
    band = Band.objects.get(id=band_id)

    data = {}
    albums = band.get_albums()
    for album in albums:
        data[album.name] = [
            (
                song.id,
                song.name,
                song.favourite,
                '+'.join(band.name.split() + song.name.split())
            )
            for song in album.get_songs()
        ]

    total_albums = albums.count()
    total_songs = sum(len(songs) for _, songs in data.items())

    return render(request, 'music/albums.html', {
        'data': data.items(),
        'band_name': band.name,
        'total_albums': total_albums,
        'total_songs': total_songs,
    })


@csrf_exempt
def add_album(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        album_name = body['album']
        band_id = body['band_id']
        songs = body['songs']
        album = Album(name=album_name, band_id=band_id)
        album.save()

        for song in songs:
            song = Song(name=song, album_id=album.id)
            song.save()

        return JsonResponse({'band_id': album.id})


def add_favourite(request, song_id):
    song = Song.objects.get(id=song_id)
    song.favourite = not song.favourite
    song.save()

    url = request.GET['url']

    return redirect(url)
