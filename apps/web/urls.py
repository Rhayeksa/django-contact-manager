from django.urls import path

from .views.person.index import index as person

app_name = "web"


urlpatterns = [
    path(route="", view=person, name="person"),
]
