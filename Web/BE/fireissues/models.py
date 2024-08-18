from django.db import models
from buildings.models import Building, Sprinkler
from robots.models import Robot

# 화재 발생 사건
class Fire_Issue(models.Model):
    # 화재 발생 건물 FK
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='fire_building')
    # 화재 발생 일시
    fire_dt = models.DateTimeField(auto_now_add=True)
    # 화재 진압 일시
    end_dt = models.DateTimeField(null=True)
    # 화재 규모 (1~10)
    fire_scale = models.IntegerField(null=True)
    # 화재 현장 및 화재 발생 상세 설명
    detail = models.TextField(null=True)
    # 현장 녹화 영상
    video = models.TextField(null=True)
    # 화재 발생 층
    fire_floor = models.IntegerField()
    # 화재 발생 sprinkler
    sprinkler = models.ForeignKey(Sprinkler, on_delete=models.CASCADE, related_name="fire_sprinkler")

    
# 화재 발생 로그
class Fire_Logs(models.Model):
    # 로봇 아이디 FK
    robot_id = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name='move_robot')
    # 화재 발생 번호 FK
    fire_id = models.ForeignKey(Fire_Issue, on_delete=models.CASCADE, related_name='fireissue')
    # 로봇 상태 통신 일시
    state_dt = models.DateTimeField(auto_now_add=True)
    # 로봇 배터리 잔량
    battery = models.IntegerField()
    # 대피 안내 용액 잔량
    guide_liquid = models.IntegerField()
    # 임무 상황
    MISSION = [
        (0, '대기'),
        (1, '이동중'),
        (2, '완료'),
        (3, '실패'),
    ]
    mission = models.IntegerField(choices=MISSION)
    # 로봇 현재 위치 x 좌표
    location_x = models.IntegerField()
    # 로봇 현재 위치 y 좌표
    location_y = models.IntegerField()
    # 장애물 발견 시 장애물 위치 x 좌표
    block_x = models.IntegerField(null=True)
    # 장애물 발견 시 장애물 위치 y 좌표
    block_y = models.IntegerField(null=True)