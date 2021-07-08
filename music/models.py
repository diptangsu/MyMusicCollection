from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=255)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    favourite = models.BooleanField()

    def __str__(self):
        return f'{self.name} [{self.album.band.name} ({self.album.name})'


class Playlist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} ({self.get_all_songs().count()} songs)'

    def get_all_songs(self):
        return PlaylistSongs.objects.filter(playlist=self)


class PlaylistSongs(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
