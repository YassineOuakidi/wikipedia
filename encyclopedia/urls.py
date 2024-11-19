from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>" , views.entry_info , name="view"),
    path("wiki/<str:entry>" , views.entry_info , name="view"),
    path("random/", views.random_entry , name="random_title"),
    path("create/" , views.create_new_page , name="create_new"),
    path("search/" , views.search_list , name="search_list"),
    path("edit/<str:entry>" , views.edit_content, name="edit_content")
]
