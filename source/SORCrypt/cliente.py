#coding: utf-8

"""
Modulo responsável por realizar as requisições ao servidor de nomes do software.
"""

import socket
import settings
from funcoes_crypt import Funcoes_crypt
from arquivo_objeto import Arquivo_objeto
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
        self.lista_chaves = []

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

    def enviar_mensagem(self, mensagem, chave):
        """
        Conecta a um host e porta, e envia a mensagem.
        """
        objeto = Funcoes_crypt().criptografar_mensagem(mensagem, chave)
        msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
        self.soquete.send(msg)

    def receber_mensagem(self, chave):
        """
        Recebe uma mensagem. O parametro tam pode ser definido.
        """        
        tam=1024
        dados = self.soquete.recv(settings.TAM_MSG)
        objeto = Arquivo_objeto(dados).obter_objeto_arquivo()
        return Funcoes_crypt().descriptografar_mensagem(objeto, chave)

    def fechar_conexao(self):
        """
        Fecha a conexão do soquete.
        """
        self.soquete.close()


def realiza_operacao(operacao, n1, n2, lista_chaves):
    """
    Realiza uma determinada operação com um servidor.
    """
    cliente = Cliente(settings.HOST_NOMES, settings.PORTA_NOMES)
    if cliente.conecta_servidor():

        cliente.enviar_mensagem(operacao, lista_chaves[2])
        servidor = cliente.receber_mensagem(lista_chaves[0])
        cliente.fechar_conexao()
        """
        Obtém a chave pública do servidor de funções
        """
        lista_chaves.append(Funcoes_crypt().troca_chaves_servidor_funcoes(servidor, lista_chaves[1]))
        cliente = Cliente(servidor, settings.PORTA_FUNCOES)
        
        if cliente.conecta_servidor():

            cliente.enviar_mensagem('{0}_{1}_{2}_'.format(operacao, n1, n2), lista_chaves[3])
            resposta = cliente.receber_mensagem(lista_chaves[0])
            cliente.fechar_conexao()
            return resposta
    else:
        return 'Impossível Calcular'
