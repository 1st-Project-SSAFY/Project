from django.db import models
from django.contrib.auth.models import AbstractUser

# 소방서
class Firestation(models.Model):
    # 소방서 id
    firestation_id = models.CharField(max_length=15, unique=True)
    # 소방서 이름
    firestation_name = models.CharField(max_length=20)
    # 소방서 주소
    firestation_address = models.TextField()
    # 소방서 x 좌표 (경도)
    firestation_x = models.FloatField()
    # 소방서 y 좌표 (위도)
    firestation_y = models.FloatField()


# 소방관
# id, username = 소방관 이름
# password = 소방관 고유넘버
class Firefighter(AbstractUser):
    # 소방관 고유넘버
    number = models.CharField(max_length=10, unique=True)
    # 소속 소방서 FK
    firestation = models.ForeignKey(Firestation, on_delete=models.CASCADE, related_name='workplace')
    DUTY = [
        (0, '현장직'),
        (1, '관리직')
    ]
    # 소방관 직무
    duty = models.IntegerField(choices=DUTY)
    

# Main 소방청 Data
class Main(models.Model):
    # 소방관 이름
    name = models.CharField(max_length=10)
    # 소방관 고유넘버
    number = models.CharField(max_length=10, unique=True)
    # 소속 소방서 FK
    firestation = models.ForeignKey(Firestation, on_delete=models.CASCADE)
    DUTY = [
        (0, '현장직'),
        (1, '관리직')
    ]
    # 소방관 직무
    duty = models.IntegerField(choices=DUTY)