from django.urls import path
from . import views

app_name='buildings'
urlpatterns = [
    path('check-building/', views.check_building, name='check_building'),

    # fake data 생성
    ## REST API 설계 규칙 찾아보고 정리하면서 만들어보기
    path('fake-building/', views.fake_building, name='fake_building'),
    path('fake-buildingfloor/', views.fake_building_floor, name='fake_buildingfloor'),
    path('fake-sprinkler/', views.fake_sprinkler, name='fake_sprinkler'),
    
]