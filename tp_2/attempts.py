import os, time

ordre = []

nb = 3

retour_r, retour_w = os.pipe() #tube globale de tous les enfants 
values = ["cmd 1", "cmd 2", "cmd 3", "cmd 4"]

for i in range(nb): 
    r, w = os.pipe() # tube d'entree personnel de chaque enfant 
    pid = os.fork()

    if pid : 
        os.close(r)
        for value in values:
            print(f"Parent : sending {value} to my child")
            os.write(w, value.encode())
        os.close(w)
        os.wait()
        #do somthing 
    else : 
        index = 0
        os.close(w)
        while True : 
            index +=1; 
            values_received_from_parent =  os.read(r, 1024).decode()
            print(f"Child : received {values_received_from_parent} from my parent, and I will sleep for {i} seconds")
            time.sleep(i)
            ordre.append(os.getpid())
            if index >=len(values): 
                print("finished ...")
                break
        os.close(r)












#####################################
"""pipe_file_name = "/tmp/pipe"

if not os.path.exists(pipe_file_name):
    os.mkfifo(pipe_file_name)

 def producer(NB): # parent 
    with open(pipe_file_name, "w") as pipe:
        for i in range(NB):
            message = f"message {i}"
            print(f"Parent producing and writing {message.strip()}")
            pipe.write(message)
            time.sleep(1) """

#######################################
""" 
if pid:
    os.close(r_dsc)
    values = ["value 1", "value 2", "value 3", "value 4", "value 5", "exit"]
    for value in values:
        print(f"Parent producing and writing {value}")
        os.write(w_dsc, value.encode())
        time.sleep(2)
    os.close(w_dsc)
    os.wait()

else:
    os.close(w_dsc)
    print(f"Receiving value from my parent : {os.getppid()}")
    while True:
        value_received_from_parent = os.read(r_dsc, 1024).decode()
        print(f"Reading {value_received_from_parent} from parent {os.getppid()}")
        if value_received_from_parent == "exit": # message to tell the child to stop  
            print("child finished ... ")
            break
    os.close(r_dsc) """

##################################################

