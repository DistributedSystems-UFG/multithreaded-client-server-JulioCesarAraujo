from socket  import *
from constCS import * 
import random as rd

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT)) 

# Enviando os 4 comandos de uma vez
mensagem = '1:arara,1:a base do teto desaba,1:rodou na prancha'
s.send(str.encode(mensagem))  

# Como enviamos 4 comandos separados por vírgula, esperamos 4 respostas
total_respostas_esperadas = 4   # <--- ALTERAÇÃO AQUI: de 3 para 4

print("Aguardando respostas do servidor...")

# Usa makefile para ler linha por linha de forma fácil
entrada = s.makefile('r', encoding='utf-8')

for i in range(total_respostas_esperadas):
    linha = entrada.readline()
    if not linha:             # conexão fechada antes de receber todas
        break
    print(f"Resposta {i+1}: {linha.strip()}")

s.close()