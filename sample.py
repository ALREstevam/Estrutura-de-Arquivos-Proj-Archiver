"""
- C1. Criar um archive com base em uma lista de arquivos informados.
– C2. Listar os nomes dos arquivos armazenados em um archive.
– C3. Extrair um arquivo de um archive, dado o nome do arquivo (sem remover esse arquivo de
dentro do archive).
– C4. Inserir um arquivo em um archive já criado.
– C5. Remover um arquivo de um archive, dado o nome do arquivo.

from texttable import Texttable
t = Texttable()
t.add_rows([['Name', 'Age'], ['Alice', 24], ['Bob', 19]])
print t.draw()
"""

import struct
import os
import sys


maxfnameSize = 244
miniHeaderSize = 256
elemSize = 256


class HeaderElement:
    def __init__(self, fsize, fpos, fname, nextdeleted = -1):
        self.nextdeleted = nextdeleted
        self.fsize = fsize
        self.fPos = fpos
        self.fname = self.encodeStrngTobBytes(fname)
        self.fnameStr = fname[0:maxfnameSize]
        # TODO: recuperar a extensão do arquivo caso o tamanho seja maior que o máximo

    def encodeStrngTobBytes(self, strng):
        return bytes((strng[0:maxfnameSize]).encode('utf-8'))

class Packer:
    """
    Manages the header packing and unpacking operations
    """

    def __init__(self, archiveName):
        self.archiveName = archiveName

    # Initiates the file
    def initFile(self):
        file = open(self.archiveName, 'wb')
        packedData = struct.pack('I  252s', 0, b'*')
        print(len(packedData))
        file.write(packedData)
        file.close()

    def getHeaderByfname(self, fname):
        headers = self.retrieveHeader()
        for header in headers:
            if header.fnameStr == fname:
                return header
        return False


    # Updates the amount of elements in the header
    def updtHeaderElemAmount(self, oldAmount, addedAmount):
        file = open(self.archiveName, 'r+b')
        #file.seek(0)
        newAmount = addedAmount + oldAmount
        packedData = struct.pack('I', newAmount)
        file.write(packedData)
        file.close()

    # Return how many elements there are into the big header
    def elemsInHeader(self):
        return self.readElemsInHeader()
        # TODO: keep the amount of header elements in memory


    def readElemsInHeader(self):
        file = open(self.archiveName, 'rb')
        file.seek(0)
        packedData = file.read(4)
        unpackedData = struct.unpack('I', packedData)
        headerElements = unpackedData[0]
        return headerElements

    # Append a new header element to the end of the file
    # TODO: this will not work with the data of the inserted files in the end of the archive!
    def appendToHeader(self, headElem):
        file = open(self.archiveName, 'a+b')
        tup = (headElem.nextdeleted, headElem.fPos, headElem.fsize, headElem.fname)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        file.write(packedData)
        file.close()
        self.updtHeaderElemAmount(pk.elemsInHeader(), 1)

    def appendToHeader2(self, headElem):
        headerElemsCount = self.elemsInHeader()
        tup = (headElem.nextdeleted, headElem.fPos, headElem.fsize, headElem.fname)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        self.updtHeaderElemAmount(pk.elemsInHeader(), 1)

        file = open(self.archiveName, 'rb')
        data = file.read()
        file.close()

        bkPos = miniHeaderSize + headerElemsCount * elemSize
        lst = [data[0:bkPos], packedData, data[bkPos:]]

        newData = b''
        for dt in lst:
            newData += dt

        file = open(self.archiveName, 'wb')
        file.write(newData)
        file.close()


        print(data)
        print(newData)

    # Returns a list of headers (from the file)
    def retrieveHeader(self):
        elemAmount = self.elemsInHeader()
        file = open(self.archiveName, 'rb')
        file.seek(miniHeaderSize)
        headerElements = []

        for i in range(elemAmount):
            data = file.read(elemSize)
            unpackedData = struct.unpack('i l l 244s', data)
            headElem  = HeaderElement(unpackedData[2], unpackedData[1], unpackedData[3].decode('utf-8').rstrip(' \t\r\n\0'), unpackedData[0])
            headerElements.append(headElem)

        return headerElements

    # Overwite a head element with the given one in a certain rrn
    def updateHeader(self, newHeader, rrn):
        file = open(self.archiveName, 'r+b')
        file.seek(miniHeaderSize + elemSize * rrn)
        tup = (newHeader.nextdeleted, newHeader.fPos, newHeader.fsize, newHeader.fname)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        file.write(packedData)
        file.close()

    # Marks a file as deleted
    # TODO: worst fit
    def delFile(self, fname):
        headers = self.retrieveHeader()
        count = 0
        for header in headers:
            print('[' + header.fnameStr + '] == [' + fname + ']')
            print(header.fnameStr == fname)
            print(header.fnameStr is fname)
            print(bytes(header.fnameStr.encode('utf-8')))
            print(bytes(fname.encode('utf-8')))

            if header.fnameStr == fname:
                print('FOUND')
                header.nextdeleted = 0
                self.updateHeader(header, count)
                return True
            else:
                print('NOT FOUND YET')
            count += 1
        return False

    # TODO: leitura de 4 em 4 k (não trazer o arquivo lido para memória)
    def read(self, filename):
        file = open(filename, 'rb')
        data = file.readlines()
        file.close()
        return data

    def unpack(self, headerElem):
        headerElems = self.elemsInHeader()
        relativePos = headerElem.fPos
        absolutePos = relativePos + miniHeaderSize + (elemSize * headerElems)
        size = headerElem.fsize
        name = headerElem.fnameStr

        data = b''
        file = open(self.archiveName, 'rb')
        file.seek(absolutePos)
        data = file.read(size)
        file.close()

        outFile = open(name, 'wb')
        outFile.write(data)
        outFile.close()

    def packAtTheEnd(self, fname):
        fsize = Util().fsize(fname)

        if(fsize < 0):
            return -1

        data = self.read(fname)
        arSize = Util().fsize(self.archiveName)
        pos = Util().absoluteToRelativePosition(arSize)

        rsp = HeaderElement(fsize, pos, fname, -1)

        archive = open(self.archiveName, 'ab')
        archive.write(bytes(data))

