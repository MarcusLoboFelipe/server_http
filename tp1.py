import os
import socket

def generate_directory_listing(directory):
    files = os.listdir(directory)
    file_list = "<ul>"
    for file in files:
        file_path = os.path.join(directory, file)
        file_url = file_path.replace(root_dir, '', 1).lstrip('/')
        if os.path.isdir(file_path):
            file += '/'
        file_list += f"<li><a href='{file_url}'>{file}</a></li>"
    file_list += "</ul>"
    return file_list

def generate_response(status, content_type, content):
    response = f"HTTP/1.1 {status}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += "Connection: close\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "\r\n"
    response += content.decode('utf-8')
    return response.encode('utf-8')

def get_content_type(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension == '.html':
        return 'text/html'
    elif extension == '.css':
        return 'text/css'
    elif extension == '.js':
        return 'text/javascript'
    elif extension == '.png':
        return 'image/png'
    elif extension == '.jpg' or extension == '.jpeg':
        return 'image/jpeg'
    elif extension == '.gif':
        return 'image/gif'
    else:
        return 'application/octet-stream'

def handle_request(client_socket, request, root_dir):
    request_lines = request.split('\r\n')
    if len(request_lines) > 0:
        request_parts = request_lines[0].split(' ')
        if len(request_parts) == 3:
            request_method, request_path, _ = request_parts
            if request_path == '/HEADER':
                headers = '\n'.join(request_lines[1:])
                response_content = headers.encode('utf-8')
                response = generate_response('200 OK', 'text/plain', response_content)
            else:
                file_path = os.path.join(root_dir, request_path.lstrip('/'))
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                    content_type = get_content_type(file_path)
                    response = generate_response('200 OK', content_type, file_content)
                elif os.path.isdir(file_path):
                    directory_listing = generate_directory_listing(file_path)
                    response = generate_response('200 OK', 'text/html', directory_listing.encode('utf-8'))
                else:
                    response_content = b"Error: Page not found"
                    response = generate_response('404 Not Found', 'text/plain', response_content)
        else:
            response_content = b"Error: Invalid request"
            response = generate_response('400 Bad Request', 'text/plain', response_content)
    else:
        response_content = b"Error: Invalid request"
        response = generate_response('400 Bad Request', 'text/plain', response_content)
    client_socket.sendall(response)

def run_server(host, port, root_dir):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server running on http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        handle_request(client_socket, request, root_dir)
        client_socket.close()

if __name__ == "__main__":
    root_dir = r'\Users\Marcu\Desktop\Teste'
    host = '172.18.186.48'
    port = 8000
    run_server(host, port, root_dir)
