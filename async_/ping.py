from schemas.schemas import PingResultBase, ErrorResultBase
from datetime import datetime
from icmplib import async_ping, Host
from icmplib.exceptions import ICMPLibError
from schemas.schemas import PingResultBase
import time
import asyncio
from itertools import chain

class PingResRaw:
    def __init__(self, url: str, ping_data: Host, time_sent: datetime):
        self.url= url
        self.ping_data= ping_data
        self.time_sent= time_sent

def gen_ping_result_objs(l: chain[PingResRaw]) -> list[PingResultBase]:
    res = []
    for el in l:
        res.append(
            PingResultBase(
                url=el.url,
                ip=el.ping_data.address,
                avg_ping_time=el.ping_data.avg_rtt,
                packets_sent=el.ping_data.packets_sent,
                packets_recieved=el.ping_data.packets_received,
                time_sent=el.time_sent
            )
        )
    return res

def chunks(l, n):
    for i in range(0, n):
        yield l[i::n]

async def async_ping_t(urls: list[str]) -> tuple[chain[PingResRaw], chain[tuple]]:
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

    This function uses async_ping() and async_resolve, which are non-blocking functions
    '''

    start = time.perf_counter()

    time_sent = datetime.now()

    async def foo(urls: list) -> tuple[list, list]:
        ok = []
        failed = []
        for url in urls:
                try:
                    res = await async_ping(address=url, count=1, privileged=False, timeout=1)
                except ICMPLibError as err:
                    failed.append(tuple([url, err]))
                else:
                    ok.append(PingResRaw(url=url, ping_data=res, time_sent=time_sent))
        return ok, failed

    list1, list2, list3, list4 = chunks(urls, 4)

    res1, res2, res3, res4 = await asyncio.gather(
        foo(list1),
        foo(list2),
        foo(list3),
        foo(list4),
    )

    ok = chain(res1[0], res2[0], res3[0], res4[0])
    failed = chain(res1[1], res2[1], res3[1], res4[1])

    stop = time.perf_counter()

    time_spent = stop - start
    print(f'pinging all {len(urls)} urls took {time_spent} seconds')
            
    return ok, failed