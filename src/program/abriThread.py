import threading


        
class Abrifast():
    def __init__(self):
        self.queu = []

    def add(self, function, name):
        self.queu.append((name, threading.Thread(target=function)))


    def info(self):
        for thread in self.queu:
            print(thread[0], ' : ', thread[1])

    def run(self):
        for thread in self.queu:
            thread[1].start()
        for thread in self.queu:
            thread[1].join()
