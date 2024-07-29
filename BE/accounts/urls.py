from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomObtainAuthToken.as_view(), name='login'),

    # fake data 생성
    path('fake-firestation/', views.fake_firestation, name='fake_firestation'),
    path('fake-firefighter/', views.fake_firefighter, name='fake_firefighter'),
]