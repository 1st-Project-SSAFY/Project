from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from buildings.models import Building

# 건물 관리자 Data
class BuildingManagerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class BuildingManager(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BuildingManagerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
import uuid
class BuildingManagerToken(models.Model):
    user = models.OneToOneField(BuildingManager, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:  # key 필드가 비어 있을 경우
            self.key = uuid.uuid4().hex  # 고유한 UUID 할당
        super().save(*args, **kwargs)
