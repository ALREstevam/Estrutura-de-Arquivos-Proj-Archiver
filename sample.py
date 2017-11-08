'''
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
'''

import struct
import os

archiveName = 'arch.ar'
maxfNameSize = 244
miniHeaderSize = 256
elemSize = 256

class HeaderElement:
    """
    Describes a element of the big header
    """
    def __init__(self, fSize, fpos, fName, nextDeleted = -1):
        self.nextDeleted = nextDeleted
        self.fSize = fSize
        self.fPos = fpos
        self.fName = self.encodeStrngTobBytes(fName)
        self.fNameStr = fName[0:maxfNameSize]

    def encodeStrngTobBytes(self, strng):
        return bytes((strng[0:maxfNameSize]).encode('utf-8'))

class Packer:
    """
    Manages the header packing and unpacking operations
    """
    # Initiates the file
    def initFile(self):
        file = open(archiveName, 'wb')
        packedData = struct.pack('I  252s', 0, b'*')
        print(len(packedData))
        file.write(packedData)
        file.close()

    # Updates the amount of elements in the header
    def updtHeaderElemAmount(self, oldAmount, addedAmount):
        file = open(archiveName, 'r+b')
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
        file = open(archiveName, 'rb')
        file.seek(0)
        packedData = file.read(4)
        unpackedData = struct.unpack('I', packedData)
        headerElements = unpackedData[0]
        return headerElements

    # Append a new header element to the end of the file
    # TODO: this will not work with the data of the inserted files in the end of the archive!
    def appendToHeader(self, headElem):
        file = open(archiveName, 'a+b')
        tup = (headElem.nextDeleted, headElem.fPos, headElem.fSize, headElem.fName)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        file.write(packedData)
        file.close()
        self.updtHeaderElemAmount(pk.elemsInHeader(), 1)

    def appendToHeader2(self, headElem):
        headerElemsCount = self.elemsInHeader()
        tup = (headElem.nextDeleted, headElem.fPos, headElem.fSize, headElem.fName)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        self.updtHeaderElemAmount(pk.elemsInHeader(), 1)

        file = open(archiveName, 'rb')
        data = file.read()
        file.close()

        bkPos = miniHeaderSize + headerElemsCount * elemSize
        lst = [data[0:bkPos], packedData, data[bkPos:]]

        newData = b''
        for dt in lst:
            newData += dt

        file = open(archiveName, 'wb')
        file.write(newData)
        file.close()


        print(data)
        print(newData)

    # Returns a list of headers (from the file)
    def retrieveHeader(self):
        elemAmount = self.elemsInHeader()
        file = open(archiveName, 'rb')
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
        file = open(archiveName, 'r+b')
        file.seek(miniHeaderSize + elemSize * rrn)
        tup = (newHeader.nextDeleted, newHeader.fPos, newHeader.fSize, newHeader.fName)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        file.write(packedData)
        file.close()

    # Marks a file as deleted
    # TODO: worst fit
    def delFile(self, fName):
        headers = self.retrieveHeader()
        count = 0
        for header in headers:
            print('[' + header.fNameStr + '] == [' + fName + ']')
            print(header.fNameStr == fName)
            print(header.fNameStr is fName)
            print(bytes(header.fNameStr.encode('utf-8')))
            print(bytes(fName.encode('utf-8')))

            if header.fNameStr == fName:
                print('FOUND')
                header.nextDeleted = 0
                self.updateHeader(header, count)
                return True
            else:
                print('NOT FOUND YET')
            count += 1
        return False

    # Prints a description of all files (deleted and not deleted)
    def describeAllFiles(self):
        totalFiles = self.elemsInHeader()

        headers = self.retrieveHeader()
        count = 0
        print('\n\n')
        totalSize = os.path.getsize(archiveName)

        print('Total files: {}\t|\tArchive total size: {}B'.format(totalFiles, totalSize))
        print('{:4s} {:25s} {:6s} {:5s} {:5s}'.format('Num', 'File Name', 'Size', 'Pos', 'isDeleted'))
        for header in headers:
            print('{:3}. {:25s} {:5}B {:5} {:5s}'
                .format(
                    count,
                    str(header.fNameStr[0:30]),
                    header.fSize,
                    header.fPos,
                    str(header.nextDeleted > -1)
                )
            )

            count += 1
        print('\n')

    # Prints a description of the non-deleted files
    def describeNonDeletedFiles(self):
        totalFiles = self.elemsInHeader()
        headers = self.retrieveHeader()
        count = 0
        print('\n\n')
        print('Total files: {:}'.format(totalFiles))
        print('{:4s} {:25s} {:6s} {:5s}'.format('Num', 'File Name', 'Size', 'Pos'))
        for header in headers:
            if header.nextDeleted < 0:
                print('{:3}. [{:30s}] [{:5}B] [{:5}]'
                    .format(
                        count,
                        str(header.fNameStr[0:30]),
                        header.fSize,
                        header.fPos,
                    )
                )
            count += 1
        print('\n')


class FileHandler:
    def __init__(self):
        pass

    def read(self, filename):
        file = open(filename, 'rb')
        data = file.readlines()
        file.close()
        return data

    def unpack(self, headerElem):
        pk = Packer()
        headerElems = pk.elemsInHeader()

        file = open(archiveName, 'rb')
        file.close()

pk = Packer()



h1 = HeaderElement(5, 0, "aaa.txt")
h2 = HeaderElement(15, 0, "b.txt")
h3 = HeaderElement(35, 0, "c.c")
h4 = HeaderElement(55, 0, "a.bin")
h5 = HeaderElement(90, 0, "jirojorel.png")


pk.initFile()
pk.appendToHeader2(h1)
pk.appendToHeader2(h2)
pk.appendToHeader2(h3)
pk.appendToHeader2(h4)
pk.appendToHeader2(h5)

print('\n' + 100 * '=' + '\n\n')
print(pk.elemsInHeader())
headers = pk.retrieveHeader()
pk.describeAllFiles()
pk.delFile('aaa.txt')
pk.describeAllFiles()

fl = FileHandler()
readed = fl.read('sampeFile.x')
print(readed)

