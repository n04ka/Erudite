from multiprocessing import Process, Pipe
from multiprocessing.connection import PipeConnection
from threading import Thread
from time import sleep

class Phone:

    def __init__(self, conn: PipeConnection, name: str, time: float) -> None:
        self.conn = conn
        self.name = name
        self.time = time
        self.listen = Thread(target=self.listener)
        self.send = Thread(target=self.sender)
        self.listen.start()
        self.send.start()
        self.listen.join()
        self.send.join()

    
    def listener(self):
        while self.conn.poll(2):
            data = self.conn.recv()
            print(f'I am {self.name} and I recieved: {data}')
        print(f'I am {self.name} and I am done with this')


    def sender(self):
        while self.listen.is_alive():
            self.conn.send(f"Hello from {self.name}")
            sleep(self.time)


if __name__ == '__main__':
    conn1, conn2 = Pipe()
    p1 = Process(target=Phone, args=(conn1, "Zebra", 1))
    p2 = Process(target=Phone, args=(conn2, "Giraffe", 2.5))
    p1.start()
    p2.start()
    p1.join()
    p2.join()