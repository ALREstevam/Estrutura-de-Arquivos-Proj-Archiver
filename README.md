# Estrutura-de-Arquivos-Proj-Archiver
Archiver desenvolvido em Python para a disciplina de Estrutura de Arquivos

----

# ST562 – Estruturas de Arquivos
## Prof. Dr. Celmar Guimarães da Silva
### Trabalho 1
**Valor: 10 pontos**
* Trabalho: em grupos de até 5 pessoas.
* **Objetivo:** Implementar um programa arquivador, ou seja, um gerenciador de archives.

### Descrição:
Um archive é um “arquivo de arquivos”; ou seja, é um arquivo que contém uma coleção de outros
arquivos, em uma estrutura que torna possível recuperar individualmente cada arquivo nele
armazenado [1]. Um arquivador (archiver) é um programa que permite criar e modificar archives, bem
como extrair arquivos de um archive.
Nesse contexto, a tarefa deste projeto é fazer um arquivador que implemente os seguintes casos de
uso:
* C1. Criar um archive com base em uma lista de arquivos informados.
* C2. Listar os nomes dos arquivos armazenados em um archive.
* C3. Extrair um arquivo de um archive, dado o nome do arquivo (sem remover esse arquivo de dentro do archive).
* C4. Inserir um arquivo em um archive já criado.
* C5. Remover um arquivo de um archive, dado o nome do arquivo.

### Relatório:
O programa deve vir acompanhado de relatório sobre quais casos de uso foram implementados, e
respectivas comprovações (trecho de código e tela de execução).
Data de entrega: vide cronograma da disciplina.
Referências:
[1] Man page do comando ar. Disponível em [https://man.cx/ar](https://man.cx/ar) (16/10/2017).
