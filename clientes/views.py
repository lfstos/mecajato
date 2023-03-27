import re
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
from django.core import serializers


# Create your views here.


def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf=cpf)

        context = {
            'nome': nome,
            'sobrenome': sobrenome,
            'carros': zip(carros, placas, anos)
        }

        if cliente.exists():
            context['email'] = email
            return render(request, 'clientes.html', context)

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            context['cpf'] = cpf
            return render(request, 'clientes.html', context)
        cliente = Cliente(nome=nome, sobrenome=sobrenome, email=email, cpf=cpf)
        cliente.save()
        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()
        return HttpResponse('teste')


def atualiza_cliente(request):
    cliente_id = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=cliente_id)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    return JsonResponse(cliente_json)
