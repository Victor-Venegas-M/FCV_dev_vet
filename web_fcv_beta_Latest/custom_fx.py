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

def getDashboardData():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_dashboard/dashboard'
    resp = requests.get(uri)
    resp_json = resp.json()
    data = resp_json['items'][0]
    return data

def getAtenciones():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_atenciones/atenciones'
    response = requests.get(uri)
    json_data = response.json()
    data = json_data['items']
    return data

def newReceta(id_atencion, prescripcion):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_recetas/receta'
    data = {
        'id_atencion': int(id_atencion),
        'prescripcion': prescripcion
    }
    return requests.post(uri, json=data)

def getRecetas():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_recetas/recetas'
    response = requests.get(uri)
    json_data = response.json()
    data = json_data['items']
    return data

def getRecetaById(id_receta):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_recetas/receta?id_receta='+str(id_receta)
    response = requests.get(uri)
    json_data = response.json()
    data = json_data['items'][0]
    return data

def getVacunaById(id_vacuna):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunas/vacuna?id_vacuna='+str(id_vacuna)
    response = requests.get(uri)
    json_data = response.json()
    data = json_data['items'][0]
    return data

def getEspecies():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_especies/especies'
    response = requests.get(uri)
    json_data = response.json()
    especies = json_data['items']
    return especies

def getTutores():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutores'
    response = requests.get(uri)
    json_data = response.json()
    tutores = json_data['items']
    return tutores

def getRacesByEspId(id_especie):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_razas/races_by_esp?id_especie='+str(id_especie)
    response = requests.get(uri)
    json_data = response.json()
    razas = json_data['items']
    return razas

def getPacienteById(id_paciente):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/paciente?id_paciente='+str(id_paciente)
    response = requests.get(uri)
    json_data = response.json()
    if len(json_data['items']) >= 1:
        paciente = json_data['items'][0]
    else:
        paciente = {}
    return paciente

def getHistorialPaciente(id_paciente):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_historial/historial_clinico?id_paciente='+str(id_paciente)
    response = requests.get(uri)
    json_data = response.json()
    if len(json_data['items']) >= 1:
        historial = json_data['items']
    else:
        historial = {}
    return historial

def getVacunasByPaciente(id_paciente):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_historial/vacunas?id_paciente='+str(id_paciente)
    response = requests.get(uri)
    json_data = response.json()
    if len(json_data['items']) >= 1:
        vacunas = json_data['items']
    else:
        vacunas = {}
    return vacunas

def getAtenciones():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_atenciones/atenciones'
    response = requests.get(uri)
    json_data = response.json()
    atenciones = json_data['items']
    return atenciones

def getPacientes():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/pacientes'
    response = requests.get(uri)
    json_data = response.json()
    pacientes = json_data['items']
    return pacientes

def getServicios():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_servicios/servicios'
    response = requests.get(uri)
    json_data = response.json()
    servicios = json_data['items']
    return servicios

def getMedicos():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medicos'
    response = requests.get(uri)
    json_data = response.json()
    medicos = json_data['items']
    return medicos

def getAtencionById(id_atencion):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_atenciones/atencion?id_atencion='+str(id_atencion)
    response = requests.get(uri)
    json_data = response.json()
    detalle = json_data['items'][0]
    return detalle

def getUserLoginData(usuario, user_pass):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api/login?usuario='+str(usuario)+'&pass='+str(user_pass)
    response = requests.get(uri)
    json_data = response.json()
    user = json_data['items'][0]
    return user

def getVacunas():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunas/vacunas'
    response = requests.get(uri)
    json_data = response.json()
    vaunas = json_data['items']
    return vaunas

def newVacunacion(id_paciente, id_vacuna, serie):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunaciones/vacunacion'
    data = {
        'id_vacuna': int(id_vacuna),
        'id_paciente': int(id_paciente),
        'serie': serie
    }
    response = requests.post(uri, json=data)
    return response

def getVacunaciones():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunaciones/vacunaciones'
    response = requests.get(uri)
    json_data = response.json()
    vacunaciones = json_data['items']
    return vacunaciones

def getAccount(usuario, passwd):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api/login?usuario='+usuario+'&pass='+passwd
    response = requests.get(uri)
    json_data = response.json()
    if 'items' in json_data and len(json_data['items']) > 0:
        print('hay datos de usuario')
        data = json_data['items'][0]
    else:
        print('no hay datos de usuario')
        data = {}

    return data

def getClinicas():
    clinica_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinicas'
    api_response = requests.get(clinica_api_url)
    json_data = api_response.json()
    clinicas = json_data['items']
    return clinicas

def getAgendamientos():
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_agendamiento/agendamientos'
    response = requests.get(uri)
    json_data = response.json()
    data = json_data['items']
    return data