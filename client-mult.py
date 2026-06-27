from socket import *
from constCS import *
import threading
import random as rd

def envia_requisicao(servidor, porta, comando, indice):
    """Envia um comando para o servidor e imprime a resposta."""
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((servidor, porta))
        s.send(str.encode(comando))
        data = s.recv(1024)
        resposta = bytes.decode(data).strip()
        print(f"[Thread {indice}] Resposta: {resposta}")
        s.close()
    except Exception as e:
        print(f"[Thread {indice}] Erro: {e}")

def main():
    # Lista de comandos a enviar (cada um será uma requisição)
    comandos = [
        '1:arara',
        '1:a base do teto desaba',
        '2:isso e uma frase',
        '1:otto'
    ]
    # Fazendo arranjo entre requisições de tipo 1, 2 e 3 com as frases de comandos. 
    num_req = rd.randint(0, 1000) # Numero suficientemente grande
    i = 0 
    while i < num_req:
        req_random = rd.randint(1,3)
        row_random = rd.randint(0,3)
        comandos.append(f"{req_random}:{comandos[row_random]}")
        i+=1

    # Aqui pode definir servidores diferentes para cada comando
    servidores = [
        (HOST, PORT),  # servidor 1
        # (OUTRO_HOST, OUTRA_PORTA),  # servidor 2, etc.
    ]

    print("Enviando requisições em paralelo...")
    threads = []
    for i, comando in enumerate(comandos):
        # Escolhe o servidor: se houver vários, pode usar (i % len(servidores))
        servidor, porta = servidores[i % len(servidores)]
        t = threading.Thread(
            target=envia_requisicao,
            args=(servidor, porta, comando, i)
        )
        threads.append(t)
        t.start()

    # Aguarda todas as threads finalizarem
    for t in threads:
        t.join()

    print("Todas as requisições concluídas.")

if __name__ == "__main__":
    main()