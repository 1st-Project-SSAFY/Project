from django.urls import path, register_converter
from . import views, converters

app_name='buildings'

register_converter(converters.SignedIntConverter, 'signed_int')

urlpatterns = [
    # 소방관 - 관할 건물 조회
    path('check-building/', views.check_building, name='check_building'),
    # 소방관 - 관할 건물 선택
    path('check-building/<int:pk>/', views.choose_building, name='choose_building'),
    # 소방관 - 층 선택
    path('check-building/<int:pk>/<signed_int:floor>/', views.choose_building_floor, name='choose_building_floor'),
    # 소방관 - 로봇 상세 정보
    path('check-building/<int:pk>/<signed_int:floor>/<int:robot_pk>/', views.check_robot, name='check_robot'),
    
    
    # 로봇의 최적경로
    path('robot-escape/<int:pk>/<signed_int:floor>/', views.robot_escape_root, name='robot_escape_root'),
    
    # 소방관(관리직) - 화재 상황 기록
    path('check-building/<int:pk>/record/', views.record_fire_issue, name='record_fire_issue'),
    
    # 소방관(관리직) - 건물 관리자 등록 및 비밀번호 재설정
    path('check-building/<int:pk>/register-manager/', views.register_manager, name='register_manager'),
    
    # 소방관(관리직) - 건물 등록
    path('register-building/', views.building_register, name='building_register'),
    # 소방관(관리직) - 건물 층별 이미지 및 정보 등록
    path('register-building-floor/', views.building_floor_register, name='building_floor_register'),
    
    
    # fake data 생성
    ## REST API 설계 규칙 찾아보고 정리하면서 만들어보기
    path('fake-building/', views.fake_building, name='fake_building'),
    path('fake-buildingfloor/', views.fake_building_floor, name='fake_buildingfloor'),
    path('fake-sprinkler/', views.fake_sprinkler, name='fake_sprinkler'),
    
]