class Util:
    def __init__(self):
        pass

    def fsize(self, fname):
        if(os.path.exists(fname)):
            return os.path.getsize(fname)
        else:
            return -1

    def relativeToAbsolutePosition(self, relativePos):
        headerElems = Packer().elemsInHeader()
        return relativePos + miniHeaderSize + (elemSize * headerElems)

    def absoluteToRelativePosition(self, absolutePos):
        headerElems = Packer().elemsInHeader()
        return absolutePos - miniHeaderSize + (elemSize * headerElems)

    def fileExists(self, fname):
        return os.path.exists(fname)

    def filesExists(self, files):
        for file in files:
            if not self.fileExists(file):
                print('File does not exists: {}'.format(file))


class TextInterface:
    def __init__(self):

        if len(sys.argv) == 1:
            print('Use open|init <archivename>')
            print('{:20s} : opens a already initiated archive'.format('open'))
            print('{:20s} : initializes a new archive'.format('init'))

        elif len(sys.argv) == 3:
            auxArchiveName = sys.argv[2]
            #auxArchiveName = 'arc.pyver'
            archiveName = auxArchiveName

            if sys.argv[1] == 'init':
                p = Packer()
                p.initFile()




        print('\n\n\n{:^50}'.format('--- PYVER ---'))
        print('Open archive: {}'.format(archiveName))
        print('Use `help` for help.')
        # self.printHelp()

        while True:
            inpt = self.getUserInput()

            if inpt[0] == 'exit' or inpt[0] == 'close':
                exit(0)
            elif inpt[0] == 'list' or inpt[0] == 'ls':
                self.describeNonDeletedFiles()
            elif inpt[0] == 'listall' or inpt[0] == 'la':
                self.describeAllFiles()
            elif inpt[0] == 'archive' or inpt[0] == 'ar' or inpt[0] == 'pack' or inpt[0] == 'pk':
                pass
            elif inpt[0] == 'del' or inpt[0] == 'rm':
                for i in range(1, len(inpt) - 1):
                    Packer().delFile(inpt[i])
            elif inpt[0] == 'unpack' or inpt[0] == 'un':
                headElem = Packer.getHeaderByfname(inpt[1])
                if headElem:
                    FileHandler().unpack(headElem)

            elif inpt[0] == 'exists':
                pk = Packer()
                rsp = ''

                if pk.getHeaderByfname(inpt[1]):
                    rsp = 'Yes'
                else:
                    rsp = 'No'

                print(rsp)

            elif inpt[0] == 'help' or inpt[0] == 'hlp':
                self.printHelp()
            else:
                print('Unknown command, try using:')
                self.printHelp()



    def printHelp(self):
        print('\nCommands'.upper())
        print("{:40} : closes the application".format('exit | close'))
        print("{:40} : lists the stored files".format('list | ls'))
        print("{:40} : lists all the stored files (including the deleted files)".format('listall | la'))
        print("{:40} : adds the files to the archive".format('archive | ar | pack | pk <filename>...'))
        print("{:40} : deletes a file from the archive".format('del | rm <filename>'))
        print("{:40} : extracts a file from the archive".format('unpack | un <filename>'))
        print("{:40} : Check if the given file it's in the archive".format('exists <filename>'))
        print("{:40} : Shows this list".format('help | hlp'))

    def describeAllFiles(self):
        totalFiles = Packer().elemsInHeader()

        headers = Packer().retrieveHeader()
        count = 0
        print('\n\n')
        totalSize = os.path.getsize(archiveName)

        print('Total files: {}\t|\tArchive total size: {}B'.format(totalFiles, totalSize))
        print('{:4s} {:25s} {:6s} {:5s} {:5s}'.format('Num', 'File Name', 'Size', 'Pos', 'isDeleted'))
        for header in headers:
            print('{:3}. {:25s} {:5}B {:5} {:5s}'
                .format(
                count,
                str(header.fnameStr[0:30]),
                header.fsize,
                header.fPos,
                str(header.nextdeleted > -1)
            )
            )

            count += 1
        print('\n')

    # Prints a description of the non-deleted files
    def describeNonDeletedFiles(self):
        totalFiles = Packer().elemsInHeader()
        headers = Packer().retrieveHeader()
        count = 0
        print('\n\n')
        print('Total files: {:}'.format(totalFiles))
        print('{:4s} {:30s} {:6s} {:5s}'.format('Num', 'File Name', 'Size', 'Pos'))
        for header in headers:
            if header.nextdeleted < 0:
                print('{:3}. [{:30s}] [{:5}B] [{:5}]'
                    .format(
                    count,
                    str(header.fnameStr[0:30]),
                    header.fsize,
                    header.fPos,
                )
                )
            count += 1
        print('\n')



    def getUserInput(self):
        return str(input('>> ')).split(' ')






pk = Packer()
fl = FileHandler()
uti = TextInterface()


h1 = HeaderElement(5, 0, "aaa.txt")
h2 = HeaderElement(15, 0, "b.txt")
h3 = HeaderElement(35, 0, "c.c")
h4 = HeaderElement(55, 0, "a.bin")
h5 = HeaderElement(90, 0, "jirojorel.png")

fl.unpack(h5)


pk.initFile()
pk.appendToHeader2(h1)
pk.appendToHeader2(h2)
pk.appendToHeader2(h3)
pk.appendToHeader2(h4)
pk.appendToHeader2(h5)

print('\n' + 100 * '=' + '\n\n')
print(pk.elemsInHeader())
headers = pk.retrieveHeader()
uti.describeAllFiles()
pk.delFile('aaa.txt')
uti.describeAllFiles()


readed = fl.read('sampeFile.x')
print(readed)

