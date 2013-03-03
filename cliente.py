#coding: utf-8

"""
Modulo responsável por realizar as requisições ao servidor de nomes do software.
"""

import socket
import settings
from sys import argv

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
			print error[0]
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


def realiza_operacao(operacao, valores):
    """
    Realiza uma determinada operação com um servidor.
    """
    print valores
    cliente = Cliente(settings.HOST_NOMES, settings.PORTA_NOMES)
    if cliente.conecta_servidor():

        cliente.enviar_mensagem(operacao)
        servidor = cliente.receber_mensagem()
        print servidor
        cliente.fechar_conexao()
        cliente = Cliente(servidor, settings.PORTA_FUNCOES)
        if cliente.conecta_servidor():
            cliente.enviar_mensagem('{0}_{1}_{2}'.format(operacao, valores[0], valores[1]))
            print '{0}_{1}_{2}'.format(operacao, valores[0], valores[1])
            resposta = cliente.receber_mensagem()
            cliente.fechar_conexao()
            print resposta
    else:
        print 'Não foi possível se Conectar.'


if __name__ == '__main__':
	if len(argv) == 3:
		realiza_operacao(argv[1], argv[2].split('_'))
	else:
		print '<operacao> <valores separados de um _ >'
