from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
import json

# Create your views here.
def calculate(request):
    file = request.FILES['fileInput']
    print("# 사용자가 등록한 파일의 이름: ", file)
    df = pd.read_excel(file, sheet_name="Sheet1", header=0)
    print(df.head())
    # grade별 value 리스트 만들기
    grade_dic = {}
    total_row_num = len(df.index)
    for i in range(total_row_num):
        data = df.loc[i, :]
        if not data.grade in grade_dic.keys():
            grade_dic[data.grade] = [data.value]
        else:
            grade_dic[data.grade].append(data.value)

    # print(grade_dic)
    # grade별 최솟값 최댓값 평균값 구하기
    grade_calculate_dic = {}
    for key in grade_dic.keys():
        grade_calculate_dic[key] = {}
        grade_calculate_dic[key]['min'] = min(grade_dic[key])
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
        grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key])) / len(grade_dic[key])

    # 결과 출력
    grade_list = list(grade_calculate_dic.keys())
    grade_list.sort()
    for key in grade_list:
        print("# grade: ", key)
        print("min:", grade_calculate_dic[key]['min'], end="")
        print("/ max:", grade_calculate_dic[key]['max'], end="")
        print("/ avg:", grade_calculate_dic[key]['avg'], end="\n\n")

    # 이메일 주소 도메인별 인원 구하기
    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i, :]
        email_domain = data['email'].split("@")[1]
        if not email_domain in email_domain_dic.keys():
            email_domain_dic[email_domain] = 1
        else:
            email_domain_dic[email_domain] += 1
    print("## EMAIL 도메인별 사용 인원")
    for key in email_domain_dic.keys():
        print("#", key, ": ", email_domain_dic[key], "명")

    grade_calculate_dic_to_session = {}
    for key in grade_list:
        grade_calculate_dic_to_session[int(key)] = {}
        grade_calculate_dic_to_session[int(key)]['max'] = float(grade_calculate_dic[key]['max'])
        grade_calculate_dic_to_session[int(key)]['avg'] = float(grade_calculate_dic[key]['avg'])
        grade_calculate_dic_to_session[int(key)]['min'] = float(grade_calculate_dic[key]['min'])
        
    request.session['grade_calculate_dic'] = grade_calculate_dic_to_session
    request.session['email_domain_dic'] = email_domain_dic

    # grade별 value 리스트 만들기
    grade_df = df.groupby('grade')['value'].agg(["min", "max", "mean"]).reset_index().rename(columns = {"mean" : "avg"})
    grade_df = grade_df.astype({'min' : 'int', 'max' : 'int', 'avg' : 'float'})
    print(grade_df.dtypes)
    grade_df = grade_df.style.hide(axis='index').set_table_attributes('class="table table-dark"')
    grade_calculate_pd_to_session = {'grade_df' : grade_df.to_html(justify='center')}
    request.session['grade_calculate_pd_dic'] = grade_calculate_pd_to_session

    # 이메일 주소 도메인별 인원 구하기
    df['domain'] = df['email'].apply(lambda x : x.split("@")[1])
    email_df = df.groupby('domain')['value'].agg("count").sort_values(ascending=False).reset_index()

    email_df = email_df.style.hide(axis='index').set_table_attributes('class="table table-dark"')
    
    email_calculate_pd_to_session = {'email_df' : email_df.to_html(justify='center')}
    request.session['email_calculate_pd_dic'] = email_calculate_pd_to_session


        # print(email_df)

    # return HttpResponse("calculate, calculate function!")
    return redirect('/result')