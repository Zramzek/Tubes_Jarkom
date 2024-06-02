from socket import *
import threading

def handle_connection(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()

        request_method = message.split()[0]
        file_requested = message.split()[1]

        if file_requested == '/':
            file_requested = '/index.html'

        content_types = {
            'html': 'text/html',
            'png': 'image/png',
        }

        file_extension = file_requested.split('.')[-1]
        file_path = file_requested[1:]

        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
            content_type = content_types.get(file_extension, 'application/octet-stream')

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n'
            response_content = file_content

        except IOError:
            with open('404.html', 'rb') as file:
                file_content = file.read()
            response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
            response_content = file_content

        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_content)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)

serverHost = 'localhost'  
serverPort = 8080        

serverSocket.bind((serverHost, serverPort))

serverSocket.listen(1)

print(f'Server running at http://{serverHost}:{serverPort}/')
while True:
    connectionSocket, addr = serverSocket.accept()

    t = threading.Thread(target=handle_connection, args=(connectionSocket,))
    t.start()