import zmq
from library.sha1Structure import *

def main():
    # Address for each server to receive files
    servAddresses = []

    context = zmq.Context()
    servers = context.socket(zmq.REP)
    servers.bind("tcp://*:5555")

    clients = context.socket(zmq.REP)
    clients.bind("tcp://*:6666")

    poller = zmq.Poller()
    poller.register(servers, zmq.POLLIN)
    poller.register(clients, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        if clients in socks:
            print("Message from client")
            operation, *msg = clients.recv_multipart()
            if operation == b"availableServers":
                clients.send_multipart(servAddresses)
            print(msg)

            if(operation == b"uploadShas"):
                fileName, completeSha1, btCompleteSha1 = clients.recv_multipart()


        if servers in socks:
            print("Message from server")
            operation, *rest = servers.recv_multipart()
            if operation == b"newServer":
                servAddresses.append(rest[0])
                print(servAddresses)
                servers.send(b"Ok")


if __name__ == '__main__':
    main()
