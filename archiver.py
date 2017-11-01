class HeaderElement:
    def __init__(self, fname, fpos, fsize, fValid):
        self.fileName = fname
        self.filePosition = fpos #The first byte of the first file should be 0, not headerSize + 1!
        self.fileSize = fsize
        self.isValid = fValid


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



