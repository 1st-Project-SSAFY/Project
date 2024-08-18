from django.urls import path, register_converter
from . import views
from buildings import converters

register_converter(converters.SignedIntConverter, 'signed_int')

app_name='fireissues'
urlpatterns = [
    # 화재 발생 팝업
    path('fire-popup/', views.fire_popup, name='fire_popup'),
    # 건물 정상 로봇 갯수 확인
    path('robot-state/<int:pk>/', views.robot_count, name='robot_count'),
    # 층별 로봇 상태 확인
    path('robot-state/<int:pk>/<signed_int:floor>/', views.robot_state, name='robot_state'),
    # 로봇 상세 정보 확인
    path('robot-state/<int:pk>/<signed_int:floor>/<int:robot_pk>/', views.robot_detail, name='robot_detail'),
]