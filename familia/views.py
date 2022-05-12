from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from familia.forms import PersonaForm

from familia.models import Persona

def index(request):
    personas = Persona.objects.all()
    template = loader.get_template('familia/index.html')
    context = {
        'personas': personas,
    }
    return HttpResponse(template.render(context, request))


def agregar(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():

            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            Persona(nombre=nombre, apellido=apellido, email=email).save()

            return HttpResponseRedirect("/familia/")
    else:
        form = PersonaForm()
    
    return render(request, 'familia/form_carga.html', {'form': form})


def borrar(request, identificador):
    persona = Persona.objects.filter(id=int(identificador)).first()

    if persona:
        persona.delete()
    
    #TODO: agregar un mensaje en el template index.html que avise al usuario que 
    # la persona fue eliminada con éxito

    return HttpResponseRedirect("/familia/")
