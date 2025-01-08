from django.urls import path
from . import views

app_name="doctor"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("manageTestLinks/", views.manageTestLinks, name="manageTestLinks"),
    path("datapage/<str:gottenTable>/", views.datapage, name="datapage")
]
