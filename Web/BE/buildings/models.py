from django.db import models
from accounts.models import Firestation

# 소방서 관리 건물
class Building(models.Model):
    # 건물 id
    building_id = models.CharField(max_length=15, unique=True)
    # 관할 소방서 FK
    firestation = models.ForeignKey(Firestation, on_delete=models.CASCADE, related_name='firestation')
    # 건물 이름
    building_name = models.TextField()
    # 건물 주소
    address = models.TextField()
    # 건물 최저 층수
    min_floor = models.IntegerField(default=1)
    # 건물 최고 층수
    max_floor = models.IntegerField(default=1)
    # 화재 상황 여부
    fire = models.BooleanField(default=False)
    # 경도
    longitude = models.TextField(null=True)
    # 위도
    latitude = models.TextField(null=True)


# 소방서 관리 건물 이미지
class Building_Floor(models.Model):
    # 건물_층 id
    building_floor = models.CharField(max_length=30, unique=True)
    # 건물 id FK
    building= models.ForeignKey(Building, on_delete=models.CASCADE, related_name='main_building')
    # 건물 층수
    floor = models.IntegerField()
    # 층수 상세 정보 (특징)
    etc = models.TextField(null=True)
    # 해당 층수 도면 이미지 경로
    img = models.ImageField(upload_to='building_image/')
    # 화재 상황 여부
    fire = models.BooleanField(default=False)


class Bicon(models.Model):
    # 비콘 맥 주소
    bicon_id = models.CharField(max_length=30, unique=True)
    # 건물_층 FK
    building_floor = models.ForeignKey(Building_Floor, on_delete=models.CASCADE)
    # 비콘 설치 x 좌표
    bicon_x = models.IntegerField()
    # 비콘 설치 y 좌표
    bicon_y = models.IntegerField()
    
class Sprinkler(models.Model):
    # 스프링클러 아이디
    sprinkler_id = models.CharField(max_length=40, unique=True)
    # 건물_층 FK
    building_floor = models.ForeignKey(Building_Floor, on_delete=models.CASCADE)
    # 스프링클러 설치 x 좌표
    sprinkler_x = models.IntegerField()
    # 스프링클러 설치 y 좌표
    sprinkler_y = models.IntegerField()