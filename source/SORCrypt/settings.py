#coding: utf-8

"""
Modulo responsavel pelas configuracoes globais do software.
"""

# Host (Ip do Servidor), PORTA (Porta do Servidor), LISTEN (maquinas)
HOST_NOMES = '127.0.0.1'
HOST_FUNCOES = '127.0.0.1'
HOST_CLIENTE = '127.0.0.1'
PORTA_NOMES = 4557
PORTA_FUNCOES = 3557
PORTA_ENVIO_CLIENTE = 8888
PORTA_RCV_CLIENTE = 8889
PORTA_ENVIO_SERVIDOR_NOMES = 9998
PORTA_RCV_SERVIDOR_NOMES = 9999
PORTA_ENVIO_SERVIDOR_FUNCOES = 7778
PORTA_RCV_SERVIDOR_FUNCOES = 7779
LISTEN = 5

# Tipos de Requisicoes do Cliente. Nao alterar.
SOMA = 'SOMA'
SUBTRACAO = 'SUBI'
PRODUTO = 'PROD'
DIVISAO = 'DIVI'
FATORIAL = 'FATO'
PORCENTAGEM = 'PORC'
FUNCOES = 'FUNC'

# Tamanho das Mensagens de requisicao.
TAM_MSG = 8889

SERVIDORES = '../arquivo/nomes.txt'
