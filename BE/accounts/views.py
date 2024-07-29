from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
from faker import Faker
import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Firestation, Firefighter, Main
from .serializers import FirestationSerializer, FirefighterSerializer, MainSerializer

###################### SignUp ######################
@api_view(['GET','POST'])
def signup(request):
    # 회원가입 시 입력한 소방관 이름
    input_name = request.data.get('name')
    # 회원가입 시 입력한 소방관 고유번호
    input_pw = request.data.get('number')
    # 입력한 소방관이 소방관 Main DataSet에 있는지 확인
    exist_user = Main.objects.filter(name=input_name, number=input_pw)
    if exist_user:
        exist_user = exist_user[0]
        exist_firefighter = MainSerializer(exist_user)   # 소방관 정보
        station = exist_user.firestation
        exist_firestation = FirestationSerializer(station)   # 소방서 정보
        firestation_name = exist_firestation.data.get('firestation_name')
        duty = exist_firefighter.data.get('duty')   # 직무 정보

    if request.method == 'GET':
        # 회원가입 시 입력한 소방관 정보가 Main DataSet에 없다면
        if not exist_user:
            context = {'error':'소방관 정보를 찾을 수 없습니다.'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        # 회원가입 시 입력한 소방관 정보가 이미 DB에 있는 사용자라면
        if Firefighter.objects.filter(number=input_pw):
            context = {'error': '이미 가입된 사용자입니다.'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        # 회원가입이 가능한 소방관 정보가 입력되었다면 
        context = {
            'data':{
                'name':input_name,
                'number':input_pw,
                'firestation': firestation_name,
                'duty': duty
            },
            'massage':'본인이 맞는지 확인해주십시오.'
        }
        return Response(context, status=status.HTTP_200_OK)
    # 앞서 massage에 본인이 맞는지 확인해주십시오 라는 메시지에 확인 버튼을 누르면
    if request.method == 'POST':
        save_user = {
            'username': input_name,
            'password': make_password(input_pw),
            'number':input_pw,
            'duty':duty
        }
        # 소방관 DB에 정보 저장 (회원가입)
        serializer = FirefighterSerializer(data = save_user)
        if serializer.is_valid(raise_exception=True):
            firestation_data = Firestation.objects.get(firestation_name = firestation_name)
            serializer.save(firestation = firestation_data)
            context = {
                'massage':f"{input_name}님 가입이 완료되었습니다."
                }
    return Response(context, status=status.HTTP_201_CREATED)


###################### Login ######################
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # 기본 ObtainAuthToken의 post 메서드를 호출하여 인증 처리
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        
        # 반환된 토큰을 이용하여 사용자 객체를 가져옴
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        # 사용자 직무 정보 가져오기
        duty_ = user.duty
        context = {
            'key': token.key,
            'duty': duty_
        }

        return Response(context, status=status.HTTP_200_OK)


###################### Fake Data ######################
API_KEY = settings.ADDRESS_API_KEY
BASE_URL = 'https://dapi.kakao.com/v2/local/search'

# fake firestation 생성
@api_view(['GET'])
def fake_firestation(request):
    message = []
    headers = {
        'Authorization': f'KakaoAK {API_KEY}'
    }
    params = {
        'query': '소방서',
        # 멀티캠퍼스 역삼 위치
        'x': 127.03959901118846,
        'y': 37.50128969904896,
        # 반경 20km내 검색
        'radius': 20000
    }
    response = requests.get(BASE_URL+'/keyword.json', headers=headers, params=params).json()
    for fire_station in response.get('documents'):
        firestation_id = fire_station.get('id')
        firestation_name = fire_station.get('place_name')
        firestation_address = fire_station.get('road_address_name')
        firestation_x = fire_station.get('x'),
        firestation_y = fire_station.get('y')
        
        if Firestation.objects.filter(firestation_id=firestation_id).exists():
            continue
        save_firestation = {
            'firestation_id':firestation_id,
            'firestation_name':firestation_name,
            'firestation_address':firestation_address,
            'firestation_x':firestation_x[0],
            'firestation_y':firestation_y,
        }
        serializer = FirestationSerializer(data=save_firestation)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    message.append({
        'message':'FireStation Data Save-Success',
        'data': save_firestation
    })
    
    return Response(message, status=status.HTTP_201_CREATED)
    

# fake firefighter 생성
@api_view(['GET'])
def fake_firefighter(request):
    msg = []
    name = ['이지예','주호성','윤경서','송창용','최유정','이유단']
    number = ['1140919','1146727','1140868','1143307','1147918','1147448']
    duty = [1, 0]*3
    firestation_list = ['역삼119안전센터','역삼119안전센터','서초119안전센터','서초119안전센터','강남소방서','강남소방서']
    for n, num, duty_, firestation in zip(name, number, duty, firestation_list):
        save_user = {
            'name': n,
            'number': num,
            'duty': duty_,
        }
        if Main.objects.filter(name=n).exists():
            continue
        serializer = MainSerializer(data = save_user)
        if serializer.is_valid(raise_exception=True):
            firestation_data = Firestation.objects.get(firestation_name = firestation)
            serializer.save(firestation = firestation_data)
            msg.append(f"{n}성공")
    return Response(msg, status=status.HTTP_201_CREATED)