#coding: utf-8

"""
Modulo responsavel por tratar das funções existentes em outros servidores de funções do software.
"""

import socket
import pickle
import settings
from json import loads
from cliente import Cliente
from threading import Thread
from Crypto.PublicKey import RSA
from Crypto.Util import randpool


def verifica_funcao(funcao):
    """
    Busca as funções dos servidores de funcoes.
    """
    servidores = []
    dados = open(settings.SERVIDORES).read()
    arq = loads(dados)
    for a in arq:
        for t in a:
            if t == funcao:
                servidores.append(a[0])

    return servidores


def trata_cliente(conexao, endereco, chavePrivada, chavePublica):
    """
    Trata as novas requisições dos clientes.
    """
    
    chavePublicaCliente = pickle.loads(conexao.recv(1024))
    conexao.send(pickle.dumps(chavePublica))

    requisicao = chavePrivada.decrypt(conexao.recv(1024))
    
    print 'Endereço: {0} Requisição: {1}'.format(endereco, requisicao)

    servidores = verifica_funcao(requisicao)
    
    # Requisição autorizada.
    if len(servidores) != 0:
        ip = servidores[0].encode('ascii', 'ignore')
        resposta = chavePublicaCliente.encrypt(ip, 32)[0]
        conexao.send(resposta)

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def loop_servidor():
    """
    Cria um novo soquete e aguarda conexoes.
    """
    
    arqPoll = randpool.RandomPool()
    chavePrivada = RSA.generate(1024, arqPoll.get_bytes)
    chavePublica = chavePrivada.publickey()

    soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soquete.bind((settings.HOST_NOMES, settings.PORTA_NOMES))
    soquete.listen(settings.LISTEN)

    # Fica aqui aguardando novas conexões.
    while True:

        # Para cada nova conexão é criado um novo processo para tratar as requisições.
        conexao = soquete.accept()
        novaConexao = []
        novaConexao.append(conexao[0])
        novaConexao.append(conexao[1])
        novaConexao.append(chavePrivada)
        novaConexao.append(chavePublica)
        Thread(target=trata_cliente, args=(novaConexao)).start()


if __name__ == '__main__':
    print 'Servidor de Nomes Iniciou na Porta {0}'.format(settings.PORTA_NOMES)
    Thread(target=loop_servidor).start()
