import os
import re
import schemas
from datetime import datetime   

def ping(host: str) -> schemas.PingResultBase:
    timeSent = datetime.now()
    stream = os.popen('ping -c 4 {host}'.format(host = host))
    out = stream.read()

    if out == 0:
        pass
        # TODO implement handling
    else:
        avgPingTimePttrn = re.compile(r'\d+.\d+/\d+.\d+/\d+.\d+/\d+.\d+')
        serverIPPttrn = re.compile(r'\d+.\d+.\d+.\d+')
        packetsSentPttrn = re.compile(r'\d+ [p][a][c]')
        packetsRecPttrn = re.compile(r'\d+ [r][e][c]')

        # FIXME returning incorrect value when parsing
        avgPingTime = float(avgPingTimePttrn.search(out).group()[7:13])
        # avgPingTime = avgPingTimePttrn.search(out)
        print(avgPingTime)
        serverIP = serverIPPttrn.search(out).group()
        packetsSent = int(packetsSentPttrn.search(out).group().split(sep=' ')[0])
        packetsRec = int(packetsRecPttrn.search(out).group().split(sep=' ')[0])

        res = schemas.PingResultBase(url=host, ip=serverIP, packets_sent=packetsSent, packets_recieved=packetsRec, avg_ping_time=avgPingTime, time_sent=timeSent)
    return res