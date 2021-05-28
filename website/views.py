## -- IMPORTANTE! --
## Quando este script é acionado, uma linha em branco é criada no final do arquivo "data.clientes.csv" para evitar que o Pandas insira o DataFrame em uma linha já populada.
## Certifique-se de deixar uma linha em branco ao modificar o arquivo CSV durante a execução do programa.

from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import requests
import pandas as pd
import numpy as np
import re
from .forms import Registrar, Login

views = Blueprint('views', __name__)

with open('data/clientes.csv', 'a') as f:  # Cria uma linha em branco no final do CSV para evitar que o Pandas insira o dataframe em uma linha já populada
    f.write('\n')

## -- PÁGINA INICIAL --
@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')

@views.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = Registrar()
    if form.validate_on_submit():
        flash('Cadastrado kkk!.')
        return redirect(url_for('.home'))
    return render_template('registrar.html', tittle='kkkaa', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        flash('Logado kkk!.')
        return redirect(url_for('.home'))
    return render_template('login.html', tittle='logiunnn', form=form)

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
@views.route('/cadastro', methods=['GET', 'POST'])  # Adicionada permissão para POST Requests
def cadastro():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """

    ## TODO pegar informações do forms
    if request.method == 'POST':
        cliente = {'nome': request.form['nome'], 'sobrenome' : request.form['sobrenome'], 'email' : request.form['email']}

    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)
        cep = request.form['cep']

        check = re.search('^(\d{8})$', cep)  # Pequeno tratamento de erro em ReGex para garantir o envio correto do CEP para a API
        if check == None:
            flash('CEP inválido. O CEP deve conter 8 NÚMEROS.', 'error')
            return render_template('cadastro.html')

        viacep = requests.get(f'http://viacep.com.br/ws/{cep}/json/', cep)
        viacep = viacep.json()  # Transforma o objeto de retorno da API em JSON

        if ('erro' in viacep):  # Quando um CEP é inserido corretamente, porém não é encontrado pela API, o retorno da API é um JSON: {'erro' = True}
            flash('CEP não encontrado, por favor tente novamente.', 'error')
            return render_template('cadastro.html')
        
        cliente.update(viacep)  # Concatena o dicionário "viacep" ao dicionário "cliente"

    ## TODO criar nova linha no arquivo csv
        df = pd.DataFrame([cliente])
        df.to_csv('data/clientes.csv', mode='a', header=False, index=False, sep=';')  # Insere o DataFrame "cliente" ao CSV

        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('.home'))  # Por causa do Blueprint, argmuento do URL_FOR precisa de ponto "." para funcionar

    return render_template('cadastro.html')


## -- CONSULTA CEP --
@views.route('/consulta-cep', methods=['GET', 'POST'])
def consulta_cep():

    ## TODO pegar CEP do forms
    if request.method == 'POST':
        cep = request.form['cep']

        check = re.search('^(\d{8})$', cep)
        if check == None:
            flash('CEP inválido. O CEP deve conter 8 NÚMEROS.', 'error')
            return render_template('consulta_cep.html')

    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)
        viacep = requests.get(f'http://viacep.com.br/ws/{cep}/json/', cep)
        viacep = viacep.json()

        if ('erro' in viacep):
            flash('CEP não encontrado, por favor tente novamente.', 'error')
            return render_template('consulta_cep.html')  

    ## TODO mostrar no html as informações obtidas
        flash('CEP encontrado!')
        return render_template('consulta_cep.html', cep=viacep['cep'],logradouro=viacep['logradouro'],complemento=viacep['complemento'],bairro=viacep['bairro'],localidade=viacep['localidade'],uf=viacep['uf'],ibge=viacep['ibge'],gia=viacep['gia'],ddd=viacep['ddd'],siafi=viacep['siafi'])
    
    return render_template('consulta_cep.html')