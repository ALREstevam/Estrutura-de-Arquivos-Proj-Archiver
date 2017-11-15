def initialize():
    fileText = open('orig.txt', 'w')
    txtStr = 'Uma string de texto normal'
    txtStr2 = '\nOutra string'

    print('\nESCREVENDO EM MODO TEXTO')
    print(txtStr)
    print(txtStr2)

    fileText.write(txtStr)
    fileText.write(txtStr2)
    fileText.close()

    fileBin = open('orig.bin', 'wb')
    rec = bytes('Uma string de texto em binário'.encode('utf-8'))
    rec1 = bytes('\nOutra string de texto em binário'.encode('utf-8'))

    print('\nESCREVENDO EM MODO BINÁRIO')
    print(rec)
    print(rec1)
    fileBin.write(rec)
    fileBin.write(rec1)
    fileBin.close()


def toOutput(originalFileName, newFileName,):
    fContent = open(originalFileName, 'rb')
    fOut = open(newFileName, 'wb')

    content = fContent.readlines()
    print('\nLENDO DO ARQUIVO DE ENTRADA:\n {}\n\n'.format(content))

    for elem in content:
        print('W na saída: {}'.format(elem))
        fOut.write(elem)

    fContent.close()
    fOut.close()

initialize()
toOutput('orig.bin', 'out.bin')
toOutput('orig.txt', 'out.txt')
toOutput('img1.png', 'outimg.png')
toOutput('index.html', 'outIndex.html')

