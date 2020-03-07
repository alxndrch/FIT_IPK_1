#!/usr/bin/python3
from socket import *
import sys, re

def parse_name(match):
    return match.split("&",1)[0].split("name=",1)[1]

def parse_type(match):
    return match.split("type=",1)[1]

def process_get(request):

    match = re.search(r"^/resolve\?.*", request[0])
    if(match == None):
        return ("400 Bad Request","")

    params = match.group().split("?",1)[1]
    match = re.search(r"^name=.*", params)

    if(match == None):
        return ("400 Bad Request","")

    name = parse_name(match.group())

    match = re.search(r"^&type=(A|PTR)$",match.group().split("name="+name,1)[1])
    if(match == None):
        return ("400 Bad Request","")

    type = parse_type(match.group())

    try:
        addr = gethostbyaddr(name)
    except:
        return ("404 Not Found","")

    try:
        if(type == "A"):
            if(gethostbyname(name) != name):
                return ("200 OK","{}:{}={}\n".format(name,type,addr[2][0]))
        else:
            if(gethostbyname(name) == name):
                return ("200 OK","{}:{}={}\n".format(name,type,addr[0]))
    except:
        pass

    return ("400 Bad Request","")


def process_post(request):

    first_line = request[0].split(" ")

    if(first_line[1] != "/dns-query"):
        return ("400 Bad Request","")

    data = request[7:]

    output = ""
    fail_counter = 0
    text_data = False
    empty_line = False
    eline_err = False
    data_len = 0

    for req in data:

        if(req == "" or req.isspace()):
            if(text_data == True):
                empty_line = True
            continue     
        else:
            if(empty_line == True):
                eline_err = True
            else:
                text_data = True

        if(eline_err == True):
            return ("400 Bad Request","")

        name = req.split(":",1)[0].strip()
        type = req.split(":",1)[1].strip()

        data_len += 1
        try:
            addr = gethostbyaddr(name)
        except:
            fail_counter += 1
            continue

        try:
            if(type == "A"):
                if(gethostbyname(name) != name):
                    output = output + "{}:{}={}\n".format(name,type,addr[2][0])
            else:
                if(gethostbyname(name) == name):
                    output = output + "{}:{}={}\n".format(name,type,addr[0])
        except:
            pass

    if(data_len == fail_counter):
        return ("404 Not Found","")

    return ("200 OK",output.strip())


if(len(sys.argv) <= 1):
    print("PORT IS MISSING")
    sys.exit()

PORT = sys.argv[1]

try:
    serverSocket = socket(AF_INET,SOCK_STREAM)
    try:
        serverSocket.bind(("",int(PORT)))
    except:
        print("PORT {} IS NOT ACCESSIBLE".format(PORT))
        sys.exit()

    serverSocket.listen(1)
    print ("THE SERVER IS READY")
    while 1:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)

        client_input = sentence.decode("utf-8")
        http_request = client_input.split('\n')[0].split(" ")
        if(http_request[0] == "GET"):
            response = process_get(http_request[1:])
        elif(http_request[0] == "POST"):
            response = process_post(client_input.split('\n'))
        else:
            response = ("405 Method Not Allowed","")

        msg = "HTTP/1.1 "+response[0]+"\r\n\r\n"+response[1]
        connectionSocket.sendall(str.encode(msg))
        connectionSocket.close()
except KeyboardInterrupt:
    print("\nSERVER DISCONNECTED")
    sys.exit()
