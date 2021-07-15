from django.urls import path

from . import views

urlpatterns = [
    path('favourites', views.favourites, name='favourites'),
    path('bands', views.bands, name='bands'),
    path('bands/<int:band_id>', views.get_band, name='band'),
    path('albums', views.add_album, name='albums'),
    path('bands/song/<int:song_id>/favourite', views.add_favourite, name='add-favourite'),
]
