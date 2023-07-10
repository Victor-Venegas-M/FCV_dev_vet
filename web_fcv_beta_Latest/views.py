from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import TruncMonth
from datetime import datetime, date
import hashlib
import requests
import json
from . import tests
from . import custom_fx

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

def showCookies(request):
    return render(request, "debug/cookies.html")

def index(request):
    data = {
        'res': custom_fx.getDashboardData()
    }
    print(data)
    return render(request, "index.html", data)



def login(request):
    return render(request, "login.html")

@csrf_exempt
def check(request):
    if request.method == 'POST':
        if request.POST.get('usuario') and request.POST.get('user_pass'):
            user = request.POST.get('usuario')
            upass = request.POST.get('user_pass')
            user_data = custom_fx.getAccount(user, upass)
            data = {
                'user': user_data
            }
            
            print(data)
            return render(request, "check.html", data)
        else:
            return redirect(login)
    else:
        return redirect(login)


def clinicas_list(request):
    # Para las vistas de lista, simplemente (teniendo creado el modulo API) lo consultamos de la siguiente
    # manera:
    # Primero definimos la url de la api que nos devolvera el json generado a partir de la consulta SELECT
    clinica_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinicas'
    # Creamos una variable que almacenara la respuesta de la consulta a la API
    api_response = requests.get(clinica_api_url)
    # en una nueva variable transformamos la respuesta anterior a formato json (variable_anterior.json())
    json_data = api_response.json()
    # Creamos un arreglo de objetos de tipo clinica, a partir del subconjunto 'items' del conjunto json anterior.
    obj_clinicas = json_data['items']
    # Transformamos este arreglo a una matriz unidimensional (otro array no mas, pero simple) para el renderizado de la vista html
    data = { 'clinicas': obj_clinicas}
    # Enviamos esta matriz como parametro para el renderizado HTML
    return render(request, 'clinicas/listar.html', data)

def clinicas_detalle(request, id_clinica):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinica?id_clinica=' + str(id_clinica)
    response = requests.get(uri)
    json_data = response.json()
    clinica = json_data['items'][0]
    return render(request, 'clinicas/ver.html', {'clinica':clinica})

