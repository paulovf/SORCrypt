#coding: utf-8

"""
Modulo responsavel por criar as interface gráficas do software.
"""

import gtk
import settings
from cliente import realiza_operacao


class Calculadora:
    """
    Interface Gráfica da Calculadora do SORCrypt.
    """

    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("SORCrypt")
        self.window.set_size_request(250, 250)
        self.window.connect("destroy",gtk.main_quit)

        self.tabela = gtk.Table(6,4,False)
        self.window.add(self.tabela) 	

        self.campoTexto = gtk.Entry()
        self.campoTexto.set_size_request(10, 30)
        self.tabela.attach(self.campoTexto,0,4,0,1)

        self.botaoCE = gtk.Button("CE")
        self.tabela.attach(self.botaoCE, 0,1,1,2) 
        self.botaoCE.connect("clicked",self.calcular,"CE")

        self.botaoClr = gtk.Button("Clr")
        self.tabela.attach(self.botaoClr,1,2,1,2)
        self.botaoClr.connect("clicked",self.calcular,"Clr")

        self.botaoFat = gtk.Button("Fat")
        self.tabela.attach(self.botaoFat,2,3,1,2)
        self.botaoFat.connect("clicked",self.calcular, "Fat")

        self.botaoPor = gtk.Button("%")
        self.tabela.attach(self.botaoPor,3,4,1,2)
        self.botaoPor.connect("clicked",self.calcular,"%")

        self.botao7 = gtk.Button("7")
        self.tabela.attach(self.botao7,0,1,2,3)
        self.botao7.connect("clicked",self.insereCampoTexto,"7")

        self.botao8 = gtk.Button("8")
        self.tabela.attach(self.botao8,1,2,2,3)
        self.botao8.connect("clicked",self.insereCampoTexto,"8")

        self.botao9 = gtk.Button("9")
        self.tabela.attach(self.botao9,2,3,2,3)
        self.botao9.connect("clicked",self.insereCampoTexto,"9")

        self.botaoDiv = gtk.Button("/")
        self.tabela.attach(self.botaoDiv,3,4,2,3)
        self.botaoDiv.connect("clicked",self.calcular,"/")

        self.botao4 = gtk.Button("4")
        self.tabela.attach(self.botao4,0,1,3,4)
        self.botao4.connect("clicked",self.insereCampoTexto,"4")

        self.botao5 = gtk.Button("5")
        self.tabela.attach(self.botao5,1,2,3,4)
        self.botao5.connect("clicked",self.insereCampoTexto,"5")

        self.botao6 = gtk.Button("6")
        self.tabela.attach(self.botao6,2,3,3,4)
        self.botao6.connect("clicked",self.insereCampoTexto,"6")

        self.botaoMult = gtk.Button("*")
        self.tabela.attach(self.botaoMult,3,4,3,4)
        self.botaoMult.connect("clicked",self.calcular,"*")

        self.botao1 = gtk.Button("1")
        self.tabela.attach(self.botao1,0,1,4,5)
        self.botao1.connect("clicked",self.insereCampoTexto,"1")

        self.botao2 = gtk.Button("2")
        self.tabela.attach(self.botao2,1,2,4,5)
        self.botao2.connect("clicked",self.insereCampoTexto,"2")

        self.botao3 = gtk.Button("3")
        self.tabela.attach(self.botao3,2,3,4,5)
        self.botao3.connect("clicked",self.insereCampoTexto,"3")

        self.botaoMenos = gtk.Button("-")
        self.tabela.attach(self.botaoMenos,3,4,4,5)
        self.botaoMenos.connect("clicked",self.calcular,"-")

        self.botao0 = gtk.Button("0")
        self.tabela.attach(self.botao0,0,1,5,6)
        self.botao0.connect("clicked",self.insereCampoTexto,"0")

        self.botaoPonto = gtk.Button(".")
        self.tabela.attach(self.botaoPonto,1,2,5,6)
        self.botaoPonto.connect("clicked",self.insereCampoTexto,".")

        self.botaoIgual = gtk.Button("=")
        self.tabela.attach(self.botaoIgual,2,3,5,6)
        self.botaoIgual.connect("clicked",self.calcular,'=')

        self.botaoMais = gtk.Button("+")
        self.tabela.attach(self.botaoMais,3,4,5,6)
        self.botaoMais.connect("clicked",self.calcular,"+")

        self.window.show_all()
        
    def insereCampoTexto(self, widget, operacao):
        """
        Atualiza o texto atual do campo de texto.
        """
        self.campoTexto.insert_text(operacao, position = 20)

    def calcular(self, widget, operacao):
        """
        Realiza as operações necessárias da calculadora.
        """
        if operacao == 'Clr':
	        self.campoTexto.set_text("")
        elif operacao == 'CE':
	        self.campoTexto.set_text("0")		
        elif operacao == '+':
	        self.tipoOperacao = 1
	        self.primeiraOperacao = self.campoTexto.get_text()
	        self.campoTexto.set_text("")
        elif operacao == '-':
	        self.tipoOperacao = 2
	        self.primeiraOperacao = self.campoTexto.get_text()
	        self.campoTexto.set_text("")
        elif operacao == '*':
	        self.tipoOperacao = 3
	        self.primeiraOperacao = self.campoTexto.get_text()
	        self.campoTexto.set_text("")
        elif operacao == '/':
	        self.tipoOperacao = 4
	        self.primeiraOperacao = self.campoTexto.get_text()
	        self.campoTexto.set_text("")
        elif operacao == '%':
	        self.tipoOperacao = 5
	        self.primeiraOperacao = self.campoTexto.get_text()
	        self.campoTexto.set_text("")
        elif operacao == 'Fat':
            self.tipoOperacao = 6
            self.primeiraOperacao = self.campoTexto.get_text()
            self.campoTexto.set_text("")
        elif operacao == '=':
            self.segundaOperacao = self.campoTexto.get_text()
            n1 = self.primeiraOperacao
            n2 = self.segundaOperacao
            resultado = 0
            if self.tipoOperacao == 1:
                resultado = realiza_operacao(settings.SOMA, n1, n2)
            elif self.tipoOperacao == 2:
                resultado = realiza_operacao(settings.SUBTRACAO, n1, n2)
            elif self.tipoOperacao == 3:
                resultado = realiza_operacao(settings.PRODUTO, n1, n2)
            elif self.tipoOperacao == 4:
                resultado = realiza_operacao(settings.DIVISAO, n1, n2)
            elif self.tipoOperacao == 5:
                resultado = realiza_operacao(settings.PORCENTAGEM, n1, n2)
            elif self.tipoOperacao == 6:
                resultado = realiza_operacao(settings.FATORIAL, n1, n2)
            self.campoTexto.set_text(str(resultado))


if __name__ == "__main__":
	c = Calculadora()
	gtk.main()