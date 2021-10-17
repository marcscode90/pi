#!/bin/python3

import os
import sys

_cpath_ = sys.path[0]
sys.path.remove(_cpath_)
import time as ti

#GLOBALS
PIPE_FILE = '/tmp/cald_pipe'
DB_FILE = ''
INDEX_FILE = '/tmp/calendar_link'
ERR_FILE = '/tmp/cald_err.log'


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




def run():
    sys.stdout = Logger()
    if os.path.exists(PIPE_FILE):
        if os.path.exists(INDEX_FILE):
           with open(INDEX_FILE,'r') as f:
               global DB_FILE
               DB_FILE = f.read()
        else:
            print("Unable to process calendar database")
            return

        if not os.path.exists(DB_FILE):
            print("Unable to process calendar database")
            return

        for i in range(0,len(sys.argv)):
            sys.argv[i] =sys.argv[i].replace("\n","")
        try:
            command = sys.argv[1]
            # deal 'GET'
            if command == 'GET':
                if sys.argv[2] == 'DATE':
                    get_date()
                if sys.argv[2] == 'INTERVAL':
                    get_interval()
                if sys.argv[2] == 'NAME':
                    get_name()
            # deal 'ADD' 'DEL' 'UPD'
            else:
                if command == 'ADD':
                    if check_add():
                        writepipe()
                elif command == 'UPD':
                    if check_upd():
                        writepipe()
                elif command == 'DEL':
                    if check_del():
                        writepipe()
                else:
                    print("Multiple errors occur")

        except:
            print("Pipe has been closed")

    else:
        print("PIPE DOESN'T EXISTS")

#GET COMMAND
def get_date():
    if not isVaildDate(sys.argv[3]):
        print("Unable to parse date")
        return
    item_list = find_db()
    output_list = []
    for item in item_list:
        if item[0] == sys.argv[3]:
            output_list.append(item)
    output_item(output_list)

def get_interval():
    try:
        start = sys.argv[3]
        end = sys.argv[4]
        if not isVaildDate(start) or not isVaildDate(end):
            print("Unable to parse date")
            return
        s_start = ti.mktime(ti.strptime(start, "%d-%m-%Y"))
        s_end = ti.mktime(ti.strptime(end, "%d-%m-%Y"))
        if s_end - s_start<0:
            print("Unable to Process, Start date is after End date")
        else:
            item_list = find_db()
            output_list = []
            for item in item_list:
                s_time = ti.mktime(ti.strptime(item[0],"%d-%m-%Y"))
                if s_time>=s_start and s_time<=s_end:
                    output_list.append(item)
            output_item(output_list)
    except Exception as e:
        print(e)

def get_name():
    if len(sys.argv)<=3:
        print("Please specify an argument")
        return
    item_list = find_db()
    output_list = []
    for item in item_list:
        if item[1].startswith(sys.argv[3]):
            output_list.append(item)
    output_item(output_list)

#CHECKCOMMAND
def check_add():
    if not isVaildDate(sys.argv[2]):
        print("Unable to parse date")
        return False
    if len(sys.argv) <=3:
        print("Missing event name")
        return False
    return True

def check_del():
    if not isVaildDate(sys.argv[2]):
        print("Unable to parse date")
        return False
    if len(sys.argv) <=3:
        print("Missing event name")
        return False
    return True

def check_upd():
    if not isVaildDate(sys.argv[2]):
        print("Unable to parse date")
        return False
    if len(sys.argv) <=3:
        print("Missing event name")
        return False
    item_list = find_db()
    upd_item = sys.argv[2:]
    for item in item_list:
        if item[0] == upd_item[0] and item[1] == upd_item[1]:
            break
    else:
        print("Unable to update, event does not exist")
        return False
    return True


#CHECKTIME
def isVaildDate(date):
    try:
        ti.strptime(date, "%d-%m-%Y")
        return True
    except Exception as e:
        print(e)
        return False

def writepipe():
    pipe = open(PIPE_FILE,'w')
    pipe.write(" ".join(sys.argv[1:]))
    pipe.close()

def find_db():
    with open(DB_FILE,'r') as f:
        item_list = []
        db_str = f.read()
        for i in db_str.split('\n'):
            item = i.split(',')
            if len(item)>1:
                item_list.append(item)
        return item_list

def output_item(item_list:list):
    for item in item_list:
        print(" : ".join(item))

if __name__ == '__main__':
    run()

