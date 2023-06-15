from django.test import TestCase
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import TruncMonth
from datetime import datetime, date
from . import views
import hashlib
import requests
import json

# Create your tests here.
# def getEspecies():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_especies/especies'
#     response = requests.get(uri)
#     json_data = response.json()
#     especies = json_data['items']
#     return especies

# def getTutores():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutores'
#     response = requests.get(uri)
#     json_data = response.json()
#     tutores = json_data['items']
#     return tutores

# def getRacesByEspId(id_especie):
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_razas/races_by_esp?id_especie='+str(id_especie)
#     response = requests.get(uri)
#     json_data = response.json()
#     razas = json_data['items']
#     return razas

# def getPacienteById(id_paciente):
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/paciente?id_paciente='+str(id_paciente)
#     response = requests.get(uri)
#     json_data = response.json()
#     paciente = json_data['items'][0]
#     return paciente

# def getAtenciones():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_atenciones/atenciones'
#     response = requests.get(uri)
#     json_data = response.json()
#     atenciones = json_data['items']
#     return atenciones

# def getPacientes():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/pacientes'
#     response = requests.get(uri)
#     json_data = response.json()
#     pacientes = json_data['items']
#     return pacientes

# def getServicios():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_servicios/servicios'
#     response = requests.get(uri)
#     json_data = response.json()
#     servicios = json_data['items']
#     return servicios

# def getMedicos():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medicos'
#     response = requests.get(uri)
#     json_data = response.json()
#     medicos = json_data['items']
#     return medicos

# def getAtencionById(id_atencion):
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_atenciones/atencion?id_atencion='+str(id_atencion)
#     response = requests.get(uri)
#     json_data = response.json()
#     detalle = json_data['items'][0]
#     return detalle

# def getUserLoginData(usuario, user_pass):
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api/login?usuario='+str(usuario)+'&pass='+str(user_pass)
#     response = requests.get(uri)
#     json_data = response.json()
#     user = json_data['items'][0]
#     return user

# def getVacunas():
#     uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunas/vacunas'
#     response = requests.get(uri)
#     json_data = response.json()
#     vaunas = json_data['items']
#     return vaunas

