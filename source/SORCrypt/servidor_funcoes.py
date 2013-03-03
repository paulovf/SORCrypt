#coding: utf-8

"""
Modulo responsavel por tratar as requisições como soma, divisao do software.
"""

import socket
import settings
from threading import Thread


def soma(conexao, valores):
    """
    Envia ao cliente a soma de dois valores.
    """
    conexao.send('{0}'.format(float(valores[1]) + float(valores[2])))


def produto(conexao, valores):
    """
    Envia ao cliente o produto de dois valores.
    """
    conexao.send('{0}'.format(float(valores[1]) * float(valores[2])))


def divisao(conexao, valores):
    """
    Envia ao cliente a divisão de dois valores.
    """
    conexao.send('{0}'.format(float(valores[1]) / float(valores[2])))


def porcentagem(conexao, valores):
    """
    Envia ao cliente a porcentagem de dois valores.
    """
    conexao.send('{0}'.format(float(valores[1]) % float(valores[2])))


def fatorial(conexao, valores):
    """
    Envia ao cliente o fatorial de um número.
    """
    soma = 1
    for i in range(2, int(valores[1]) + 1):
        soma *= i
    conexao.send('{0}'.format(soma))


def trata_cliente(conexao, endereco):
    """
    Trata as novas requisições dos clientes.
    """

    requisicao = conexao.recv(1024)
    requisicao = requisicao.split('_')

    print 'Endereço: {0} Requisição: {1}'.format(endereco[0], requisicao[0])

    # Requisição de soma.
    if requisicao[0] == settings.SOMA:
        soma(conexao, requisicao)

    # Requisição de produto.
    elif requisicao[0] == settings.PRODUTO:
        produto(conexao, requisicao)

    # Requisição de divisao.
    elif requisicao[0] == settings.DIVISAO:
        divisao(conexao, requisicao)

    # Requisição de divisao.
    elif requisicao[0] == settings.FATORIAL:
        fatorial(conexao, requisicao)

    # Requisição de porcentagem.
    elif requisicao[0] == settings.PORCENTAGEM:
        porcentagem(conexao, requisicao)

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def loop_servidor():
    """
    Abre um novo soquete servidor para tratar as novas conexões do cliente.
    """
    soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soquete.bind((settings.HOST_FUNCOES, settings.PORTA_FUNCOES))
    soquete.listen(settings.LISTEN)

    # Fica aqui aguardando novas conexões.
    while True:
        # Para cada nova conexão é criado um novo processo para tratar as requisições.
        Thread(target=trata_cliente, args=(soquete.accept())).start()


if __name__  == '__main__':
    print 'Servidor de Funções Iniciou na Porta {0}'.format(settings.PORTA_FUNCOES)
    Thread(target=loop_servidor).start()
