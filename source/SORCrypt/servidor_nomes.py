#coding: utf-8

"""
Modulo responsavel por tratar das funções existentes em outros servidores de funções do software.
"""

import socket
import settings
from threading import Thread
from cliente import Cliente
from funcoes_crypt import Funcoes_crypt
from arquivo_objeto import Arquivo_objeto
from json import loads

lista_chaves = []

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


def trata_cliente(conexao, endereco):
    """
    Trata as novas requisições dos clientes.
    """
    global lista_de_chaves
    dados, host = conexao.recvfrom(settings.TAM_MSG)
    objeto = Arquivo_objeto(dados).obter_objeto_arquivo()
    requisicao = Funcoes_crypt().descriptografar_mensagem(objeto, lista_chaves[0])

    print 'Endereço: {0} Requisição: {1}'.format(endereco[0], requisicao)

    servidores = verifica_funcao(requisicao)
    # Requisição autorizada.
    if len(servidores) != 0:
        ip = servidores[0].encode('ascii', 'ignore')
        objeto = Funcoes_crypt().criptografar_mensagem(ip, lista_chaves[2])
        msg = Arquivo_objeto(objeto).gerar_arquivo_objeto()
        conexao.send(msg)

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def loop_servidor():
    """
    Gera as chaves do servidor de nomes
    """
    global lista_chaves
    lista_chaves.append(Funcoes_crypt().gerar_chaves_de_criptografia())
    
    """
    Gera a chave pública do servidor de nomes
    """
    lista_chaves.append(Funcoes_crypt().obter_chave_publica(lista_chaves[0]))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((settings.HOST_NOMES, settings.PORTA_ENVIO_SERVIDOR_NOMES))
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
    soquete.bind((settings.HOST_NOMES, settings.PORTA_NOMES))
    soquete.listen(settings.LISTEN)

    # Fica aqui aguardando novas conexões.
    while True:
        # Para cada nova conexão é criado um novo processo para tratar as requisições.
        Thread(target=trata_cliente, args=(soquete.accept())).start()


if __name__ == '__main__':
    print 'Servidor de Nomes Iniciou na Porta {0}'.format(settings.PORTA_NOMES)
    Thread(target=loop_servidor).start()
