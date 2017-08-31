from multiprocessing import Process
def test():
    print "Hi"
    
process = Process(target=test)
process.start()
process.join()