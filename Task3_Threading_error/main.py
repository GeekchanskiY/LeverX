from threading import Thread
from threading import Lock
from concurrent.futures import ThreadPoolExecutor


class Data:
    def __init__(self):
        self.variable = 0


lock = Lock()

def function(arg, obj):
    lock.acquire()
    for _ in range(arg):
        obj.variable += 1
    lock.release()



def main():
    obj = Data()
    threads = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit(function(1000000, obj))



    [t.join() for t in threads]
    print("----------------------", obj.variable)


main()