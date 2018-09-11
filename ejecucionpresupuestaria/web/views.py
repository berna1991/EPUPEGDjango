from django.shortcuts import render
import requests

from .forms import PostForm
from .API import Api
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

# Create your views here.

dependencias = None


def saludo(request):
    nombre = "Uelsen"
    blog = "https://www.uno-de-piera.com"
    tupla = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    context = {
        'saludo': 'hola que hace',
        'tupla': tupla,
        'nombre': nombre,
        'blog': blog
        }

    #devolvemos los datos a la vista saludo.html para mostrarlos
    return render(request, 'saludo.html', context)

def formulario(request):
    try:
        api = Api()

        tokenValido = api.validarToken(request.session["token"])
        if(tokenValido):
            return HttpResponseRedirect('/home/')
    except:
        api = Api()
        

    form = PostForm()    
    return render(request, 'formulario.html', {'form': form})

def getToken(request):
    if(request.method == "POST"):
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        api = Api()
        token = api.getToken(usuario, password)

        if(token != None):
            request.session["token"] = token
            return HttpResponseRedirect('/home/')

    return HttpResponseRedirect('/formulario/')

        
def home(request):
    global dependencias
    api = Api()
    try:
        tokenValido = api.validarToken(request.session["token"])
        if(not tokenValido):
            return HttpResponseRedirect('/formulario/')
    except:
        return HttpResponseRedirect('/formulario/')


    usuario = api.getUsuario(request.session["token"])
    dependencias = api.leerDependencias(request.session["token"])

    if(usuario != None and dependencias != None):
        context = {
            'nombre' : usuario["nombre"],
            'dependencias' : dependencias
            }
        return render(request, "home.html", context)
    else :
        context = {
            'nombre' : request.session["token"]
            }
        return render(request, "home.html", context)

def dependencias(request):
    api = Api()
    try:
        tokenValido = api.validarToken(request.session["token"])
        if(not tokenValido):
            return HttpResponseRedirect('/formulario/')
    except:
        return HttpResponseRedirect('/formulario/')

    idDependencia = request.GET.get('dependencia')
    dependencia = buscarDependencia(idDependencia, dependencias)

    ejecucionPresupuestaria = api.ejecucionPresupuestaria(dependencia["id"], request.session["token"])

    if(len(ejecucionPresupuestaria) > 0):
        opcionesPrograma = api.buscarFiltro(dependencia["id"], "id_programa", request.session["token"])
        opcionesProyecto = api.buscarFiltro(dependencia["id"], "id_proyecto", request.session["token"])
        opcionesActividad = api.buscarFiltro(dependencia["id"], "id_actividad", request.session["token"])
        opcionesFuente = api.buscarFiltro(dependencia["id"], "id_fuente", request.session["token"])
        opcionesOrganismo = api.buscarFiltro(dependencia["id"], "id_organismo", request.session["token"])
        opcionesObjetoDeGasto = api.buscarFiltro(dependencia["id"], "id_objeto_de_gasto", request.session["token"])
        opcionesBeneficiario = api.buscarFiltro(dependencia["id"], "id_beneficiario", request.session["token"])
    

    context = {
        'idDependencia' : dependencia["id"],
        'nombreDependencia' : dependencia["nombre"],
        'subDependencias' : dependencia["subDependencias"],
        'ejecucionPresupuestaria' : ejecucionPresupuestaria,
        'opcionesPrograma' : opcionesPrograma,
        'opcionesProyecto' : opcionesProyecto,
        'opcionesActividad' : opcionesActividad,
        'opcionesFuente' : opcionesFuente,
        'opcionesOrganismo' : opcionesOrganismo,
        'opcionesObjetoDeGasto' : opcionesObjetoDeGasto,
        'opcionesBeneficiario' : opcionesBeneficiario}
    
    return render(request, "dependencias.html", context)

def sitemap(request):
    lista = []
    listarDependencias(lista, dependencias)
    context = {
        'lista': lista
        }

    return render(request, "sitemap.html", context)

def buscarDependencia(idDependencia, lista):
    for elemento in lista:
        if(int(elemento["id"]) == int(idDependencia)):
            return elemento

        if(len(elemento["subDependencias"]) > 0):
            dependencia = buscarDependencia(idDependencia, elemento["subDependencias"])
            if dependencia != None :
                return dependencia

    return None

def listarDependencias(lista, lDependencias):
    for elemento in lDependencias :
        lista.append(elemento)
        if (len(elemento["subDependencias"]) > 0):
            listarDependencias(lista, elemento["subDependencias"])


def mostrarFiltro(request):
    filtro = request.GET.get('objeto')

    api = Api()
    try:
        tokenValido = api.validarToken(request.session["token"])
        if(not tokenValido):
            return HttpResponseRedirect('/formulario/')
    except:
        return HttpResponseRedirect('/formulario/')

    idDependencia = request.GET.get('dependencia')
    dependencia = buscarDependencia(idDependencia, dependencias)

    ejecucionPresupuestaria = api.consultaConFiltros(dependencia["id"], filtro, request.session["token"])

    newJson = {"filtro" : filtro, "dependencia" : idDependencia,
               "EjecucionPresupuestaria": ejecucionPresupuestaria}
    return JsonResponse(newJson)
