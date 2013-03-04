#coding: utf-8
import pickle

"""
módulo responsável por converter objetos em arquivos para que possam 
ser enviados por um socket
"""

class Arquivo_objeto:
    """
    Esta classe fornece os métodos de geração e leitura de arquivos 
    de objetos
    """
    
    def __init__(self, objeto):
        self.objeto = objeto
        self.arquivo = None

    def obter_objeto_arquivo(self):
        """
        Obtém o objeto enviado via socket e retorna o objeto
        para criptografia original
        """
        self.arquivo = file('../arquivo/arquivo_objeto', 'wb')
        self.arquivo.write(self.objeto)
        self.arquivo.close()
       
        return pickle.load(file('../arquivo/arquivo_objeto', 'rb'))
        
    def gerar_arquivo_objeto(self):
        """
        Esta função cira umarquivo para que o objeto gerador de chaves
        possa ser enviado por um socket
        """
            
        self.arquivo = open('../arquivo/arquivo_objeto.rlp', 'wb')
        pickle.dump(self.objeto, self.arquivo)
        self.arquivo.close()
                
        return open('../arquivo/arquivo_objeto.rlp', 'rb').read()    
