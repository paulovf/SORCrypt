#coding: utf-8

"""
Modulo responsavel por tratar das funções existentes em outros servidores de funções do software.
"""

import socket
import settings
from threading import Thread
from cliente import Cliente
from json import loads


def verifica_funcao(funcao):
    """
    Busca as funções dos servidores de funcoes.
    """
    print funcao
    servidores = []
    dados = open(settings.SERVIDORES).read()
    arq = loads(dados)
    for a in arq:
        for t in a:
            if t == funcao:
                servidores.append(a[0])

    return servidores


def trata_cliente(conexao, endereco):
    """
    Trata as novas requisições dos clientes.
    """
    print endereco
    funcao = conexao.recvfrom(settings.TAM_MSG)
    print '>>> {0}'.format(funcao)
    servidores = verifica_funcao(funcao)

    # Requisição autorizada.
    if len(servidores) != 0:
        print servidores
        print 'aqui 1'
        print servidores[0]
        print servidores
        conexao.send(servidores[0])
        print 'aqui 2'

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def loop_servidor():
    """
    Abre um novo soquete servidor para tratar as novas conexões do cliente.
    """
    soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soquete.bind((settings.HOST_NOMES, settings.PORTA_NOMES))
    soquete.listen(settings.LISTEN)

    # Fica aqui aguardando novas conexões.
    while True:
        # Para cada nova conexão é criado um novo processo para tratar as requisições.
        Thread(target=trata_cliente, args=(soquete.accept())).start()


if __name__ == '__main__':
    print 'Servidor de Nomes Iniciou na Porta {0}'.format(settings.PORTA_NOMES)
    Thread(target=loop_servidor).start()
