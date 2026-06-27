from socket import *
from constCS import *
import threading
import random as rd
import time
import argparse

def envia_requisicao(servidor, porta, comando, indice):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((servidor, porta))
        s.send(str.encode(comando))
        data = s.recv(1024)
        resposta = bytes.decode(data).strip()
        s.close()
    except Exception as e:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--single', action='store_true', help='Modo single-thread (servidor sequencial)')
    parser.add_argument('--multi', action='store_true', default=True, help='Modo multi-thread (servidor paralelo)')
    args = parser.parse_args()

    templates = [
        '1:arara',
        '1:a base do teto desaba',
        '2:isso e uma frase',
        '1:otto'
    ]

    num_req = rd.randint(0, 1000)
    comandos = []
    i = 0
    while i < num_req:
        req_random = rd.randint(1, 3)
        row_random = rd.randint(0, 3)
        comandos.append(f"{req_random}:{templates[row_random]}")
        i += 1

    if args.single:
        print(f"[SINGLE-THREAD] Enviando {len(comandos)} requisições sequencialmente...")
        start = time.time()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        mensagem = ','.join(comandos)
        s.send(str.encode(mensagem))
        total_respostas = len(comandos)
        entrada = s.makefile('r', encoding='utf-8')
        for _ in range(total_respostas):
            entrada.readline()
        s.close()
        end = time.time()
        print(f"[SINGLE-THREAD] Tempo total: {end - start:.4f}s para {len(comandos)} requisições")
    else:
        print(f"[MULTI-THREAD] Enviando {len(comandos)} requisições em paralelo...")
        start = time.time()
        threads = []
        for i, comando in enumerate(comandos):
            t = threading.Thread(target=envia_requisicao, args=(HOST, PORT, comando, i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        print(f"[MULTI-THREAD] Tempo total: {end - start:.4f}s para {len(comandos)} requisições")

if __name__ == "__main__":
    main()