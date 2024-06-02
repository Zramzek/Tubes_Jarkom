import socket
import threading

server_address = ('localhost', 8080)

def make_request(file_name):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        request = f"GET /{file_name} HTTP/1.1\r\nHost: {server_address[0]}\r\n\r\n"
        client_socket.send(request.encode())
        response = client_socket.recv(4096)
        print(f"Response for {file_name}:\n{response.decode()}\n")
    except Exception as e:
        print(f"An error occurred: {e}")

    client_socket.close()

file_names = ['index.html', 'index2.html', 'assets/buku.png', 'design.css']

threads = []

for file_name in file_names:
    thread = threading.Thread(target=make_request, args=(file_name,))
    thread.start()
    # threads.append(thread)

for thread in threads:
    thread.join()
