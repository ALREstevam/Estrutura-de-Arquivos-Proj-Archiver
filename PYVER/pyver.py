"""
- C1. Criar um archive com base em uma lista de arquivos informados.
– C2. Listar os nomes dos arquivos armazenados em um archive.
– C3. Extrair um arquivo de um archive, dado o nome do arquivo (sem remover esse arquivo de
dentro do archive).
– C4. Inserir um arquivo em um archive já criado.
– C5. Remover um arquivo de um archive, dado o nome do arquivo.
"""

import os
import struct
import sys

miniHeaderSize = 256
miniHeaderTrashSize = 0

sizeOfLongLong = len(struct.pack('q', 0))
sizeOfInteger = len(struct.pack('i', 0))
sizeOfUnsignedInteger = len(struct.pack('I', 0))

maxfnameSize = 256 - (2 * sizeOfLongLong + sizeOfInteger)
elemSize = maxfnameSize + 2 * sizeOfLongLong + sizeOfInteger

class HeaderElement:
    """Describes a element of the secondary header"""
    def __init__(self, fsize, fpos, fname, nextdeleted =-1):
        self.nextdeleted = nextdeleted
        self.fsize = fsize
        self.fPos = fpos
        self.fnameStr = self.shortFileName(maxfnameSize, fname)
        self.fname = self.encodeStrngTobBytes(self.fnameStr)

    def encodeStrngTobBytes(self, strng):
        return bytes((strng[0:maxfnameSize]).encode('utf-8'))

    def shortFileName(self, maxLen, fname):
        if len(fname) > maxLen:
            splitted = fname.split('.')
            extension = splitted[len(splitted) - 1]
            fname = fname[0:maxLen - len(extension) + 1]
            return '{}.{}'.format(fname, extension)
        else:
            return fname

    def __str__(self):
        return '\'{}\'` : [size: {}, pos: {}, nextDel: {}]'.format(
            self.fnameStr,
            self.fsize,
            self.fPos,
            self.nextdeleted
        )

