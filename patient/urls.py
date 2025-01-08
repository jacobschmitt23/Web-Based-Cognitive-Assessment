from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path("welcome/<int:value>", views.welcome, name="welcome"),
    path("digitIntro", views.digitIntro, name="digitIntro"),
    path("digitKeyboard", views.digitKeyboard, name="digitKeyboard"),
    path("mixedIntro", views.mixedIntro, name="mixedIntro"),
    path("mixedKeyboard", views.mixedKeyboard, name="mixedKeyboard"),
    path("mixedStimuli", views.mixedStimuli, name="mixedStimuli"),
    path("stimuli", views.stimuli, name="stimuli"),
    path("response", views.response, name="response"),
    path("conclusion", views.conclusion, name="conclusion"),
    path("practiceFinish", views.practiceFinish, name="practiceFinish"),
    path("isQuit", views.isQuit, name="isQuit"),
    path("isInvalid", views.isInvalid, name="isInvalid"),
]


