from django.urls import path

from .views.contact.add import add as contact_add
from .views.contact.detail import detail as contact_detail
from .views.contact.edit import edit as contact_edit
from .views.contact.index import index as contact
from .views.contact.utils.btn_delete import btn_delete as contact_delete
from .views.contact.utils.btn_delete_edu import \
    btn_delete_edu as contact_delete_edu
from .views.contact.utils.btn_delete_work import \
    btn_delete_work as contact_delete_work

app_name = "web"


urlpatterns = [
    path(route="", view=contact, name="contact"),
    path(route="contact/add/", view=contact_add, name="contact_add"),
    path(route="contact/edit/<str:id>", view=contact_edit, name="contact_edit"),
    path(route="contact/detail/<str:id>",
         view=contact_detail, name="contact_detail"),
    path(route="contact/delete/<str:id>",
         view=contact_delete, name="contact_delete"),
    path(route="contact/delete-edu/<str:contact_id>/<str:id>",
         view=contact_delete_edu, name="contact_delete_edu"),
    path(route="contact/delete-work/<str:contact_id>/<str:id>",
         view=contact_delete_work, name="contact_delete_work"),
]