@csrf_exempt
def clinicas_agregar(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('direccion') and request.POST.get('comuna') and request.POST.get('telefono'):
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            cut_comuna = request.POST.get('comuna')
            telefono = request.POST.get('telefono')

            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinica'
            data = {
                'nombre': nombre,
                'direccion': direccion,
                'cut_comuna': cut_comuna,
                'telefono': telefono
            }

            response = requests.post(uri, json=data)

            if response.status_code == 200:
                return redirect(clinicas_list)
            else:
                print(response.status_code)
                regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
                regs_api_resp = requests.get(regs_api_url)
                regs_json_data = regs_api_resp.json()
                regiones = regs_json_data['items']
                data = { 'regiones':regiones }
                return render(request, 'clinicas/agregar.html', data)
    else:
        regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
        regs_api_resp = requests.get(regs_api_url)
        regs_json_data = regs_api_resp.json()
        regiones = regs_json_data['items']
        data = { 'regiones':regiones }
        return render(request, 'clinicas/agregar.html', data)

@csrf_exempt
def clinicas_modificar(request, id_clinica):
    if request.method == 'POST':
        
        if  request.POST.get('nombre') and request.POST.get('direccion') and request.POST.get('comuna') and request.POST.get('telefono'):

            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            cut_comuna = request.POST.get('comuna')
            telefono = request.POST.get('telefono')
            
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinica'
            datos = {
                'id_clinica': id_clinica,
                'nombre': nombre,
                'direccion': direccion,
                'cut_comuna': cut_comuna,
                'telefono': telefono
            }
            headers = {'Content-Type': 'application/json'}
            
            response = requests.put(uri, headers=headers, data=json.dumps(datos))
            if response.ok:
                # return response.json()
                print('exito')
                return redirect(clinicas_list)
            else:
                print('error :C')
                return {'error': 'No se pudo actualizar el empleado'}
        else:
            print('no paso el form')

        return redirect(clinicas_list)
    else:
        uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinica?id_clinica=' + str(id_clinica)
        response = requests.get(uri)
        json_data = response.json()
        clinica = json_data['items'][0]

        regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
        regs_api_resp = requests.get(regs_api_url)
        regs_json_data = regs_api_resp.json()
        regiones = regs_json_data['items']

        data = { 'clinica': clinica, 'regiones':regiones}
        return render(request, 'clinicas/editar.html', data)




def tutores_listar(request):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutores'
    response = requests.get(uri)
    json_data = response.json()
    objetos = json_data['items']
    data = { 'tutores': objetos }
    return render(request, 'tutores/listar.html', data)

def tutores_detalle(request, id_tutor):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutor?id_tutor=' + str(id_tutor)
    response = requests.get(uri)
    json_data = response.json()
    tutor = json_data['items'][0]
    data = { 'tutor':tutor }
    return render(request, 'tutores/ver.html', data)

@csrf_exempt
def tutores_agregar(request):
    # Preguntamos primero si la llamada a la vista
    # que contiene el formulario es POST (es decir, si es que efectivamente ya rellenamos el formulario
    # y debemos enviar los datos a la API para ser ingresados en la base de datos)
    if request.method == 'POST':

        # Preguntamos si el formulario fue completado con los campos requeridos
        if request.POST.get('comuna') and request.POST.get('pnombre') and request.POST.get('snombre') and request.POST.get('appaterno') and request.POST.get('apmaterno') and request.POST.get('email') and request.POST.get('telefono') and request.POST.get('direccion'):
            
            # Si los datos son correctos, los almacenamos en variables
            cut_comuna = request.POST.get('comuna') 
            pnombre = request.POST.get('pnombre') 
            snombre = request.POST.get('snombre') 
            appaterno = request.POST.get('appaterno') 
            apmaterno = request.POST.get('apmaterno') 
            email = request.POST.get('email') 
            telefono = request.POST.get('telefono') 
            direccion = request.POST.get('direccion')
            
            # Definimos la URL del metodo POST correspondiente
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutor'
            
            # Creamos un arreglo con los datos que irán a la API
            data = {
                'cut_comuna': cut_comuna,
                'pnombre': pnombre,
                'snombre': snombre,
                'appaterno': appaterno,
                'apmaterno': apmaterno,
                'email': email,
                'telefono': telefono,
                'direccion': direccion
            }
            
            # Definimos una variable para ejecutar la solicitud POST a la API
            # y almacenará la respuesta del servidor
            response = requests.post(uri, json=data)

            # Si la respuesta del servidor es favorable (codigo 200), redireccionamos a la lista de tutores
            if response.status_code == 200:
                 print('exito')
                 return redirect(tutores_listar)
            
            # Si hubo un error se muestra en la consola del server y se salta a la redirección de la lista de tutores
            else:
                print(response.status_code)

        # Si el formulario no tenía todos los campos necesarios, informa por consola
        # y salta a la redirección de lista de tutores
        else:
            print('no paso el form')
        

        # Redirección a lista haya o no haya error
        return redirect(tutores_listar)
    
    # Si la llamada a la vista NO es POST, es decir, simplemente ingresamos al formulario
    # para llenar los campos 
    else:
        # Me traigo las regiones para el caso de formularios con dirección
        regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
        regs_api_resp = requests.get(regs_api_url)
        regs_json_data = regs_api_resp.json()
        regiones = regs_json_data['items']
        # Guardo las regiones en un arreglo
        data = { 'regiones': regiones }
        # Llamo a la vista de formulario pasandole las regiones dentro del arreglo "data"
        return render(request, 'tutores/agregar.html', data)

@csrf_exempt
def tutores_modificar(request, id_tutor):
    if request.method == 'POST':
        if request.POST.get('comuna') and request.POST.get('pnombre') and request.POST.get('snombre') and request.POST.get('appaterno') and request.POST.get('apmaterno') and request.POST.get('direccion') and request.POST.get('telefono') and request.POST.get('email'):
            tutorId = id_tutor
            cut_comuna = request.POST.get('comuna')
            pnombre = request.POST.get('pnombre')
            snombre = request.POST.get('snombre')
            appaterno = request.POST.get('appaterno')
            apmaterno = request.POST.get('apmaterno')
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            email = request.POST.get('email')
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutor'

            data = {
                'id_tutor': tutorId,
                'cut_comuna': cut_comuna,
                'pnombre': pnombre,
                'snombre': snombre,
                'appaterno': appaterno,
                'apmaterno': apmaterno,
                'direccion': direccion,
                'telefono': telefono,
                'email': email
            }

            headers = {'Content-Type': 'application/json'}
            
            response = requests.put(uri, headers=headers, data=json.dumps(data))
            if response.ok:
                return redirect(tutores_listar)

    else:
        uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_tutores/tutor?id_tutor=' + str(id_tutor)
        response = requests.get(uri)
        json_data = response.json()
        tutor = json_data['items'][0]

        regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
        regs_api_resp = requests.get(regs_api_url)
        regs_json_data = regs_api_resp.json()
        regiones = regs_json_data['items']

        data = { 
            'tutor':tutor,
            'regiones': regiones
            }
        
        return render(request, 'tutores/editar.html', data)



def pacientes_listar(request):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/pacientes'
    resp = requests.get(uri)
    json_data = resp.json()
    pacientes = json_data['items']
    data = { 'pacientes': pacientes }
    return render(request, 'pacientes/listar.html', data)

@csrf_exempt
def pacientes_agregar(request, id_tutor):
    if request.method == 'POST':
        
        if request.POST.get('nombre') and request.POST.get('id_tutor') and request.POST.get('id_raza') and request.POST.get('f_nac'):
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/paciente'
            
            id_tutor = request.POST.get('id_tutor')
            id_raza = request.POST.get('id_raza')
            nombre = request.POST.get('nombre')
            f_nac = str(request.POST.get('f_nac'))

            data = {
                'id_tutor':id_tutor,
                'id_raza':id_raza,
                'nombre':nombre,
                'f_nac':f_nac
            }
            
            response = requests.post(uri, json=data)

            if response.status_code == 200:
                 print('exito')
                 return redirect(pacientes_listar)

            return redirect(pacientes_listar)
        
        else:
            return redirect(pacientes_listar)
    else:
        tutores = custom_fx.getTutores()
        especies = custom_fx.getEspecies()
        data = {
            'especies': especies,
            'tutores': tutores,
            'id_tutor': id_tutor
        }
        return render(request, 'pacientes/agregar.html', data)

def pacientes_detalle(request, id_paciente):
    data = { 
        'paciente': custom_fx.getPacienteById(id_paciente),
        'atenciones': custom_fx.getHistorialPaciente(id_paciente),
        'vacunas': custom_fx.getVacunasByPaciente(id_paciente)
        }
    
    return render(request, 'pacientes/ver.html', data)

@csrf_exempt
def pacientes_modificar(request, id_paciente):
    if request.method == 'POST':

        if request.POST.get('nombre') and request.POST.get('id_tutor') and request.POST.get('id_raza') and request.POST.get('f_nac'):
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/paciente'
            id_tutor = request.POST.get('id_tutor')
            id_raza = request.POST.get('id_raza')
            nombre = request.POST.get('nombre')
            f_nac = str(request.POST.get('f_nac'))

            data = {
                'id_tutor':id_tutor,
                'id_raza':id_raza,
                'nombre':nombre,
                'f_nac':f_nac,
                'id_paciente': id_paciente
            }
            headers = {'Content-Type': 'application/json'}
            
            response = requests.put(uri, headers=headers, data=json.dumps(data))
            if response.ok:
                return redirect(pacientes_listar)
            
            return redirect(pacientes_listar)
        
        return redirect(pacientes_listar)
    else:
        uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/paciente?id_paciente='+str(id_paciente)
        resp = requests.get(uri)
        json_data = resp.json()
        paciente = json_data['items'][0]

        especies = custom_fx.getEspecies()
        tutores = custom_fx.getTutores()
        razas = custom_fx.getRacesByEspId(paciente['id_especie'])
        f_nac_texto = paciente['f_nac']
        f_nac_object = datetime.strptime(f_nac_texto, '%d/%m/%Y').date()
        f_nac_formatted = f_nac_object.strftime('%Y-%m-%d')

        data = {
            'paciente': paciente,
            'fecha': f_nac_formatted,
            'especies': especies,
            'razas': razas,
            'tutores': tutores
        }

        return render(request, 'pacientes/modificar.html', data)

def atenciones_listar(request):
    data = { 'atenciones': custom_fx.getAtenciones() }
    return render(request, 'atencion/listar.html', data)

@csrf_exempt
def atenciones_agregar(request, id_pte):
    if request.method == 'POST':
        if request.POST.get('id_servicio') and request.POST.get('id_medico') and request.POST.get('id_paciente') and request.POST.get('anamnesis') and request.POST.get('frec_card') and request.POST.get('frec_resp') and request.POST.get('temp') and request.POST.get('peso') and request.POST.get('tlp') and request.POST.get('pc') and request.POST.get('condicion_corporal') and request.POST.get('porc_hidratacion') and request.POST.get('lista_problemas') and request.POST.get('obs'):
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_atenciones/atencion'
            id_servicio = request.POST.get('id_servicio')
            id_medico = request.POST.get('id_medico')
            id_paciente = request.POST.get('id_paciente')
            anamnesis = request.POST.get('anamnesis')
            frec_card = request.POST.get('frec_card')
            frec_resp = request.POST.get('frec_resp')
            temp = request.POST.get('temp')
            peso = request.POST.get('peso')
            tlp = request.POST.get('tlp')
            pc = request.POST.get('pc')
            condicion_corporal = request.POST.get('condicion_corporal')
            porc_hidratacion = request.POST.get('porc_hidratacion')
            lista_problemas = request.POST.get('lista_problemas')
            obs = request.POST.get('obs')

            data = {
                'id_servicio': id_servicio,
                'id_medico': id_medico,
                'id_paciente': id_paciente,
                'anamnesis': anamnesis,
                'frec_card': frec_card,
                'frec_resp': frec_resp,
                'temp': temp,
                'peso': peso,
                'tlp': tlp,
                'pc': pc,
                'condicion_corporal': condicion_corporal,
                'porc_hidratacion': porc_hidratacion,
                'lista_problemas': lista_problemas,
                'obs': obs
                }
            
            response = requests.post(uri, json=data)

            if response.status_code == 200:
                print('Exito')
            else:
                print('Algo no funciono xD')

        return redirect(atenciones_listar)
    else:
        data = {
            'pacientes': custom_fx.getPacientes(),
            'servicios': custom_fx.getServicios(),
            'medicos': custom_fx.getMedicos(),
            'id_paciente': id_pte
        }
        return render(request, 'atencion/agregar.html', data)

def atenciones_modificar(request, id_atencion):
    return render(request, 'atencion/editar.html')

def atenciones_detalle(request, id_atencion):
    data = {
        'detalle': custom_fx.getAtencionById(id_atencion)
    }
    return render(request, 'atencion/ver.html', data)

def vacunaciones_listar(request):
    data = {
        'vacunaciones': custom_fx.getVacunaciones()
    }
    return render(request, 'vacunacion/listar.html', data)

@csrf_exempt
def vacunaciones_agregar(request, id_paciente):
    if request.method == 'POST':
        print('entro post')
        if request.POST.get('id_paciente') and request.POST.get('id_vacuna') and request.POST.get('serie'):
            print('paso datos en el form')
            id_paciente = request.POST.get('id_paciente')
            id_vacuna = request.POST.get('id_vacuna')
            serie = request.POST.get('serie')
            print(id_paciente+' '+id_vacuna+' '+serie)
            response = custom_fx.newVacunacion(id_paciente, id_vacuna, serie)
            print(response.raise_for_status)
            if response.status_code == 200:
                print('exito')
                return redirect(vacunaciones_listar)
            else:
                print(response.raise_for_status)
                return redirect(vacunaciones_listar)
            
        return redirect(vacunaciones_listar)
    else:
        data = {
            'pacientes': custom_fx.getPacientes(),
            'especies': custom_fx.getEspecies(),
            'paciente': custom_fx.getPacienteById(id_paciente),
            'vacunas': custom_fx.getVacunas()
        }
        return render(request, 'vacunacion/agregar.html', data)

def vacunaciones_modificar(request,id_vacunacion):
    return render(request, 'vacunacion/editar.html')

def vacunaciones_detalle(request,id_vacunacion):
    return render(request, 'vacunacion/ver.html')


@csrf_exempt
def veterinarios_agregar(request, id_clinica):
    if request.method == 'POST':
        if request.POST.get('comuna') and request.POST.get('id_clinica') and request.POST.get('pnombre') and request.POST.get('snombre') and request.POST.get('appaterno') and request.POST.get('apmaterno') and request.POST.get('telefono') and request.POST.get('email') and request.POST.get('direccion'):
            cut_comuna = request.POST.get('comuna')
            id_clinica = request.POST.get('id_clinica')
            pnombre = request.POST.get('pnombre')
            snombre = request.POST.get('snombre')
            appaterno = request.POST.get('appaterno')
            apmaterno = request.POST.get('apmaterno')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            
            id_rol = request.POST.get('rol')
            username = request.POST.get('username')
            userpass = request.POST.get('passwd')
            key = str(username)+str(userpass)
            api_key = hashlib.md5(key.encode('utf-8')).hexdigest()

            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medico'
            data = {
                'cut_comuna': cut_comuna,
                'id_clinica': id_clinica,
                'pnombre': pnombre,
                'snombre': snombre,
                'appaterno': appaterno,
                'apmaterno': apmaterno,
                'email': email,
                'telefono': telefono,
                'direccion': direccion,
                'id_rol': id_rol,
                'usuario': username,
                'passwd': userpass,
                'api_key': api_key
            }
            print(data)
            response = requests.post(uri, json=data)

            if response.status_code == 200:
                return redirect(veterinarios_listar)
            else:
                print(response.status_code)
                print(response.reason)

        return redirect(veterinarios_listar)
    else:
        uri_clinicas = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinicas'
        response = requests.get(uri_clinicas)
        json_data = response.json()
        clinicas = json_data['items']

        regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
        regs_api_resp = requests.get(regs_api_url)
        regs_json_data = regs_api_resp.json()
        regiones = regs_json_data['items']

        roles_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/roles/roles'
        roles_api_resp = requests.get(roles_api_url)
        roles_json_data = roles_api_resp.json()
        roles = roles_json_data['items']

        data = { 
            'id_clinica': id_clinica,
            'clinicas':clinicas,
            'regiones':regiones,
            'roles':roles
         }

        return render(request, 'veterinarios/agregar.html', data)

@csrf_exempt
def veterinarios_modificar(request, id_medico):
    if request.method == 'POST':
        if request.POST.get('comuna') and request.POST.get('id_clinica') and request.POST.get('pnombre') and request.POST.get('snombre') and request.POST.get('appaterno') and request.POST.get('apmaterno') and request.POST.get('telefono') and request.POST.get('email') and request.POST.get('direccion'):
            
            id_vet = id_medico
            cut_comuna = request.POST.get('comuna')
            id_clinica = request.POST.get('id_clinica')
            pnombre = request.POST.get('pnombre')
            snombre = request.POST.get('snombre')
            appaterno = request.POST.get('appaterno')
            apmaterno = request.POST.get('apmaterno')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')


            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medico'
            data = {
                'id_medico': id_vet,
                'cut_comuna': cut_comuna,
                'id_clinica': id_clinica,
                'pnombre': pnombre,
                'snombre': snombre,
                'appaterno': appaterno,
                'apmaterno': apmaterno,
                'email': email,
                'telefono': telefono,
                'direccion': direccion
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.put(uri, headers=headers, data=json.dumps(data))
            if response.ok:
                return redirect(veterinarios_listar)
        
    else:
        getDocUri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medico?id_medico='+str(id_medico)
        response = requests.get(getDocUri)
        json_data = response.json()
        medico = json_data['items'][0]

        regs_api_url = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/regiones'
        regs_api_resp = requests.get(regs_api_url)
        regs_json_data = regs_api_resp.json()
        regiones = regs_json_data['items']

        uri_clinicas = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/clinicas_api/clinicas'
        response = requests.get(uri_clinicas)
        json_data = response.json()
        clinicas = json_data['items']

        data = { 
            'vet': medico, 
            'regiones': regiones,
            'clinicas': clinicas
            }
        return render(request, 'veterinarios/modificar.html', data)

def veterinarios_listar(request):
    med_uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medicos'
    api_response = requests.get(med_uri)
    json_data = api_response.json()
    medicos = json_data['items']
    data = {
        'medicos':medicos
    }
    return render(request, 'veterinarios/listar.html', data)

def veterinarios_detalle(request, id_medico):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/med_modules/medico?id_medico=' + str(id_medico)
    response = requests.get(uri)
    json_data = response.json()
    medico = json_data['items'][0]
    data = { 'veterinario': medico }
    return render(request, 'veterinarios/ver.html', data)

@csrf_exempt
def vacunas_agregar(request):
    if request.method == 'POST':
        print(request.POST.get('id_especie'))
        if request.POST.get('nom_vac') and request.POST.get('id_especie'):
            print('paso el form')
            nombre = request.POST.get('nom_vac')
            id_especie = request.POST.get('id_especie')
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunas/vacuna'
            data = {
                'nombre': nombre,
                'id_especie': id_especie
            }
            response = requests.post(uri, json=data)
            print(response.status_code)
            print(response.raise_for_status)
            if response.status_code == 200:
                print('Exito')
            else:
                print('algo no funciono')
        print('no paso el form')
        return redirect(vacunas_listar)
    else:
        data = { 'especies': custom_fx.getEspecies() }
        return render(request, 'vacunacion/vacunas/agregar.html', data)

def vacunas_listar(request):
    data = { 
        'vacunas': custom_fx.getVacunas()
    }
    return render(request, 'vacunacion/vacunas/listar.html', data)

def vacunas_modificar(request,id_vacuna):
    return render(request, 'vacunacion/vacunas/editar.html')

def vacunas_detalle(request,id_vacuna):
    data = {
        'vacuna':custom_fx.getVacunaById(id_vacuna)
    }
    return render(request, 'vacunacion/vacunas/ver.html', data)

@csrf_exempt
def recetas_agregar(request, id_atencion):
    if request.method == 'POST':
        if request.POST.get('id_atencion') and request.POST.get('prescripcion'):
            id = request.POST.get('id_atencion')
            prescripcion = request.POST.get('prescripcion')
            post_response = custom_fx.newReceta(id, prescripcion)
            if  post_response.status_code == 200:
                return redirect(recetas_listar)
            else:
                print(post_response.raise_for_status)
        return redirect(recetas_listar)
    else:
        data = { 
            'atenciones':custom_fx.getAtenciones(),
            'id_atencion': int(id_atencion)
            }
        return render(request, 'recetas/agregar.html', data)

def recetas_listar(request):
    data = {
        'recetas': custom_fx.getRecetas()
    }
    return render(request, 'recetas/listar.html', data)

def recetas_modificar(request, id_receta):
    return render(request, 'recetas/editar.html')

def recetas_detalle(request, id_receta):
    data = {
        'receta':custom_fx.getRecetaById(id_receta)
    }
    return render(request, 'recetas/ver.html', data)

@csrf_exempt
def especie_agregar(request):
    if request.method == 'POST':
        if request.POST.get('descripcion'):
            
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_especies/especie'
            descripcion = request.POST.get('descripcion')
            data = {
                'descripcion': descripcion
            }
            
            response = requests.post(uri, json=data)

            if response.status_code == 200:
                return redirect(especie_listar)
            else:
                print(response.status_code)
                print(response.reason)

    return render(request, 'especie/agregar.html')

def especie_listar(request):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_especies/especies'
    response = requests.get(uri)
    json_data = response.json()
    objetos = json_data['items']
    data = { 'especies': objetos }
    return render(request, 'especie/listar.html', data)

def especie_modificar(request, id_especie):
    return render(request, 'especie/editar.html')

def especie_detalle(request, id_especie):
    return render(request, 'especie/ver.html')

@csrf_exempt
def razas_agregar(request, id_esp):
    if request.method == 'POST':
        if request.POST.get('id_especie') and request.POST.get('raza'):
            id_especie = request.POST.get('id_especie')
            raza = request.POST.get('raza')
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_razas/raza'
            data = {
                'id_especie': id_especie,
                'raza': raza
            }
            response = requests.post(uri, json=data)

            if response.status_code == 200:
                return redirect(razas_listar)
            else:
                print(response.status_code)
                print(response.reason)

        return redirect(razas_listar)
    else:
        uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_especies/especies'
        response = requests.get(uri)
        json_data = response.json()
        objetos = json_data['items']
        data = { 'especies': objetos, 'id_especie': id_esp }
        return render(request, 'especie/razas/agregar.html', data)

def razas_listar(request):
    uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_razas/razas'
    response = requests.get(uri)
    json_data = response.json()
    objetos = json_data['items']
    data = { 'razas': objetos }
    return render(request, 'especie/razas/listar.html', data)

def razas_modificar(request, id_raza):
    return render(request, 'especie/razas/editar.html')

def razas_detalle(request, id_raza):
    return render(request, 'especie/razas/ver.html')

def usuarios_agregar(request):
    return render(request, 'usuarios/agregar.html')

def usuarios_listar(request):
    return render(request, 'usuarios/listar.html')

def usuarios_modificar(request, id_usuario):
    return render(request, 'usuarios/editar.html')

def usuarios_detalle(request, id_usuario):
    return render(request, 'usuarios/ver.html')


def agenda_listar(request):
    data = {
        'citas': custom_fx.getAgendamientos()
    }
    return render(request, 'agenda/listar.html', data)

@csrf_exempt
def agenda_agregar(request, id_clinica):
    if request.method == 'POST':
        if request.POST.get('id_clinica') and request.POST.get('servicio') and request.POST.get('nombre') and request.POST.get('telefono')  and request.POST.get('email') and request.POST.get('fecha'):
            data = {
                'id_clinica': request.POST.get('id_clinica'),
                'id_tipo_serv': request.POST.get('servicio'),
                'nombre': request.POST.get('nombre'),
                'f_ini': str(request.POST.get('fecha')),
                'telefono': request.POST.get('telefono'),
                'correo': request.POST.get('email'),
            }
            uri = 'http://fcv.onecloud.cl:8181/ords/fcv_pt/api_agendamiento/agendamiento'

            response = requests.post(uri, json=data)

            if response.status_code == 200:
                print("Agendamiento agregado")
                return redirect(agenda_listar)
            else:
                print("Casi (:")
                print(response.status_code)
                print(response.reason)

        return redirect(agenda_listar)
    else:
        data = {
            'id_clinica': id_clinica,
            'clinicas': custom_fx.getClinicas(),
            'servicios': custom_fx.getServicios()
        }
        return render(request, 'agenda/agregar.html', data)