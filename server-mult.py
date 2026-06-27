from socket import *
from constCS import *
import threading

def is_palindromo(text):
    if text == text[::-1]:
        return "Palindromo"
    return "Não é Palindromo"

def processa_comando(comando):
    """Processa um único comando no formato 'opção:texto' e retorna o resultado."""
    try:
        # Divide opção e texto
        if ':' not in comando:
            return "Erro: formato inválido (use opcao:texto)"
        partes = comando.split(':', 1)
        op = int(partes[0])
        texto = partes[1]
    except ValueError:
        return "Erro: operação deve ser um número"

    if op == 1:
        return is_palindromo(texto)
    elif op == 2:
        return texto.upper()
    elif op == 3:
        return texto.lower()
    else:
        return "Operação Inválida"

def atende_cliente(conn, addr):
    """Função executada por cada thread para lidar com um cliente."""
    print(f"Thread iniciada para {addr}")
    try:
        # Lê uma linha da conexão (o comando)
        data = conn.recv(1024)
        if not data:
            return
        comando = bytes.decode(data).strip()
        print(f"[{addr}] Comando recebido: {comando}")

        resposta = processa_comando(comando)
        # Envia resposta com quebra de linha
        conn.send(str.encode(resposta + '\n'))
    except Exception as e:
        print(f"Erro ao atender {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexão com {addr} encerrada")

def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)  # Permite até 5 conexões pendentes
    print(f"Servidor multithread ouvindo em {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        # Cria uma thread para o cliente conectado
        t = threading.Thread(target=atende_cliente, args=(conn, addr))
        t.daemon = True  # Thread será encerrada quando o principal finalizar
        t.start()

if __name__ == "__main__":
    main()