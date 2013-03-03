#coding: utf-8

"""
Modulo responsavel por criar as interface gráficas do software.
"""

from gi.repository import Gtk, Gdk
import settings
from cliente import realiza_operacao


class Calculadora:
    """
    Interface Gráfica da Calculadora do SORCrypt.
    """

    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("SORCrypt")
        self.window.set_size_request(250, 280)
        self.window.connect("destroy",Gtk.main_quit)
        self.window.set_resizable(False)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.toolbar = CustomToolbar()
        self.toolbar.set_hexpand(True)

        self.botaoHelp = Gtk.ToolButton(stock_id=Gtk.STOCK_HELP)
        self.botaoHelp.set_is_important(True)
        self.botaoHelp.set_label('Sobre o SORCrypt')
        self.botaoHelp.connect('clicked', self.chamar_help, self.window)
        
        self.botaoQuit = Gtk.ToolButton(stock_id=Gtk.STOCK_QUIT)
        self.botaoQuit.set_is_important(True)
        self.botaoQuit.connect('clicked', Gtk.main_quit)

        self.toolbar.insert(self.botaoHelp, 0)
        self.toolbar.insert(self.botaoQuit, 1)

        self.tabela = Gtk.Table(6,4,False)

        self.campoTexto = Gtk.Entry()
        self.campoTexto.set_size_request(10, 30)
        self.tabela.attach(self.campoTexto,0,4,0,1)

        self.botaoCE = Gtk.Button("CE")
        self.tabela.attach(self.botaoCE, 0,1,1,2) 
        self.botaoCE.connect("clicked",self.calcular,"CE")

        self.botaoClr = Gtk.Button("Clr")
        self.tabela.attach(self.botaoClr,1,2,1,2)
        self.botaoClr.connect("clicked",self.calcular,"Clr")

        self.botaoFat = Gtk.Button("Fat")
        self.tabela.attach(self.botaoFat,2,3,1,2)
        self.botaoFat.connect("clicked",self.calcular, "Fat")

        self.botaoPor = Gtk.Button("%")
        self.tabela.attach(self.botaoPor,3,4,1,2)
        self.botaoPor.connect("clicked",self.calcular,"%")

        self.botao7 = Gtk.Button("7")
        self.tabela.attach(self.botao7,0,1,2,3)
        self.botao7.connect("clicked",self.insereCampoTexto,"7")

        self.botao8 = Gtk.Button("8")
        self.tabela.attach(self.botao8,1,2,2,3)
        self.botao8.connect("clicked",self.insereCampoTexto,"8")

        self.botao9 = Gtk.Button("9")
        self.tabela.attach(self.botao9,2,3,2,3)
        self.botao9.connect("clicked",self.insereCampoTexto,"9")

        self.botaoDiv = Gtk.Button("/")
        self.tabela.attach(self.botaoDiv,3,4,2,3)
        self.botaoDiv.connect("clicked",self.calcular,"/")

        self.botao4 = Gtk.Button("4")
        self.tabela.attach(self.botao4,0,1,3,4)
        self.botao4.connect("clicked",self.insereCampoTexto,"4")

        self.botao5 = Gtk.Button("5")
        self.tabela.attach(self.botao5,1,2,3,4)
        self.botao5.connect("clicked",self.insereCampoTexto,"5")

        self.botao6 = Gtk.Button("6")
        self.tabela.attach(self.botao6,2,3,3,4)
        self.botao6.connect("clicked",self.insereCampoTexto,"6")

        self.botaoMult = Gtk.Button("*")
        self.tabela.attach(self.botaoMult,3,4,3,4)
        self.botaoMult.connect("clicked",self.calcular,"*")

        self.botao1 = Gtk.Button("1")
        self.tabela.attach(self.botao1,0,1,4,5)
        self.botao1.connect("clicked",self.insereCampoTexto,"1")

        self.botao2 = Gtk.Button("2")
        self.tabela.attach(self.botao2,1,2,4,5)
        self.botao2.connect("clicked",self.insereCampoTexto,"2")

        self.botao3 = Gtk.Button("3")
        self.tabela.attach(self.botao3,2,3,4,5)
        self.botao3.connect("clicked",self.insereCampoTexto,"3")

        self.botaoMenos = Gtk.Button("-")
        self.tabela.attach(self.botaoMenos,3,4,4,5)
        self.botaoMenos.connect("clicked",self.calcular,"-")

        self.botao0 = Gtk.Button("0")
        self.tabela.attach(self.botao0,0,1,5,6)
        self.botao0.connect("clicked",self.insereCampoTexto,"0")

        self.botaoPonto = Gtk.Button(".")
        self.tabela.attach(self.botaoPonto,1,2,5,6)
        self.botaoPonto.connect("clicked",self.insereCampoTexto,".")

        self.botaoIgual = Gtk.Button("=")
        self.tabela.attach(self.botaoIgual,2,3,5,6)
        self.botaoIgual.connect("clicked",self.calcular,'=')

        self.botaoMais = Gtk.Button("+")
        self.tabela.attach(self.botaoMais,3,4,5,6)
        self.botaoMais.connect("clicked",self.calcular,"+")

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.layout.pack_start(self.toolbar, False, False, 0)
        self.layout.pack_end(self.tabela, True, True, 0)

        self.window.add(self.layout)

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

    def chamar_help(self, evento, janela):
        DialogoHelp(janela)


def DialogoHelp(janela):
    """
    Exibe um dialogo de informações do software.
    """
    dialogo = Gtk.MessageDialog(janela, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text='Informacoes do Software')
    dialogo.set_title('SORCrypt')
    dialogo.format_secondary_text('Nome:\nServidor de Operacoes Remotas Criptografadas\n\nDesenvolvedores:\nCharles Tim Batista Garrocho\nPaulo Vitor Francisco')
    dialogo.run()
    dialogo.destroy()


class CustomToolbar(Gtk.Toolbar):
    """
    Instancia uma ToolBar customizada.
    """

    def __init__(self):
        """
        Configurando o Estilo do Toolbar.
        """
        super(CustomToolbar, self).__init__()
        context = self.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

    def insert(self, item, pos):
        """
        Verifica se o item e uma instancia do Gtk.ToolItem antes de coloca-lo no toolbar.
        """
        if not isinstance(item, Gtk.ToolItem):
            widget = Gtk.ToolItem()
            widget.add(item)
            item = widget

        super(CustomToolbar, self).insert(item, pos)
        return item


if __name__ == "__main__":
	c = Calculadora()
	Gtk.main()