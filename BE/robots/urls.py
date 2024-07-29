from django.urls import path
from . import views

app_name='robots'
urlpatterns = [
    # fake data 생성
    path('fake-robots/', views.fake_robots, name='fake_robots'),
]