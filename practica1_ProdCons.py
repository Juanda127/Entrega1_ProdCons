
"""
Created on Sun Mar  6 19:05:27 2022

@author: juan
"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
import random

NPROD = 3
NCONS = 1
N = 5


def producer(sem_empty, sem_nonempty, buffer, prid):
    v = 0 
    for i in range(N):
        print(f"producer {current_process().name} producing")
        sleep(0.01)
        sem_empty[prid].acquire() 
        v += random.randint(0,10)
        buffer[prid] = v
        sem_nonempty[prid].release()
        print(f"producer {current_process().name} storing {v}")
    sem_empty[prid].acquire()
    buffer[prid] = -1
    sem_nonempty[prid].release()
    
def minimum(l):
    i = 0
    j = 0
    while j <len(l):
        
        while l[i] ==-1:
            i = i +1
            j = i + 1
        if j == len(l):
            break
        while l[j] == -1:
            j = j + 1            
            if j == len(l):
                break
        if j == len(l):
            break
        if l[i]<=l[j]:
            j = j +1
        else:
            i=j
    return l[i], i
        



def consumer(sem_empty, sem_nonempty, buffer):  
    out = []
    for i in range(NPROD):
        sem_nonempty[i].acquire()
    listastop = [-1]*NPROD
    while listastop != list(buffer): 
        print ("consumer unstock")
        sleep(random.random()/3)
        v, prid = minimum(list(buffer))
        out.append(v) 
        sem_empty[prid].release()
        print (f"consumer consuming {v}")
        sem_nonempty[prid].acquire()
    print(out )


def main():
    buffer = Array('i',NPROD)
    sem_empty = []
    sem_nonempty = []
    for i in range(NPROD):
        non_empty = Semaphore(0)
        empty = BoundedSemaphore(1)
        sem_empty.append(empty)
        sem_nonempty.append(non_empty)
    prodlst = [Process(target = producer, 
                       name=f'prod_{i}', 
                       args=(sem_empty, sem_nonempty, buffer,i))
                    for i in range (NPROD)]
    conslst = [Process(target = consumer, args = (sem_empty, sem_nonempty, buffer))]
    
    for p in prodlst + conslst:
        p.start()
         
    for p in prodlst + conslst:
        p.join()

if __name__ == "__main__":
   main()
           
         
    
    