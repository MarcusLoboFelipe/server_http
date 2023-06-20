import os
from flask import Flask, request, send_from_directory

app = Flask(__name__)

root_dir = '/Users/Marcu/Desktop'

@app.route('/')
def list_files():
    return generate_directory_listing(root_dir)

@app.route('/<path:path>')
def download_file(path):
    file_path = os.path.join(root_dir, path)

    if os.path.isfile(file_path):
        return send_from_directory(root_dir, path, as_attachment=True)
    elif os.path.isdir(file_path):
        return generate_directory_listing(file_path)
    else:
        return "Erro: Página não encontrada", 404

@app.route('/HEADER')
def show_header():
    headers = request.headers  
    header_list = "<br>".join([f"{header}: {value}" for header, value in headers.items()])
    return header_list

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

if __name__ == "__main__":
    app.run(host='172.18.186.48', port=8000, debug=False)
