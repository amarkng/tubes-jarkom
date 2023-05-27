import socket
import os

def main():
    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Mengaitkan socket ke alamat dan port tertentu
    server_socket.bind(('localhost', 8080))
    # Mengatur socket untuk mendengarkan koneksi masuk
    server_socket.listen(1)

    print("Web server berjalan di http://localhost:8080")

    # Loop utama untuk menerima koneksi dari client
    while True:
        # Menerima koneksi dari client
        client_socket, client_address = server_socket.accept()
        # Menerima data request dari client dan mendekode menjadi string
        request = client_socket.recv(1024).decode()
        print(request)

        # Memproses request dan menghasilkan response
        http_response = handle_request(request)
        # Mengirim response ke client
        client_socket.sendall(http_response)
        # Menutup koneksi dengan client
        client_socket.close()

def handle_request(request):
    # Memisahkan baris dalam request
    request_lines = request.split('\r\n')
    # Mengambil baris pertama (request line)
    request_line = request_lines[0]
    # Memisahkan method, path, dan versi HTTP dari request line
    method, path, version = request_line.split(' ')

    # Menggantikan path dengan index.html jika path adalah "/"
    if path == "/":
        path = "/index.html"

    # Mencoba membuka file yang diminta
    try:
        # Membaca konten file
        with open(os.path.join('TUBES', path[1:]), 'rb') as file:
            content = file.read()
            # Membuat response header untuk file yang ditemukan
            response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {get_content_type(path)}\r\n\r\n"
    # Jika file tidak ditemukan
    except FileNotFoundError:
        # Membuat konten untuk pesan 404 Not Found
        print("404 Error..")
        content = b"<h1>404 Not Found</h1>"
        # Membuat response header untuk pesan 404 Not Found
        response_header = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n"
		
    # Menggabungkan response header dan konten untuk menghasilkan response lengkap
    http_response = response_header.encode() + content
    return http_response

def get_content_type(path):
    # Mengembalikan tipe konten berdasarkan ekstensi file
    if path.endswith(".html"):
        return "text/html"
    elif path.endswith(".css"):
        return "text/css"
    else:
        return "application/octet-stream"

if __name__ == "__main__":
    main()
