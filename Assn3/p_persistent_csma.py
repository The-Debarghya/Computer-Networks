#!/usr/bin/env python3
import threading
import time
import random

class bcolors:
    HEADER = '\033[106m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @classmethod
    def return_color(cls, style, fg, bg, text):
        format = ';'.join([str(style), str(fg), str(bg)])
        s1 = '\x1b[%sm%s \x1b[0m' % (format, text)
        return s1

total_frames = 0
frametime = 0.2
inbetween_frametime = 0.05
nframes = 0
frame_attempts = 0
#backoff_period = 0

def channel(lock: threading.Lock, total_frames_to_send: int) -> None:
    global total_frames
    global frame_attempts
    being_used = 0
    total = 0
    while total_frames < total_frames_to_send:
        if lock.locked():
            being_used += 1
        total += 1
        #print(f"{bcolors.return_color(0, 32, 40, f'[i] INFO: Used:{being_used}, Total:{total}')}")
    try:
        print(f"{bcolors.return_color(0, 35, 40, f'[i] INFO: Channel Utilisation: {being_used/total}')}")
        print(f"{bcolors.return_color(0, 35, 40, f'[i] INFO: Channel Idle: {(total-being_used)/total}')}")
        print(f"{bcolors.return_color(0, 35, 40, f'[i] INFO: Efficiency: {total_frames/frame_attempts}')}")
    except ZeroDivisionError:
        print(f"{bcolors.return_color(0, 31, 40, '[-] ERROR: Division by zero is not possible!')}")

class PPersistentCsma(threading.Thread):
    def __init__(self, lock: threading.Lock, index: int) -> None:
        super().__init__()
        self.index = index
        self.lock = lock

    def run(self):
        global total_frames
        global nframes
        global frame_attempts
        global probability
        global backoff_period
        random.seed(time.time())
        cnt = 1
        while cnt <= nframes:
            print(f"{bcolors.return_color(1, 33, 40, f'[i] ATTEMPT: Frame {cnt}, Station {self.index}')}")
            while self.lock.locked():
                print(f"{bcolors.return_color(0, 33, 40, f'[-] CARRIER SENSE: Frame {cnt}, Station {self.index}')}")
            
            x = random.random()
            while x > probability:
                print(f"{bcolors.return_color(0, 35, 40, f'[-] WAITING: Frame {cnt}, Station {self.index}, Period: {backoff_period}, x: {x}')}")
                time.sleep(backoff_period)
                while self.lock.locked():
                    print(f"{bcolors.return_color(0, 31, 40, f'[-] FAILED: Frame {cnt}, Station {self.index}')}")
                frame_attempts += 1
                x = random.random()

            self.lock.acquire()
            #critical section
            time.sleep(frametime)
            total_frames += 1
            frame_attempts += 1
            print(f"{bcolors.return_color(1, 32, 40, f'[+] SUCCESS: Frame {cnt}, Station {self.index}')}")
            self.lock.release()
            time.sleep(inbetween_frametime)
            cnt += 1

def main():
    global nframes
    global backoff_period
    global probability
    nstations = int(input(f"{bcolors.OKBLUE}[*] PROMPT: Number of stations:{bcolors.ENDC}"))
    nframes = int(input(f"{bcolors.OKBLUE}[*] PROMPT: Number of frames to send per station:{bcolors.ENDC}"))
    backoff_period = round(random.uniform(0.3, 0.5), 2)
    probability = 1/nstations

    lock = threading.Lock()
    station_list = [PPersistentCsma(lock, i+1) for i in range(nstations)]
    channel_thread = threading.Thread(target=channel, args=[lock, nstations*nframes])
    channel_thread.start()
    for station in station_list:
        station.start()
    for station in station_list:
        station.join()
    channel_thread.join()

if __name__ == "__main__":
    main()
