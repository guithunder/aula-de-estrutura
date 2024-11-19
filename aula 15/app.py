from http.server import BaseHTTPRequestHandler, HTTPServer
import json

#CLASSE para gerenciar filas de atendimento

class FilaAtendimento:
    def __init__(self):
        self.fila = []
        self.proximo_numero = 1

    def gerar_senha(self):
        senha = self.proximo_numero
        self.fila.append(senha)
        self.proximo_numero += 1
        return senha
    
    def antender_cliente(self):
        if self.fila:
            return self.fila.pop(0)
        return None
        
        
# listar todas as senhas 

class FilaAtendimentoHandler(BaseHTTPRequestHandler):
    fila_atendimento = FilaAtendimento()
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        
    def do_POST(self):
        if self.path == "/gera-senha":
            senha = self.fila_atendimento.gerar_senha() 
            self._set_headers(201)
            self.wfile.write(json.dumps({"senha": senha}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Rota nao encontrada"}))   
    
    def do_GET(self):
        if self.path == "/chamar-senha":
            senha = self.fila_atendimento.antender_cliente()
            if senha:
                self._set_headers(200)
                self.wfile.write(json.dumps({"senha": senha}).encode())
            else:
                self._set_headers(204)
                self.wfile.write(json.dumps({"message": "Não há senhas na fila."}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Rota não encontrada."}).encode())

    
    
    
def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, FilaAtendimentoHandler) 
    print("Servidor iniciado na porta 8080")
    httpd.serve_forever()
    
if __name__ == "__main__":
    run()  # Inicia o servidor HTTP
    
    
