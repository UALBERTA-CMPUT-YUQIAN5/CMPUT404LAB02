import socket
import sys


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


def main():
    # connect to proxy server
    s = create_tcp_socket()
    s.connect(("127.0.0.1", 8001))

    # send payload to proxy server
    s.sendall(f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'.encode())

    # continue accepting data until no more left
    full_data = b""
    while True:
        data = s.recv(2048)
        if not data:
            break
        full_data += data
    print(full_data)


if __name__ == "__main__":
    main()
