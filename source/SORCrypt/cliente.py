#coding: utf-8

"""
Modulo responsável por realizar as requisições ao servidor de nomes do software.
"""

import socket
import settings
from sys import argv
from os import system

class Cliente:
    """
    Esta Classe permite criar conexões com um determinado host em uma determinada porta.
    """

    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.soquete = None

    def conecta_servidor(self):
        """
        Retorna o estado da conexão do servidor.
        """
        try:
            self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soquete.connect((self.host, self.porta))
            return True
        except Exception, error:
            return False

    def enviar_mensagem(self, mensagem):
        """
        Conecta a um host e porta, e envia a mensagem.
        """
        self.soquete.send(mensagem)

    def receber_mensagem(self):
        """
        Recebe uma mensagem. O parametro tam pode ser definido.
        """
        tam=1024
        print 'aqui'
        return self.soquete.recv(tam)

    def fechar_conexao(self):
        """
        Fecha a conexão do soquete.
        """
        self.soquete.close()


def realiza_operacao(operacao, n1, n2):
    """
    Realiza uma determinada operação com um servidor.
    """
    cliente = Cliente(settings.HOST_NOMES, settings.PORTA_NOMES)
    if cliente.conecta_servidor():

        cliente.enviar_mensagem(operacao)
        servidor = cliente.receber_mensagem()

        cliente.fechar_conexao()
        cliente = Cliente(servidor, settings.PORTA_FUNCOES)
        if cliente.conecta_servidor():
            cliente.enviar_mensagem('{0}_{1}_{2}_'.format(operacao, n1, n2))
            resposta = cliente.receber_mensagem()
            cliente.fechar_conexao()
            return resposta
    else:
        return 'Impossível Calcular'