import socket
import sys
import time


# create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s


def main():
    s = create_tcp_socket()
    s.connect(("127.0.0.1", 8001))
    s.sendall(f'GET / HTTP/1.0\r\nHost: 142.251.33.100\r\n\r\n'.encode())
    while True:

        msg = s.recv(2048)

        if msg == b"":
            s.close()
            break

        print(msg)


if __name__ == "__main__":
    main()
