#coding: utf-8

"""
Modulo responsavel por tratar as requisições como soma, divisao do software.
"""

import socket
import settings
from threading import Thread
from funcoes_crypt import Funcoes_crypt
from arquivo_objeto import Arquivo_objeto


lista_chaves = []

def soma(conexao, valores, chave):
    """
    Envia ao cliente a soma de dois valores.
    """
    mensagem = '{0}'.format(float(valores[1]) + float(valores[2]))
    objeto = Funcoes_crypt().criptografar_mensagem(mensagem, chave)
    msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
    conexao.send(msg)
    
def subtracao(conexao, valores, chave):
    """
    Envia ao cliente a subtração de dois valores.
    """
    mensagem = '{0}'.format(float(valores[1]) - float(valores[2]))
    objeto = Funcoes_crypt().criptografar_mensagem(mensagem, chave)
    msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
    conexao.send(msg)    


def produto(conexao, valores, chave):
    """
    Envia ao cliente o produto de dois valores.
    """
    mensagem = '{0}'.format(float(valores[1]) * float(valores[2]))
    objeto = Funcoes_crypt().criptografar_mensagem(mensagem, chave)
    msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
    conexao.send(msg)    


def divisao(conexao, valores, chave):
    """
    Envia ao cliente a divisão de dois valores.
    """
    mensagem = '{0}'.format(float(valores[1]) / float(valores[2]))
    objeto = Funcoes_crypt().criptografar_mensagem(mensagem, chave)
    msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
    conexao.send(msg)      


def porcentagem(conexao, valores, chave):
    """
    Envia ao cliente a porcentagem de dois valores.
    """
    mensagem = '{0}'.format(float(valores[1]) % float(valores[2]))
    objeto = Funcoes_crypt().criptografar_mensagem(mensagem, chave)
    msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
    conexao.send(msg)      
    

def fatorial(conexao, valores, chave):
    """
    Envia ao cliente o fatorial de um número.
    """
    soma = 1
    for i in range(2, int(valores[1]) + 1):
        soma *= i
        
    mensagem = '{0}'.format(soma)
    objeto = Funcoes_crypt().criptogtafar_mensagem(mensagem, chave)
    msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
    conexao.send(msg)          


def trata_cliente(conexao, endereco):
    """
    Trata as novas requisições dos clientes.
    """
    global lista_chaves
    dados = conexao.recv(1024)
    objeto = Arquivo_objeto(dados).obter_objeto_arquivo()
    requisicao = Funcoes_crypt().descriptografar_mensagem(objeto, lista_chaves[0])
    requisicao = requisicao.split('_')

    print 'Endereço: {0} Requisição: {1}'.format(endereco[0], requisicao[0])

    # Requisição de soma.
    if requisicao[0] == settings.SOMA:
        soma(conexao, requisicao, lista_chaves[2])
        
    # Requisição de sobtração.
    elif requisicao[0] == settings.SUBTRACAO:
        subtracao(conexao, requisicao, lista_chaves[2])        

    # Requisição de produto.
    elif requisicao[0] == settings.PRODUTO:
        produto(conexao, requisicao, lista_chaves[2])

    # Requisição de divisao.
    elif requisicao[0] == settings.DIVISAO:
        divisao(conexao, requisicao, lista_chaves[2])

    # Requisição de divisao.
    elif requisicao[0] == settings.FATORIAL:
        fatorial(conexao, requisicao, lista_chaves[2])

    # Requisição de porcentagem.
    elif requisicao[0] == settings.PORCENTAGEM:
        porcentagem(conexao, requisicao, lista_chaves[2])

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def loop_servidor():
    """
    Aguarda a chegada da chave pública do cliente
    """
    global lista_chaves
    
    """
    Gera as chaves do servidor de funções
    """
    lista_chaves.append(Funcoes_crypt().gerar_chaves_de_criptografia())
    
    """
    Gera a chave pública do servidor de funções
    """
    lista_chaves.append(Funcoes_crypt().obter_chave_publica(lista_chaves[0]))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((settings.HOST_FUNCOES, settings.PORTA_ENVIO_SERVIDOR_FUNCOES))
    dados, cliente = s.recvfrom(settings.TAM_MSG)
    s.close()
    
    """
    Salva a chave pública do cliente
    """
    lista_chaves.append(Arquivo_objeto(dados).obter_objeto_arquivo())
    
        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(Arquivo_objeto(lista_chaves[1]).gerar_arquivo_objeto(), (cliente[0], settings.PORTA_ENVIO_CLIENTE))
    s.close()

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
