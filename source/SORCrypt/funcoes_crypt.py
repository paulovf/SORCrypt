#coding: utf-8

import re
import settings
import socket
from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
from arquivo_objeto import Arquivo_objeto


"""
Módulo responsável por fornecer métodos de criptografia.
"""

class Funcoes_crypt:
    """
    Esta classe implementa os métodos referentes a criptografia RSA
    """
    
    def __init__(self):
        self.tamanho_chave = 1024
        self.lista_chaves = []
        
    def gerar_chaves_de_criptografia(self):
        """
        Gera as chaves pública e privada
        """
        pool = open("/dev/urandom")
        funcao_rand = pool.read
        self.tamanho_chave = 1024
        k = ''

        """ 
        Chave possui as chaves pública e privada       
        """
        return RSA.generate(self.tamanho_chave, funcao_rand)
        
    def troca_de_chaves(self):
        """
        Envia a chave pública para o servidor de nomes, que envia
        para o cliente a sua chave pública
        """
        chaves = Funcoes_crypt()
        self.lista_chaves.append(chaves.gerar_chaves_de_criptografia())
        
        chave_publica_cliente = chaves.obter_chave_publica(self.lista_chaves[0])
        self.lista_chaves.append(chave_publica_cliente)
        
        arquivo = Arquivo_objeto(chave_publica_cliente)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(arquivo.gerar_arquivo_objeto(), (settings.HOST_NOMES, settings.PORTA_ENVIO_SERVIDOR_NOMES))
        s.close()
        
        res = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        res.bind((settings.HOST_CLIENTE, settings.PORTA_ENVIO_CLIENTE))
        dados, host = res.recvfrom(settings.TAM_MSG)
        res.close()
        arq = Arquivo_objeto(dados)
        self.lista_chaves.append(arq.obter_objeto_arquivo())
        return self.lista_chaves
        
    def troca_chaves_servidor_funcoes(self, ip_servidor, chave_publica_cliente):
        """
        Envia a chave pública para o servidor de funcoes, que envia
        para o cliente a sua chave pública
        """    
        arquivo = Arquivo_objeto(chave_publica_cliente)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(arquivo.gerar_arquivo_objeto(), (ip_servidor, settings.PORTA_ENVIO_SERVIDOR_FUNCOES))
        s.close()
        
        res = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        res.bind((settings.HOST_CLIENTE, settings.PORTA_ENVIO_CLIENTE))
        dados, host = res.recvfrom(1024)
        res.close()
        arq = Arquivo_objeto(dados)
        return arq.obter_objeto_arquivo()
        
    def obter_chaves_de_acesso(self):        
        """
        Obtém a chave pública do servidor de nomes e envia a chave 
        pública do cliente
        """
        return self.troca_de_chaves() 
        
    def obter_chave_publica(self, chave):
        return chave.publickey()
        
    def criptografar_mensagem(self, mensagem, chave):
        return chave.encrypt(mensagem, self.tamanho_chave)
        
    def descriptografar_mensagem(self, mensagem, chave):
        return chave.decrypt(mensagem)        
