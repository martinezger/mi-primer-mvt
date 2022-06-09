from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from familia.forms import PersonaForm, BuscarPersonasForm, ActualizarPersonaForm

from familia.models import Persona

def index(request):
    personas = Persona.objects.all()
    template = loader.get_template('familia/lista_familiares.html')
    context = {
        'personas': personas,
    }
    return HttpResponse(template.render(context, request))


def agregar(request):
    '''
    TODO: agregar un mensaje en el template index.html que avise al usuario que 
    la persona fue cargada con éxito
    '''

    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():

            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            altura = form.cleaned_data['altura']
            Persona(nombre=nombre, apellido=apellido, email=email, fecha_nacimiento=fecha_nacimiento, altura=altura).save()

            return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        form = PersonaForm()
    else:
        return HttpResponseBadRequest("Error no conzco ese metodo para esta request")

    
    return render(request, 'familia/form_carga.html', {'form': form})


def borrar(request, identificador):
    '''
    TODO: agregar un mensaje en el template index.html que avise al usuario que 
    la persona fue eliminada con éxito        
    '''
    if request.method == "GET":
        persona = Persona.objects.filter(id=int(identificador)).first()
        if persona:
            persona.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseBadRequest("Error no conzco ese metodo para esta request")


def actualizar(request, identificador=''):
    '''
    TODO: implementar una vista para actualización
    '''
    if request.method == "GET":
        persona = get_object_or_404(Persona, pk=int(identificador))
        initial = {
            "id": persona.id,
            "nombre": persona.nombre, 
            "apellido": persona.apellido, 
            "email": persona.email,
            "fecha_nacimiento": persona.fecha_nacimiento.strftime("%d/%m/%Y"),
            "altura": persona.altura,
        }
    
        form_actualizar = ActualizarPersonaForm(initial=initial)
        return render(request, 'familia/form_carga.html', {'form': form_actualizar, 'actualizar': True})
    
    elif request.method == "POST":
        form_actualizar = ActualizarPersonaForm(request.POST)
        if form_actualizar.is_valid():
            persona = get_object_or_404(Persona, pk=form_actualizar.cleaned_data['id'])
            persona.nombre = form_actualizar.cleaned_data['nombre']
            persona.apellido = form_actualizar.cleaned_data['apellido']
            persona.email = form_actualizar.cleaned_data['email']
            persona.fecha_nacimiento = form_actualizar.cleaned_data['fecha_nacimiento']
            persona.altura = form_actualizar.cleaned_data['altura']
            persona.save()

            return HttpResponseRedirect(reverse("index"))


def buscar(request):
    
    if request.GET.get("palabra_a_buscar") and request.method == "GET":
        form_busqueda = BuscarPersonasForm(request.GET)
        if form_busqueda.is_valid():
            personas = Persona.objects.filter(nombre__icontains=request.GET.get("palabra_a_buscar"))
            return  render(request, 'familia/lista_familiares.html', {"personas": personas, "resultados_busqueda":True})

    elif request.method == "GET":
        form_busqueda = BuscarPersonasForm()
        return render(request, 'familia/form_busqueda.html', {"form_busqueda": form_busqueda})
        
    
