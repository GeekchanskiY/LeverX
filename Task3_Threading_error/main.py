from threading import Thread
from threading import Lock



a = 0
lock = Lock()

def function(arg):
    global a
    for _ in range(arg):
        lock.acquire()
        a += 1
        lock.release()



def main():
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)


main()