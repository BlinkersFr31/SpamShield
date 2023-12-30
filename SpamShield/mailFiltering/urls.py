from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:serveur_id>", views.listemails, name="listemails"),
    path("serveurs", views.serveurs, name="serveurs"),
    path("serveur/<int:serveur_id>", views.serveur, name="serveur"),
    path("<int:serveur_id>/saveServeur", views.saveServeur, name="saveServeur"),
]