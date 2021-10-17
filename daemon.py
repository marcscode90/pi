#!/bin/python3

import signal
import os
import sys


#Globals
PIPE_FILE = '/tmp/cald_pipe'
DB_FILE = '/home/cald_db.csv'
ERR_FILE = '/tmp/cald_err.log'
INDEX_FILE = '/tmp/calendar_link'

#logger
class Logger(object):
    def __init__(self, filename=ERR_FILE):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass



#Use this variable for your loop
daemon_quit = False


#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True




def run():
    sys.stdout = Logger()
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within 
    # the run() funcion
    if not os.path.exists(PIPE_FILE):
        os.mkfifo(PIPE_FILE)

    if len(sys.argv)>1:
        global DB_FILE
        DB_FILE = sys.argv[1]
    print(sys.argv)
    with open(INDEX_FILE,'w') as f:
        f.write(DB_FILE)

    with open(DB_FILE,'a') as f:
        f.close()

    while not daemon_quit:

        pipe = open(PIPE_FILE,'r')

        recv_commond = pipe.readline()


        #run
        if len(recv_commond) != 0:
            recv_commond = recv_commond.split(' ')
            if recv_commond[0] == 'ADD':
                add(recv_commond)
            if recv_commond[0] == 'DEL':
                dele(recv_commond)
            if recv_commond[0] == 'UPD':
                upd(recv_commond)

        pipe.close()

def check_add(new_item):
    item_list = find_db()
    for item in item_list:
        if item[0] == new_item[0] and item[1] == new_item[1]:
            return False
    else:
        return True


def add(recv_commond):
    item_list = find_db()
    add_list = []
    for j in recv_commond[1:]:
        add_list.append(j.replace("\n",""))
    if check_add(add_list):
        item_list.append(add_list)
        write_db(item_list)
    else:
        print("crush")

def dele(recv_commond):
    item_list = find_db()
    del_item = []
    for j in recv_commond[1:]:
        del_item.append(j.replace("\n",""))
    for item in item_list:
        if item[0] == del_item[0] and item[1] == del_item[1]:
            item_list.remove(item)
    write_db(item_list)

def upd(recv_commond):
    item_list = find_db()
    upd_item = []
    for j in recv_commond[1:]:
        upd_item.append(j.replace("\n",""))
    for i in range(0,len(item_list)):
        item = item_list[i]
        if item[0] == upd_item[0] and item[1] == upd_item[1]:
            item_list[i]=[item[0]]
            item_list[i].extend(upd_item[2:])
            break
    write_db(item_list)


def write_db(item_list):
    with open(DB_FILE,'w') as f:
        com_str = ""
        for i in range(0,len(item_list)):
            item = item_list[i]
            com_str = com_str +  ','.join(item)
            com_str = com_str+'\n'
        f.write(com_str)

def find_db():
    with open(DB_FILE,'r') as f:
        item_list = []
        db_str = f.read()
        for i in db_str.split('\n'):
            item = i.split(',')
            if len(item)>1:
                item_list.append(item)
        return item_list

if __name__ == '__main__':
    run()
