#!/usr/bin/env python3

import asyncio
import time
import aiohttp
import skim_controller
ctrl = skim_controller.SkimController()


class Asink:

    async def requester(self, url):
        try:
            session = aiohttp.ClientSession()
            async with session.get(url, timeout=20) as resp:
                print(str(url) + " : " + str(resp.status))
                session.close()
        except Exception as e:
            print(str(url) + " Error!!: " + str(e))

    def read_domains(self):
        dir = ctrl.path_to_urls
        with open(dir, "r") as url_file:
            doms = [str("https://" + url) for url in url_file.read().splitlines()]
        return doms

    async def gen(self):
        tasks = [asyncio.ensure_future(self.requester(str(u))) for u in self.read_domains()]
        await asyncio.wait(tasks)

async def main():
    p1 = time.perf_counter()
    a = Asink()
    await a.gen()
    p2 = time.perf_counter()
    print("Total Time: " + str(p2 - p1))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


