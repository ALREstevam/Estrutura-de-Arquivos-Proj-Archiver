import struct
data0 = {'nextDeletd': 500, 'fSize': 600, 'fPos': 153, 'fName': "aaaaa.txt"}
data1 = {'nextDeletd': 500, 'fSize': 600, 'fPos': 153, 'fName': "aaaaa.txt"}
data2 = {'nextDeletd': 500, 'fSize': 600, 'fPos': 153, 'fName': "aaaaa.txt"}

archiveName = 'arch.ar'

class HeaderElement:
    def __init__(self, fSize, fpos, fname, nextDeleted = -1):
        self.nextDeleted = nextDeleted
        self.fSize = fSize
        self.fpos = fpos
        self.fname = bytes((fname[0:255]).encode('utf-8'))




class Packer:
    def initFile(self):
        file = open(archiveName, 'wb')
        packedData = struct.pack('I 252s', 0, b'*')
        file.write(packedData)
        file.close()


    def updtHeaderElemAmount(self, newCount):
        file = open(archiveName, 'r+b')
        file.seek(0)
        packedData = file.read(4)
        unpackedData = struct.unpack('I', packedData)
        newAmount = unpackedData[0] + newCount
        packedData = struct.pack('I', newAmount)
        print('===')
        print(packedData)
        file.write(packedData)
        file.close()

    def elemsInHeader(self):
        file = open(archiveName, 'rb')
        file.seek(0)
        packedData = file.read(256)
        unpackedData = struct.unpack('I 252s', packedData)
        return unpackedData[0]


    def appendToHeader(self, headElem):
        file = open(archiveName, 'a+b')
        tup = (headElem.nextDeleted, headElem.fpos, headElem.fSize, headElem.fname)
        formatation = 'i l l 244s'
        st = struct.Struct(formatation)
        packedData = st.pack(*tup)
        file.write(packedData)
        file.close()

    def retriveHeader(self):
        file = open(archiveName, 'rb')


pk = Packer()

h1 = HeaderElement(5, 0, "aaa.txt")
h2 = HeaderElement(15, 0, "b.txt")
h3 = HeaderElement(35, 0, "c.c")
h4 = HeaderElement(55, 0, "a.bin")


pk.initFile()
pk.appendToHeader(h1)
pk.appendToHeader(h2)
pk.appendToHeader(h3)
pk.appendToHeader(h4)

print(pk.elemsInHeader())

pk.updtHeaderElemAmount(100)

print(pk.elemsInHeader())