class Packer:
    """
    Manages read and write operations into the archive
    """

    def __init__(self, archiveName):
        self.archiveName = archiveName
        self.headerPat = '=i q q ' + str(maxfnameSize) + 's'

    # Initiates the file
    def initFile(self):
        try:
            file = open(self.archiveName, 'wb')
            packedData = struct.pack('=I' + str(256 - sizeOfUnsignedInteger) + 's', 0, b'*')
            file.write(packedData)
            file.close()
        except:
            print('Error initializing the archive')
            input()
            exit(-1)

    def getHeaderByfname(self, fname):
        headers = self.retrieveHeader()
        for header in headers:
            if header.fnameStr == fname:
                return header
        raise AttributeError

    def getInfo(self):
        validFiles = 0
        deletedFiles = 0
        for header in self.retrieveHeader():
            if header.nextdeleted < 0:
                validFiles += 1
            else:
                deletedFiles += 1

        return[
                   ['primaryHeaderSize',      str(miniHeaderSize) + ' B'],
                   ['headerElementSize',      str(elemSize) + ' B'],
                   ['totalFiles',             self.elemsInHeader()],
                   ['secondaryHeaderSize',    str(self.elemsInHeader() * elemSize) + 'B'],
                   ['maxFnameSize',           str(maxfnameSize) + ' characters'],
                   ['validFiles',             validFiles],
                   ['deletedFiles',           deletedFiles],
                   ['totalFileSize',          str(Util(self.archiveName).fsize(self.archiveName)) + ' B']
               ]


    # Updates the amount of elements in the header
    def updtHeaderElemAmount(self, oldAmount, addedAmount):
        try:
            file = open(self.archiveName, 'r+b')
            newAmount = addedAmount + oldAmount
            packedData = struct.pack('I', newAmount)
            file.write(packedData)
            file.close()
        except:
            print('Error updating header.')
            input()
            exit(-1)

    # Return how many elements there are into the big header
    def elemsInHeader(self):
        """
        Return how many elements there are into the big header
        """
        return self.readElemsInHeader()

    # Returns a list of the header elements in the file
    def readElemsInHeader(self):
        """
        Returns a list of the header elements in the file
        """
        try:
            file = open(self.archiveName, 'rb')
            file.seek(0)
            packedData = file.read(4)
            unpackedData = struct.unpack('I', packedData)
            headerElements = unpackedData[0]
            return headerElements
        except Exception as e:
            print('Error occurred while reading the header.')
            input()
            exit(-1)

    def appendToHeader2(self, headElem):
        """
        Appends a header element to the archive
        """
        headerElemsCount = self.elemsInHeader()
        tup = (headElem.nextdeleted, headElem.fPos, headElem.fsize, headElem.fname)
        st = struct.Struct(self.headerPat)
        packedData = st.pack(*tup)
        self.updtHeaderElemAmount(self.elemsInHeader(), 1)

        try:
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
        except Exception:
            print('Error at appending an element to the header.')
            input()
            exit(-1)


    # Returns a list of headers (from the file)
    def retrieveHeader(self):
        """
        Returns a list of headers (from the file)
        """
        try:
            elemAmount = self.elemsInHeader()
            file = open(self.archiveName, 'rb')
            file.seek(miniHeaderSize)
            headerElements = []

            for i in range(elemAmount):
                data = file.read(elemSize)
                unpackedData = struct.unpack(self.headerPat, data)
                headElem = HeaderElement(unpackedData[2], unpackedData[1],
                                         unpackedData[3].decode('utf-8').rstrip(' \t\r\n\0'), unpackedData[0])
                headerElements.append(headElem)
            return headerElements
        except Exception:
            print('An error occurred while reading the header.')
            input()
            exit(-1)

    # Overwite a head element with the given one in a certain rrn
    def updateHeader(self, newHeader, rrn):
        """
        Overwite a head element with the given one in a certain rrn
        """
        try:
            file = open(self.archiveName, 'r+b')
            file.seek(miniHeaderSize + elemSize * rrn)
            tup = (newHeader.nextdeleted, newHeader.fPos, newHeader.fsize, newHeader.fname)
            formatation = self.headerPat
            st = struct.Struct(formatation)
            packedData = st.pack(*tup)
            file.write(packedData)
            file.close()
        except Exception:
            print('An error occurred while updating the header.')
            input()
            exit(-1)

    # Marks a file as deleted
    def delFile(self, fname):
        """
        Marks a file as deleted
        """
        headers = self.retrieveHeader()
        count = 0
        for header in headers:
            if header.fnameStr == fname:
                header.nextdeleted = count
                self.updateHeader(header, count)
                return True
            count += 1
        return False

     # Marks a file as not deleted
    def recFile(self, fname):
        """
        Marks a file as not deleted
        """
        headers = self.retrieveHeader()
        count = 0
        for header in headers:
            if header.fnameStr == fname:
                header.nextdeleted = -1
                self.updateHeader(header, count)
                return True
            count += 1
        return False

    def unpack(self, headerElem):
        """
        Unpacks a file from the archive
        """
        if headerElem.nextdeleted >= 0:
            return False

        relativePos = headerElem.fPos
        absolutePos = Util(self.archiveName).relativeToAbsolutePosition(relativePos)
        size = headerElem.fsize
        name = headerElem.fnameStr


        file = open(self.archiveName, 'rb')
        file.seek(absolutePos)
        data = file.read(size)
        file.close()

        if '\\' in name:
            os.makedirs(os.path.dirname(name), exist_ok=True)

        outFile = open(name, 'wb')
        outFile.write(data)
        outFile.close()
        return True


    def packAtTheEnd(self, fname):
        """
        Packs a file to the end of the archive
        """
        fsize = Util(self.archiveName).fsize(fname)

        if(fsize < 0):
            return -1

        arSize = Util(self.archiveName).fsize(self.archiveName)
        pos = Util(self.archiveName).absoluteToRelativePosition(arSize)
        rsp = HeaderElement(fsize, pos, fname, -1)

        bytesPerLoop = 4096
        loopCount = 0

        try:
            with open(self.archiveName, 'ab') as archive, open(fname, 'rb') as file:
                while True:
                    data = file.read(bytesPerLoop)  # read 4K
                    if data == b'':  # end of file reached
                        break
                    archive.write(data)
                    loopCount += 1
                    print('Read\Written: [{:^10} of {:^10}] [{:^3}%]'.format(
                        str(bytesPerLoop * loopCount) + ' B',
                        str(fsize) + ' B',
                        '100' if (bytesPerLoop * loopCount) * 100 // fsize > 100 else (
                         bytesPerLoop * loopCount) * 100 // fsize
                        , end='\r'))
            return rsp
        except Exception:
            raise Exception



