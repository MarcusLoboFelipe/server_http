import socket
import os

directory = "/scratch/convidado/Área de Trabalho"

port = 8000

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    request_parts = request.split(" ")

    if request_parts[0] == "GET":
        if request_parts[1] == "/HEADER":
            header = "HTTP/1.1 200 OK\nContent-type: text/plain\n\n"
            response = header + str(request)
            client_socket.sendall(response.encode())
        else:
            path = directory + request_parts[1]
            if os.path.isfile(path):
                with open(path, "rb") as file:
                    data = file.read()
                    header = "HTTP/1.1 200 OK\nContent-type: application/octet-stream\nContent-Disposition: attachment; filename=" + os.path.basename(path) + "\n\n"
                    response = header.encode() + data
                    client_socket.sendall(response)
            else:
                if os.path.isdir(path):
                    file_list = os.listdir(path)
                    file_links = "<br>".join([f"<a href='{os.path.basename(file)}'>{os.path.basename(file)}</a>" for file in file_list])
                    html = f"<html><body>{file_links}</body></html>"
                    header = "HTTP/1.1 200 OK\nContent-type: text/html\n\n"
                    response = header + html
                    client_socket.sendall(response.encode())
                else:
                    response = "HTTP/1.1 404 Not Found\nContent-type: text/plain\n\n404 Not Found"
                    client_socket.sendall(response.encode())
    else:
        response = "HTTP/1.1 400 Bad Request\nContent-type: text/plain\n\n400 Bad Request"
        client_socket.sendall(response.encode())

    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(("", port))

server_socket.listen(1)
print(f"Servidor iniciado na porta {port}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        handle_request(client_socket)
except KeyboardInterrupt:
    pass

server_socket.close()

