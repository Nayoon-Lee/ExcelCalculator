from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    # 로그인된 사용자만 접근
    # 조건문 : 사용자의 정보가 세션에 존재하면 메인 화면으로 출력
    #          만약 사용자 정보가 세션에 없다면 로그인 화면으로 출력
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html') # 사용자의 세션 정보가 들어있는 상태의 메인 화면
    else:
        return redirect('main_signin')

    # return render(request, 'main/index.html') # 그냥 아무 정보 없는 메인 화면

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print(request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()

    # print("사용자 정보 저장 완료됨!")

    # 인증코드
    code = randint(1000, 9000)
    print("인증코드 생성--------", code) # 서버가 보낸 코드, 쿠키와 세션
    
    response = redirect('main_verifyCode') # 응답을 객체로 저장한다.
    response.set_cookie('code', code) # 인증코드
    response.set_cookie('user_id', user.id)
    print("응답 객체 완성--------", response)

    # 이메일 발송 함수 호출
    send_result = send(email, code)
    if send_result:
        print("Main > views.py > 이메일 발송 중")
        return response
    else:
        return HttpResponse("이메일 발송에 실패했습니다.")

    return response

def signin(request):
    return render(request, 'main/signin.html')

def login(request):
    # 로그인된 사용자만 이용할 수 있도록 구현
    # 이 때, 현재 사용자가 로그인된 사용자인지 판단하기 위해 FROM(verify함ㅅ 에서 만든 세션)
    # 세션 처리 진행.
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']
    user = User.objects.get(user_email = loginEmail)
    if user.user_password == loginPW: # 로그인 성공하면
        request.session['user_name'] = user.user_name # 사용자가 회원가입 시 입력한 정보
        request.session['user_email'] = user.user_email # 사용자가 회원가입 시 입력한 정보
        return redirect('main_index')
    else: # 로그인 실패하면
        return redirect('main_loginFail')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    # 사용자가 입력한 code 값을 받아야 함
    user_code = request.POST['verifyCode']
    # 쿠키에 저장된 code 값을 가져와서 일치시키야함. (join 함수 확인)
    cookie_code = request.COOKIES.get('code')
    print("코드 확인: ", user_code, cookie_code)
    
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id')) # select from where id = cookide_id; 해당되는 데이터만 가져오겠다는 의미
        user.user_validate = 1 # True = 1, False = 0
        user.save()

        print("DB에 user_validate 업데이트-----------")

        response = redirect('main_index')
        
        # 저장되어 있는 쿠키 삭제
        response.delete_cookie('code') 
        response.delete_cookie('user_id')
        # response.set_cookie('user', user)

        '''
        response와 request의 차이
        response는 main_index에 응답을 주는 것, 즉 index 페이지로 가시오.
        request는 로그인 화면 구현하는데에 요청을 줌.
        '''

        # 사용자 정보를 세션에 저장
        request.session['user_name'] = user.user_name # 로그인 화면 구현
        request.session['user_email'] = user.user_email # 로그인 화면 구현
        return response
    else:
        return redirect('main_verifyCode')


    # return redirect('main_index') # 인증이 완료되면 메인 화면을 보내달라는 의미

def result(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/result.html') # 사용자의 세션 정보가 들어있는 상태의 메인 화면, 엑셜 결과 페이지까지 세션 유지
    else:
        return redirect('main_signin')

def logout(request):
    # 로그아웃의 개념 : 세션 종료, 즉 세션을 삭제
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')