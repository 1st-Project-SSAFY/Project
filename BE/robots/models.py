from django.db import models
from buildings.models import Building

# robot
class Robot(models.Model):
    # 로봇 아이디
    robot_id = models.CharField(max_length=50, unique=True)
    # 로봇 설치 건물 FK
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='install_building')
    # 로봇 등록일
    upload_day = models.DateField(auto_now_add=True)
    # 로봇 충전 상태
    charged_state = models.IntegerField()
    # 로봇 배터리 잔량
    battery = models.IntegerField()
    # 대피 안내 용액 잔량
    guide_liquid = models.IntegerField()
    # 로봇 정상 상태 여부
    right = models.BooleanField()
    # 로봇 활동 여부 (True : 현재 건물에 활동 가능한 로봇으로 설치되어 있는지, False : 사용 종료된 로봇)
    state = models.BooleanField()
    # 로봇이 위치한 층
    location_floor = models.IntegerField()
    # 로봇 보관 x 좌표
    start_x = models.IntegerField()
    # 로봇 보관 y 좌표
    start_y = models.IntegerField()