import json
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponse
from api.models import Company, Vacancy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from api.serializers import  CompanySerializer,VacancySerializer
@csrf_exempt
def companies_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer=CompanySerializer(companies,many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        request_body = json.loads(request.body)
        serializer=CompanySerializer(data=request_body)
        if serializer.is_valid():
            serializer.save()
            return  JsonResponse(serializer.data)
        return JsonResponse({'error': serializer.errors})
@csrf_exempt
def vacancy_list(request):
    if request.method == 'GET':
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        request_body = json.loads(request.body)
        serializer = VacancySerializer(data=request_body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': serializer.errors})
@csrf_exempt
def company_detail(request,company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist as e:
        return JsonResponse({'error': 'message does not exits'})
    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        request_body = json.loads(request.body)
        serializer= CompanySerializer(instance=company,data=request_body)
        if serializer.is_valid():
            serializer.save()
            return  JsonResponse(serializer.data)
        return JsonResponse({'error': serializer.errors})
    elif request.method == 'DELETE':
        company.delete()
        return JsonResponse({'deleted': True})
@csrf_exempt
def vacancy_detail(request,vacancy_id):
    try:
        vacancy=Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist as e:
        return JsonResponse({'error':'message does not exits'})
    if request.method == 'GET':
        serializer = VacancySerializer(vacancy)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        request_body = json.loads(request.body)
        serializer = VacancySerializer(instance=vacancy, data=request_body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': serializer.errors})
    elif request.method == 'DELETE':
        vacancy.delete()
        return JsonResponse({'deleted': True})