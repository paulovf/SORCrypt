#coding: utf-8

"""
Modulo responsável por realizar as requisições ao servidor de nomes do software.
"""

import socket
import settings
import pickle
from sys import argv
from os import system
from Crypto.PublicKey import RSA
from Crypto.Util import randpool


class Cliente:
    """
    Esta Classe permite criar conexões com um determinado host em uma determinada porta.
    """

    def __init__(self):
        self.soquete = None
        arqPoll = randpool.RandomPool()
        self.chavePrivada = RSA.generate(1024, arqPoll.get_bytes)
        self.chavePublica = self.chavePrivada.publickey()

    def conecta_servidor(self, host, porta):
        """
        Retorna o estado da conexão do servidor.
        """
        try:
            self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soquete.connect((host, porta))
            return True
        except Exception, error:
            return False

    def enviar_mensagem(self, mensagem):
        """
        Conecta a um host e porta, e envia a mensagem.
        """
        self.soquete.send(pickle.dumps(self.chavePublica))
        msgChavePublicaServidor = self.soquete.recv(1024)
        chavePublicaServidor = pickle.loads(msgChavePublicaServidor)
        msgCriptografada = chavePublicaServidor.encrypt(mensagem, 32)[0]
        self.soquete.send(msgCriptografada)

    def receber_mensagem(self):
        """
        Recebe uma mensagem. O parametro tam pode ser definido.
        """        
        respostaCriptografada = self.soquete.recv(1024)
        return self.chavePrivada.decrypt(respostaCriptografada)

    def fechar_conexao(self):
        """
        Fecha a conexão do soquete.
        """
        self.soquete.close()


def realiza_operacao(operacao, n1, n2):
    """
    Realiza uma determinada operação com um servidor.
    """
    cliente = Cliente()
    if cliente.conecta_servidor(settings.HOST_NOMES, settings.PORTA_NOMES):

        cliente.enviar_mensagem(operacao)
        servidor = cliente.receber_mensagem()
        print servidor
        cliente.fechar_conexao()

        cliente = Cliente()
        if cliente.conecta_servidor(servidor, settings.PORTA_FUNCOES):

            cliente.enviar_mensagem('{0}_{1}_{2}_'.format(operacao, n1, n2))
            resposta = cliente.receber_mensagem()
            cliente.fechar_conexao()
            return resposta
    else:
        return 'ERRO'
