import re
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


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
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente[0])
            car.save()
        return HttpResponse('teste')


def atualiza_cliente(request):
    cliente_id = request.POST.get('id_cliente')

    cliente = Cliente.objects.filter(id=cliente_id)
    carros = Carro.objects.filter(cliente=cliente[0])

    clientes_json = json.loads(serializers.serialize('json', cliente))[
        0]['fields']
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']}
                   for carro in carros_json]

    data = {'cliente': clientes_json, 'carros': carros_json}

    return JsonResponse(data)


@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')

    carro = Carro.objects.get(id=id)
    list_carro = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_carro.exists():
        return HttpResponse('Placa já existente')

    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()
    return HttpResponse('Dados alterados com sucesso')


def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=atualizar_cliente&id_cliente={id}')
    except:
        # TODO: Exibir mensagem de erro
        return redirect(reverse('clientes')+f'?aba=atualizar_cliente&id_cliente={id}')
