from schemas import PingResultBase, ErrorResultBase
from datetime import datetime   
from icmplib import ping, exceptions, Host
from icmplib.exceptions import NameLookupError, SocketPermissionError, SocketAddressError, ICMPSocketError

def ping_t(host: str) -> PingResultBase | ErrorResultBase:
    host_clean = host.replace("\n", "")
    time_sent = datetime.now()
    resp = None

    try:
        ping_res = ping(host_clean, count=1, privileged=False)
    except NameLookupError:
        resp = ErrorResultBase(url=host_clean, error_name=NameLookupError.__name__, error_desc="Could not resolve host")
    except SocketPermissionError:
        resp = ErrorResultBase(url=host_clean, error_name=SocketPermissionError.__name__, error_desc="Socket does not have priviliges")
    except SocketAddressError:
        resp = ErrorResultBase(url=host_clean, error_name=SocketAddressError.__name__, error_desc="Address cannot be assigned to socket")
    except ICMPSocketError:
        resp = ErrorResultBase(url=host_clean, error_name=SocketAddressError.__name__, error_desc="An error with the socket occurred")
    else:
        if ping_res.is_alive:
            resp = PingResultBase(url=host_clean, ip=ping_res.address, packets_sent=ping_res.packets_sent, packets_recieved=ping_res.packets_received, avg_ping_time=ping_res.avg_rtt, time_sent=time_sent)
        else:
            resp = ErrorResultBase(url=host_clean, error_name="AddressUnreachable", error_desc="Could not reach host")
    
    return resp