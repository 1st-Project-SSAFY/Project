from django.urls import path, register_converter
from buildings import converters
from . import views

app_name='building-user'

register_converter(converters.SignedIntConverter, 'signed_int')

urlpatterns = [
    # 건물 관리자 - 건물 조회
    path('building/', views.building, name='building'),
    # 건물 관리자 - 층별 정보
    path('building/<signed_int:floor>/', views.building_floor, name='building_floor'),
    # 건물 관리자 - 로봇 상세 정보
    path('building/<signed_int:floor>/<int:robot_pk>/', views.building_floor_robot, name='building_floor_robot'),
    

]