class Util:
    """
    This is a utility class
    """
    def __init__(self, archiveName):
        self.archiveName = archiveName
        self.pk = Packer(archiveName)

    def fsize(self, fname):
        """
        Calculate a size of a file
        """
        if os.path.exists(fname):
            return os.path.getsize(fname)
        else:
            return -1

    def relativeToAbsolutePosition(self, relativePos):
        """
        Converts a relative position in the archive to the absolute position
        """
        headerElems = self.pk.elemsInHeader()
        return relativePos + miniHeaderSize + (elemSize * headerElems)

    def absoluteToRelativePosition(self, absolutePos):
        """
        Converts a absolute position in the archive to the relative position
        """
        headerElems = self.pk.elemsInHeader()
        return absolutePos - (miniHeaderSize + (elemSize * headerElems))

    def fileExists(self, fname):
        """
        Returns true only if the file exists
        """
        return os.path.exists(fname)


    #def filesExists(self, files):
    #    for file in files:
    #        if not self.fileExists(file):
    #            print('File does not exists: {}'.format(file))


class TextInterface:
    """
    This class generates the text interface and comunicate with the classes that manage the archive
    """
    def __init__(self):
        self.archiveName = 'defaultArchiver.pyver'

        if len(sys.argv) == 1:
            print('You have not entered any commands')
            print('Try: `open <archivename>.pyver` to open a already initiated archive')
            print('Try: `init <archivename>` to initializes a new archive')
            input()
            exit(0)

        elif len(sys.argv) == 3:
            auxArchiveName = sys.argv[2]
            self.archiveName = auxArchiveName

            if sys.argv[1] == 'init':
                self.archiveName += '.pyver'
                p = Packer(self.archiveName)
                p.initFile()

        self.pk = Packer(self.archiveName)
        self.util = Util(self.archiveName)

        print('\n\n\n{:^50}\n'.format('***[ PYVER BASH ]***'))
        print('Selected archive: [{}]'.format(self.archiveName))

        print('\nTip: type `help` for displaying the help message.')

        while True:
            inpt = self.getUserInput()
            inpt[0] = inpt[0].lower()

            if len(inpt) == 1:
                inpt.append('')



            ## EXIT
            if inpt[0] == 'exit' or inpt[0] == 'close':
                exit(0)

            ## INFO
            elif inpt[0] == 'info':
                info = self.pk.getInfo()

                for line in info:
                    print('{:30}:{:>20}'.format(line[0], line[1]))

            ## SHOW HELP
            elif inpt[0] == 'help' or inpt[0] == 'hlp':
                self.printHelp()

            ## FILE IS IN THE ARCHIVE
            elif inpt[0] == 'exists':
                pk = self.pk
                try:
                    if pk.getHeaderByfname(inpt[1]):
                        rsp = '[ Yes ]'
                        print(rsp)
                    else:
                        rsp = '[ No  ]'
                        print(rsp)
                except:
                    print('An error occurred while looking for the file [{}] in the archive\'s header.'.format(inpt[1]))

            ## LIST FILES
            elif inpt[0] == 'list' or inpt[0] == 'ls':
                self.describeNonDeletedFiles()

            ## LIST ALL FILES
            elif inpt[0] == 'listall' or inpt[0] == 'la':
                self.describeAllFiles()

            ## DELETE FILE
            elif inpt[0] == 'del' or inpt[0] == 'rm' or inpt[0] == 'remove':
                print('Deleting [{}]'.format(inpt[1]))
                if self.pk.delFile(inpt[1]):
                    print('Deleted with success.')
                else:
                    print('An error occurred, the file could not be deleted.')


            ## RECOVERY FILE
            elif inpt[0] == 'rec' or inpt[0] == 'recover' or inpt[0] == 'undelete':
                print('Recovering [{}]'.format(inpt[1]))
                if self.pk.recFile(inpt[1]):
                    print('Reovered with success.')
                else:
                    print('An error occurred, the file could not be recovered.')


            ## ARCHIVE FILE
            elif inpt[0] == 'archive' or inpt[0] == 'ar' or inpt[0] == 'pack' or inpt[0] == 'pk' or inpt[0] == 'append' or inpt[0] == 'add' or inpt[0] == 'arc':
                print('Inserting files...')
                for i in range(1, len(inpt)):
                    try:
                        print("Archiving file: [{}]...".format(inpt[i]))
                        insetedHead = self.pk.packAtTheEnd(inpt[i])
                        self.pk.appendToHeader2(insetedHead)
                        print("[{}] was successfully archived.".format(inpt[i]))
                    except Exception:
                        print('Error: File {} could not be archived.'.format(inpt[i]))


            ## UNPACK FIILE
            elif inpt[0] == 'unpack' or inpt[0] == 'un':
                try:
                    print('Unpacking file: [{}]'.format(inpt[1]))
                    headElem = self.pk.getHeaderByfname(inpt[1])
                    self.pk.unpack(headElem)
                    print("[{}] was successfully unpacked.".format(inpt[1]))
                except Exception:
                    print('Error: File {} could not be unpacked.'.format(inpt[1]))
            else:
                print('Unknown command, try using:')
                self.printHelp()



    def printHelp(self):
        """
        Print the help message
        """
        print('\n{:^94}'.format('[ COMMANDS ]'))
        print('-'*94)
        print("{:42}  {:50}".format('help     hlp', 'prints this list'))
        print("{:42}  {:50}".format('exit     close', 'closes the bash'))
        print("{:42}  {:50}".format('list     ls', 'lists the stored files'))
        print("{:42}  {:50}".format('listall  la', 'lists all the stored files (including the deleted files)'))
        print("{:42}  {:50}".format('archive  ar    pack    pk <filename>...', 'adds the files to the archive'))
        print("{:42}  {:50}".format('del      rm <filename>', 'deletes a file from the archive'))
        print("{:42}  {:50}".format('rec      recover    undelete <filename>', 'recovers a deleted file'))
        print("{:42}  {:50}".format('unpack   un <filename>', 'extracts a file from the archive'))
        print("{:42}  {:50}".format('exists <filename>', 'checks if the given file it\'s inside the archive'))
        print("{:42}  {:50}".format('info', 'prints information about the archive'))


    def describeAllFiles(self):
        """
        Prints a description of all the files in the archive
        """
        totalFiles = self.pk.elemsInHeader()

        headers = self.pk.retrieveHeader()
        count = 0
        print('\n\n')
        totalSize = os.path.getsize(self.archiveName)

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
        """
        Prints a description of the non-deleted files
        """
        totalFiles = self.pk.elemsInHeader()
        headers = self.pk.retrieveHeader()
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
        return str(input('\n\n>> ')).split(' ')


#sys.argv = ['', 'init', 'afile'] #uncomment this for debug
userTextInterface = TextInterface()
