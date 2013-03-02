#coding: utf-8

"""
Modulo responsavel por tratar as requisições como soma, divisao do software.
"""

import socket
import settings
from threading import Thread


def soma(conexao):
    """
    Envia ao cliente a soma de dois valores.
    """
    print 'aqui 1'
    valores = conexao.recv(1024)
    print 'aqui 2'
    valores = valores.split('_')
    print valores.split('_')
    print 'aqui 3'
    conexao.send('{0}'.format(int(valores[0]) + int(valores[1])))
    print 'aqui 4'


def produto(conexao):
    """
    Envia ao cliente o produto de dois valores.
    """
    valores = conexao.recv(1024)
    valores = valores.split('_')
    conexao.send('{0}'.format(int(valores[0]) * int(valores[1])))


def divisao(conexao):
    """
    Envia ao cliente a divisão de dois valores.
    """
    valores = conexao.recv(1024)
    valores = valores.split('_')
    conexao.send('{0}'.format(int(valores[0]) / int(valores[1])))


def trata_cliente(conexao, endereco):
    """
    Trata as novas requisições dos clientes.
    """
    print endereco
    
    print '3'
    requisicao = conexao.recv(settings.TAM_MSG)
    print '4'
    print requisicao
    # Requisição de soma.
    if requisicao == settings.SOMA:
        print 'aqui'
        soma(conexao)

    # Requisição de produto.
    if requisicao == settings.PRODUTO:
        produto(conexao)

    # Requisição de divisao.
    elif requisicao == settings.DIVISAO:
        divisao(conexao)

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def loop_servidor():
    """
    Abre um novo soquete servidor para tratar as novas conexões do cliente.
    """
    soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soquete.bind((settings.HOST_FUNCOES, settings.PORTA_FUNCOES))
    soquete.listen(settings.LISTEN)
    print '1'

    # Fica aqui aguardando novas conexões.
    while True:
        # Para cada nova conexão é criado um novo processo para tratar as requisições.
        print '2'
        Thread(target=trata_cliente, args=(soquete.accept())).start()


if __name__  == '__main__':
    print 'Servidor de Funções Iniciou na Porta {0}'.format(settings.PORTA_FUNCOES)
    Thread(target=loop_servidor).start()
