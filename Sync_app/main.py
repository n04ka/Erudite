from multiprocessing import Process, Pipe
from multiprocessing.connection import PipeConnection
from threading import Thread
import customtkinter as tk
from time import sleep


class Task:

    def __init__(self, conn: PipeConnection) -> None:
        self._conn = conn
        self._progress = 0
        self._paused = True
        self._finished = False
        listener = Thread(target=self.listener, daemon=True)
        sender = Thread(target=self.sender, daemon=True)
        task = Thread(target=self.task, daemon=True)
        listener.start()
        print('task listener ON')
        sender.start()
        print('task sender ON')
        task.start()
        print('task task ON')
        listener.join()
        print('task listener OFF')
        sender.join()
        print('task sender OFF')
        task.join()
        print('task task OFF')
    

    def task(self):
        while self._progress < 1 and not self._finished:
            if not self._paused:
                sleep(0.5)
                self._progress += 0.1
        self._finished = True


    def listener(self):
        while self._conn.poll(None):
            match self._conn.recv():
                case 'Start':
                    self._paused = False
                case 'Stop':
                    self._paused = True
                case 'Finished':
                    self._paused = True
                    self._finished = True
                    exit()

    
    def sender(self):
        while not self._finished:
            self._conn.send(self._progress)
            sleep(0.1)
        self._conn.send('Finished')
            

class GUI:

    def __init__(self, conn: PipeConnection) -> None:
        self.app = tk.CTk()
        app = self.app
        app.title("Синхронизатор")
        app.geometry('500x300')
        app.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._conn = conn
        self._listen = True

        self.main_frame = tk.CTkFrame(app)
        self.control_butt = tk.CTkButton(self.main_frame, text="Start", command=self.butt_callback)
        self.progress_bar = tk.CTkProgressBar(self.main_frame)
        self.progress_bar.set(0)
        
        self.display()
        listener = Thread(target=self.listener, daemon=True)
        listener.start()
        print('gui listener ON')
        print('mainloop ON')
        app.mainloop()
        

    def on_closing(self):
        self._listen = False
        self._conn.send('Finished')
        self.app.destroy()
        print('gui mainloop OFF')
        print('gui listener OFF')
        exit()


    def listener(self):
        progress = 0
        while self._listen and progress < 1:
            if self._conn.poll(0.1):
                progress = self._conn.recv()
                if progress == 'Finished':
                    break
                try:
                    self.progress_bar.set(progress)
                except RuntimeError:
                    break
        self.control_butt.configure(text='Finished')
        self._conn.send('Finished')


    def butt_callback(self):
        match self.control_butt._text:
            case 'Start':
                self._conn.send('Start')
                self.control_butt.configure(text='Stop')
            case 'Stop':
                self._conn.send('Stop')
                self.control_butt.configure(text='Start')
            case 'Finished':
                self.on_closing()


    def display(self):
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.control_butt.pack(padx=8, pady=8, fill='x')
        self.progress_bar.pack(padx=8, pady=8, fill='x')


def main():
    conn1, conn2 = Pipe()
    task_proc = Process(target=Task, args=[conn1], daemon=True)
    gui_proc = Process(target=GUI, args=[conn2])
    task_proc.start()
    gui_proc.start()
    task_proc.join()
    print('task_proc finished')
    gui_proc.join()
    print('gui_proc finished')
    

if __name__ == '__main__':
    main()
