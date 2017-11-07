# # Testes com o módulo struct
# (https://www.youtube.com/watch?v=eTOw-Cw_VkI)[https://www.youtube.com/watch?v=eTOw-Cw_VkI]
# ()[]

import struct
print(ord('p'))
x = b'bytestring'
print(x)
print(x[0])

#open('anyfile', 'wb')
#struct: bytes, float, int e string

nome = 'Jão'
idade = 20
altura = 1.87

# cod = struct.pack(fmt = formato, valores...)

cod = struct.pack('10s I f', nome.encode(), idade, altura)
print(cod)

# 4s = uma string de 4 caracteres (precisa estar no formado de bytes)
# I integer
# f float

arq = open('pessoas.cod', 'wb')
print(arq.write(cod))
arq.close()
arq = open('pessoas.cod', 'rb')
cod_rb = arq.readline()
print(cod_rb)
cod_desemp = struct.unpack('10s I f', cod_rb)
print(cod_desemp)
nome = cod_desemp[0].decode()
print(nome)


"""
Format	C Type	            Python type	            Standard size
x	    pad byte	        no value
c	    char	            string of length 1	        1
b	    signed char	        integer	                    1
B	    unsigned char	    integer	                    1
?	    _Bool	            bool	                    1
h	    short	            integer	                    2
H	    unsigned short	    integer	                    2
i	    int	                integer	                    4
I	    unsigned int	    integer	                    4
l	    long	            integer	                    4
L	    unsigned long	    integer	                    4
q	    long long	        integer	                    8
Q	    unsigned long long	integer	                    8
f	    float	            float	                    4
d	    double	            float	                    8
s	    char[]	            string
p	    char[]	            string
P	    void *	            integer
"""

print(30*'-')
# # Empacotando tuplas

nome = 'Jãos'.encode('utf-8')
nome = bytes(nome)

print(nome)
tup = (nome, 23, 1.75)
strct = struct.Struct('10s I f')
packedData = strct.pack(*tup)
print(packedData)
unpackedData = strct.unpack(packedData)

print(unpackedData)