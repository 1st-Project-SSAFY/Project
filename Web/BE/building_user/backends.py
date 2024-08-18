from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import BuildingManager

class BuildingManagerBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # BuildingManager 모델에서 username으로 사용자 검색
            user = BuildingManager.objects.get(username=username)
            # 저장된 비밀번호와 입력된 비밀번호 비교
            if check_password(password, user.password):
                return user
        except BuildingManager.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return BuildingManager.objects.get(pk=user_id)
        except BuildingManager.DoesNotExist:
            return None