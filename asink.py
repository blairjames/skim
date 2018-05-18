#!/usr/bin/env python3

import asyncio
import time
import aiohttp
import skim_controller
ctrl = skim_controller.SkimController()

class Asink:

    async def requester(self, url):
        try:
            p1 = time.perf_counter()
            session = aiohttp.ClientSession()
            async with session.get(url, timeout=180) as resp:
                print(str(url) + " : " + str(resp.status))
            p2 = time.perf_counter()
            print(p2-p1)
            session.close()
        except Exception as e:
            print(str(url) + " error: " + str(e))

    def read_domains(self):
        dir = ctrl.path_to_urls
        doms = []
        ap = doms.append
        with open(dir, "r") as url_file:
            for url in url_file.read().splitlines():
                ap("http://" + str(url))
            url_file.close()
        return doms

    async def gen(self):
        tasks = [asyncio.ensure_future(self.requester(u)) for u in self.read_domains()]
        await asyncio.wait(tasks)


def main():
    p1 = time.perf_counter()
    a = Asink()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a.gen())
    loop.close()
    p2 = time.perf_counter()
    print("Total Time: " + str(p2 - p1))


if __name__ == '__main__':
    main()


