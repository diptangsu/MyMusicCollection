from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name} ({len(self.get_albums())})'

    def get_albums(self):
        return Album.objects.filter(band=self)


class Album(models.Model):
    name = models.CharField(max_length=255)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} [{self.band.name}]'

    def get_songs(self):
        return Song.objects.filter(album=self).order_by('-favourite')

    def get_favourites(self):
        return Song.objects.filter(album=self, favourite=True)


class Song(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} [{self.album.band.name} ({self.album.name})]'


class Playlist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} ({self.get_songs().count()} songs)'

    def get_songs(self):
        return PlaylistSongs.objects.filter(playlist=self)


class PlaylistSongs(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
