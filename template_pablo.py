import os
import time

pipe_file_name = "/tmp/pipe"


#signed by Pablo CONCHA

if os.path.exists(pipe_file_name):
    os.mkfifo(pipe_file_name)


def producer(NB):
    with open(pipe_file_name, "w") as pipe:
        for i in range(NB):
            message = f"message {i}"
            print(f"producing and writing {message.strip()}")
            pipe.write(message)
            time.sleep(1)


def consumer():
    with open(pipe_file_name, "r") as pipe:
        while True:
            message = pipe.readline()
            if message == "":
                break
            print(f"Consumer just read : {message.strip()}")


if __name__ == "__main__":
    consumer_process = os.fork()
    #enfant
    if consumer_process == 0:
        consumer()
    else:
        #parent
        producer(8)
