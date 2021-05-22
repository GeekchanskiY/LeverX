from threading import Thread
from threading import Lock
from concurrent.futures import ThreadPoolExecutor


class Data:
    def __init__(self):
        self.lock = Lock()
        self.variable = 0

    def function(self, arg:int):
        for _ in range(arg):
            self.lock.acquire()
            self.variable += 1
            self.lock.release()




def main():
    obj = Data()
    result = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit( obj.function(1000000) )


    print("----------------------", obj.variable)


main()