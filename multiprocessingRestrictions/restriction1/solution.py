from multiprocessing import Process
def test():
    print "Hi"
    
if __name__ == '__main__':
    process = Process(target=test)
    process.start()
    process.join()