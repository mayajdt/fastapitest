import os
import re
import schemas
from datetime import datetime

def ping(host, pcktAmt) -> schemas.PingResultBase:
    timeSent = datetime.now()
    stream = os.popen('ping -c {pcktAmt} {host}'.format(pcktAmt = pcktAmt, host = host))
    out = stream.read()

    if out == 0:
        res = schemas.PingResultBase()
    else:
        timePttrn = re.compile(r'[t][i][m][e] \d+')
        serverIPPttrn = re.compile(r'\d+.\d+.\d+.\d+')
        packetsSentPttrn = re.compile(r'\d+ [p][a][c]')
        packetsRecPttrn = re.compile(r'\d+ [r][e][c]')

        time = timePttrn.search(out).group()[5:]
        serverIP = serverIPPttrn.search(out).group()
        packetsSent = packetsSentPttrn.search(out).group().split(sep=' ')[0]
        packetsRec = packetsRecPttrn.search(out).group().split(sep=' ')[0]

        res = schemas.PingResultBase(url=host, ip=serverIP, packets_sent=packetsSent, packets_recieved=packetsRec, time_spent=time, time_sent=timeSent)
    return res