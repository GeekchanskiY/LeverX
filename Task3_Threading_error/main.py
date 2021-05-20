from threading import Thread
from threading import Lock
from concurrent.futures import ThreadPoolExecutor


class Data:
    def __init__(self):
        self.lock = Lock()
        self.variable = 0


def function(arg, obj):

    for _ in range(arg):
        obj.lock.acquire()
        obj.variable += 1
        obj.lock.release()


def main():
    obj = Data()
    threads = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit(function(arg=1000000, obj=obj))

    [t.join() for t in threads]
    print("----------------------", obj.variable)


main()