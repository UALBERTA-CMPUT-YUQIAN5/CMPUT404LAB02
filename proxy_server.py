import socket
import sys
from multiprocessing import Process, active_children

# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 2048


# create a tcp socket
def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        sys.exit()
    return s


# get host information
def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        sys.exit()
    return remote_ip


# send data to server
def send_data(serversocket, payload):
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        sys.exit()


# get data from google
def get_google(payload):
    try:
        # define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        buffer_size = 4096

        # make the socket, get the ip, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip, port))
        print(f'Socket Connected to {host} on ip {remote_ip}')

        # send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        # continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            full_data += data
        return full_data
    except Exception as e:
        print(e)
    finally:
        # always close at the end!
        s.close()


# handler thread for an incoming connection
def handle_connection(conn):
    client_data = conn.recv(BUFFER_SIZE).decode()

    google_data = get_google(client_data)
    conn.sendall(google_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to address
        s.bind((HOST, PORT))
        # set to listening mode
        s.listen(2)

        # join all finished thread
        active_children()

        # continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            p = Process(target=handle_connection, args=(conn, ))
            p.start()


if __name__ == "__main__":
    main()
