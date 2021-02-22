from django.conf.urls import url
from BookConferenceHallApp.views import *

app_name = 'book'
urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^Hall/(?P<id>(\d)+)$', Hall, name="Hall"),
    url(r'^Hall/new$', NewHallView.as_view(), name="new-Hall"),
    url(r'^Hall/modify/(?P<id>(\d)+)$', ModifyView.as_view(), name="modify"),
    url(r'^Hall/delete/(?P<id>(\d)+)$', DeleteView.as_view(), name="delete"),
    url(r'^Hall/reservation/(?P<id>(\d)+)$', ReservationView.as_view(), name="reservation"),
    url(r'^search$', SearchView.as_view(), name="search"),

]