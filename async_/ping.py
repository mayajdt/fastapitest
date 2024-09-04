from schemas.schemas import PingResultBase, ErrorResultBase
from datetime import datetime   
from icmplib import async_ping, async_resolve, Host
from icmplib.exceptions import NameLookupError, SocketPermissionError, SocketAddressError, ICMPSocketError
from schemas.schemas import PingResultBase

async def async_ping_t(urls: list[str]) -> tuple[list[PingResultBase], list[dict]]:
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

    This function uses async_multiping() and async_resolve, which are non-blocking functions
    '''

    time_sent = datetime.now()

    ok = []
    resolved_ips = []
    failed = []

    for url in urls:
        try:
            ips = await async_resolve(url)
        except NameLookupError:
            failed.append(dict(url= url, error_desc="Could not resolve host"))
        else:
            try:
                res = await async_ping(address=ips[0], count=1, privileged=False)
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