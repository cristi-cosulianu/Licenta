from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /mbsapi/persons/1
    path('persons/<int:person_id>/', views.person, name = 'person'),
    # ex: /mbsapi/persons/1/name/
    path('persons/<int:person_id>/name/', views.person_name, name='person_name')
]