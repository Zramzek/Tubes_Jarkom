from socket import *
import threading

def handle_connection(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()

        # Parsing request from client
        request_method = message.split()[0]
        file_requested = message.split()[1]

        # Default to index.html if the server is run with no specific file
        if file_requested == '/':
            file_requested = '/index.html'

        # Dictionary for mapping file extension to content type
        content_types = {
            'html': 'text/html',
            'png': 'image/png'
        }

        # Open the requested file
        file_extension = file_requested.split('.')[-1]
        file_path = file_requested[1:]  # Remove leading '/'

        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
            # Determine the content type
            content_type = content_types.get(file_extension, 'application/octet-stream')

            # Create the HTTP response message
            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n'
            response_content = file_content

        except IOError:
            # File not found, send 404 response
            with open('404.html', 'rb') as file:
                file_content = file.read()
            response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
            response_content = file_content

        # Send the HTTP response to the client
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_content)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        connectionSocket.close()

# Create TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to an address and port
serverHost = 'localhost'  # Local IP address
serverPort = 8080         # Port to use, changed from 80 to 8080

serverSocket.bind((serverHost, serverPort))

# Make the server socket ready to accept connections
serverSocket.listen(1)

print(f'Server running at http://{serverHost}:{serverPort}/')
while True:
    # Accept a new connection from a client
    connectionSocket, addr = serverSocket.accept()

    # Create a new thread to handle the connection
    t = threading.Thread(target=handle_connection, args=(connectionSocket,))
    t.start()