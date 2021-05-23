from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import requests
import pandas as pd
import numpy as np
import re

views = Blueprint('views', __name__)
cliente = None

## -- PÁGINA INICIAL --
@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')


@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    df = pd.read_csv('data/clientes.csv', dtype=object, sep=';')
    df = df.replace(np.nan, '', regex=True)
    return render_template('clientes.html', df=df, titles=df.columns.values)


## -- CADASTRO --
@views.route('/cadastro', methods=['GET', 'POST'])    ### Adicionada permissão para POST Request para o URL
def cadastro():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """
    ## TODO pegar informações do forms
    #if request.method == 'POST':
    #    cliente = (f'\n%s; %s; %s; %s' % (request.form['nome'], request.form['sobrenome'], request.form['email'], request.form['cep']))
        
    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)
    #data = requests.get(f'http://viacep.com.br/ws/{cliente[3]}/json/', cliente[3])

    ## TODO criar nova linha no arquivo csv
    #data = data.keys()


    return render_template('cadastro.html')


## -- CONSULTA CEP --
@views.route('/consulta-cep', methods=['GET', 'POST'])
def consulta_cep():
    ## TODO pegar CEP do forms

    if request.method == 'POST':
        cep = request.form['cep']

        check = re.search("^(\d{8})$", cep)   ###  Pequeno tratamento de exceção para garantir o envio correto do CEP para a API

        if check == None:
            flash("CEP inválido, por favor tente novamente.", "error")
            return render_template('consulta_cep.html')

    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)

        data = requests.get(f'http://viacep.com.br/ws/{cep}/json/', cep)  ### Pega o cep na API ViaCep
        data = data.json()

        if len(data) == 1:  ### Caso o CEP não seja encontrado pela API, o retorno é: '{error: True}', ou seja, um dicíonario/JSON com apenas um elemento
            flash("CEP não encontrado, por favor tente novamente.", "error")
            return render_template('consulta_cep.html')
          
    ## TODO mostrar no html as informações obtidas

        flash("CEP encontrado!")
        return render_template('consulta_cep.html', cep=data['cep'],logradouro=data['logradouro'],complemento=data['complemento'],bairro=data['bairro'],localidade=data['localidade'],uf=data['uf'],ibge=data['ibge'],gia=data['gia'],ddd=data['ddd'],siafi=data['siafi'])
    
    return render_template('consulta_cep.html')