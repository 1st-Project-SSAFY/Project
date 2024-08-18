from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    # 소방관 회원가입
    path('signup/', views.signup, name='signup'),
    # 소방관 로그인
    path('login/', views.CustomObtainAuthToken.as_view(), name='login'),
    # 건물 관리자 로그인
    path('manager-login/', views.CustomManagerAuthToken.as_view(), name='manager_login'),
    # 건물 관리자 로그아웃
    path('manager-logout/', views.building_manager_logout, name='manager_logout'),




    # fake data 생성
    path('fake-firestation/', views.fake_firestation, name='fake_firestation'),
    path('fake-firefighter/', views.fake_firefighter, name='fake_firefighter'),
]