
"""
# Problemas
* Precisamos de dados no começo do arquivo para dizer quandos elementos de cabeçalho o arquivo tem
    * Assim é possível fazer um `seek(pos: 256, bytes:n*256)` e dividir em `n` registros de cabeçalho
* Ao adicionar um registro de cabeçalho precisamos empurrar o resto do arquivo
    * Inserir no meio é complicado: reescrever todo o arquivo
        * Sobrescrever ou inserir no final é mais simples
        * Inserir no final não resolve o problema
    * Estudar como incluir espaços vazios no fim do cabeçalho
        * **Ex:**
            1. Guardar no cabeçalho menor
                * Quantidade de espaços usados no cabeçaho maior
                * Quantidade de espaços total
            2. Quando o espaço estiver acabando aumentar o espaço vago em x% do espaço total
* Se for feito o uso da alocação pelo worst fit
    * Organizar listas é fácil
    * Criar novos registros a partir da quebra de um deletado não é tanto
    * Vale a pena unir registros vizinhos que estão deletados

* Fazer storage compaction pode ser mais fácil que usar worst fit mas
    * É preciso reescrever todo o arquivo, o que não é tão simples
        * Ler e colocar lado a lado registros válidos
        * Reorganizar dados do cabeçaho

* Na maior parte dos sistemas de arquivos o maior nome do arquivo é 255B
        * Mas se definirmos o máximo como 244 é possível fazer com que cada registro do header tenha 256B

* O nome dos arquivos precisa ser uma string de tamanho fixo
        * Se não for fica muito difícil de gerenciar o cabeçalho

----

# ORGANIZAÇÃO DO ARQUIVO

Header primário
(x1)
[int: qtd de registros no header secundário ] 256B

Header secundário
(x qtd de arquivos deletados e não deletados)
[int: próximo deletado | long: tamanho do arquivo | long: posição no arquivo | string(244): nome do arquivo] 256B

Arquivos
[bytes(n).......][bytes(n1)...][bytes(n2)...]
Arquivos de tamanho variável referenciados pelo header secundário

---

--header prim-|--------------------header sec-------------------------|--------files------------|
[HEADER0_256B][[HEADER_ELEM_256B][HEADER_ELEM_256B][HEADER_ELEM_256B]][FILE_nB][FILE_nB][FILE_nB]


"""









class HeaderElement:
    def __init__(self, fname, fpos, fsize, fValid):
        self.fileName = fname
        self.filePosition = fpos #The first byte of the first file should be 0, not headerSize + 1!
        self.fileSize = fsize
        #self.isValid = fValid


class Header:
    def __init__(self):
        ar = Archiver()
        self.fHeaders = ar.readHeader(ar.readHeaderSize())

class Archiver:
    def readHeader(self):
        size = self.readHeaderSize()
        data = self.readData(0, size)

        # Create an list of HeaderElement objects
        return False

    def readHeaderSize(self):
        return 0

    def readData(self, pos, bytes):
        return False

    def calcOffset(self, headerSize, fPos):
        return fPos + headerSize

    def addFile(self, fname):
        return False

    def defFile(self, fname):
        return False

    def listNonDeletedFiles(self):
        return False

    def listAllFiles(self):
        return False

    def recoveryFile(self, fname):
        return False

    def storageCompation(self):
        return False

    def updateHeader(self, header):
        return False


class Interface:
    def readArgs(self, args):
        '''Case arg do...'''



