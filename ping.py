from schemas import PingResultBase, ErrorResultBase
from datetime import datetime   
from icmplib import ping, resolve
from icmplib.exceptions import NameLookupError, SocketPermissionError, SocketAddressError, ICMPSocketError
from models import PingResult
from schemas import PingResultBase

def ping_t(urls: list[str]) -> tuple[list[PingResultBase], list[dict]]:
    '''
    Ping urls in the passed list

    If url pings successfully, instance of PingResultBase with appropriate data will be created

    If url doesn't ping successfully, the following dict will be created:

        dict(
            url: str,
            error_name: str,
            error_desc: str,
        )

    Function will return two lists: one for successful pings and one for unsuccessful
    '''
    # host_clean = host.replace("\n", "")
    # time_sent = datetime.now()
    # resp = None

    # try:
    #     ping_res = ping(host_clean, count=1, privileged=False)
    # except NameLookupError:
    #     resp = ErrorResultBase(url=host_clean, error_name=NameLookupError.__name__, error_desc="Could not resolve host")
    # except SocketPermissionError:
    #     resp = ErrorResultBase(url=host_clean, error_name=SocketPermissionError.__name__, error_desc="Socket does not have priviliges")
    # except SocketAddressError:
    #     resp = ErrorResultBase(url=host_clean, error_name=SocketAddressError.__name__, error_desc="Address cannot be assigned to socket")
    # except ICMPSocketError:
    #     resp = ErrorResultBase(url=host_clean, error_name=SocketAddressError.__name__, error_desc="An error with the socket occurred")
    # else:
    #     if ping_res.is_alive:
    #         resp = PingResultBase(url=host_clean, ip=ping_res.address, packets_sent=ping_res.packets_sent, packets_recieved=ping_res.packets_received, avg_ping_time=ping_res.avg_rtt, time_sent=time_sent)
    #     else:
    #         resp = ErrorResultBase(url=host_clean, error_name="AddressUnreachable", error_desc="Could not reach host")
    
    # return resp

    time_sent = datetime.now()

    ok = []
    failed = []

    for url in urls:
        try:
            ips = resolve(url)
        except NameLookupError:
            failed.append(dict(url= url, error_desc="Could not resolve host"))
        try:
            res = ping(ips[0], count=1, privileged=False)
        except SocketPermissionError:
            failed.append(
                dict(
                    url= url, 
                    error_name=SocketPermissionError.__name__,
                    error_desc="Socket does not have privilige"
                    )
            )
        except SocketAddressError:
            failed.append(
                dict(
                    url= url, 
                    error_name= SocketAddressError.__name__,
                    error_desc="Address cannot be assigned to socket"
                    )
            )
        except ICMPSocketError:
            failed.append(
                dict(
                    url= url,
                    error_name=ICMPSocketError.__name__,
                    error_desc="An error with the socket occurred"
                    )
            )
        else:
            if res.packets_received != res.packets_sent:
                failed.append(
                    dict(
                        url= url,
                        error_name="NoPacketsRecieved",
                        error_desc="Didnt recieve any packets back, probably dead"
                        )
                )
            else:
                ok.append(
                    PingResultBase(
                        url=url,
                        ip=res.address,
                        packets_sent=res.packets_sent,
                        packets_recieved=res.packets_received,
                        avg_ping_time=res.avg_rtt,
                        time_sent=time_sent
                    )
                )

    return ok, failed