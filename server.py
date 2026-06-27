from socket import *
from constCS import *

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("Servidor aguardando conexão...")
(conn, addr) = s.accept()
print(f"Conectado por: {addr}")

def is_palindromo(text):
    # Adicionado retorno explicitamente caso não seja palíndromo
    text = text.replace(' ', '')
    if text == text[::-1]: 
        return "Palindromo"
    return "Não é Palindromo"

while True:
    data = conn.recv(1024)
    if not data: 
        break
    
    data_str = bytes.decode(data)
    # Remove espaços ou quebras de linha nas pontas e divide por vírgula
    tokens = data_str.strip().split(",") 
    print(f"Tokens recebidos: {tokens}")
    
    for e in tokens:
        # Pula elementos vazios (como o gerado por uma vírgula no final da string)
        if not e or ":" not in e:
            continue
            
        op = e.split(":")
        
        # Garante que op tem exatamente 2 partes antes de continuar
        if len(op) < 2:
            continue
            
        print(f"Processando comando -> Opção: {op[0]}, Texto: {op[1]}")
        
        try:
            cmd = int(op[0])
            texto = str(op[1])
            
            if cmd == 1: 
                r = is_palindromo(texto)
            elif cmd == 2: 
                r = texto.upper()
            elif cmd == 3: 
                r = texto.lower()
            else: 
                r = "Operação Inválida"
        except ValueError:
            r = "Erro: Operação deve ser um número"
            
        # Envia a resposta + quebra de linha para o cliente
        conn.send(str.encode(str(r) + '\n')) 

conn.close()