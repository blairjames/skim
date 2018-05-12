import asyncio
import cProfile
import pstats


class Astinkio:

    async def my_coroutine(self, number: int):
        result = number * number
        result = result * result
        print(str(result))

    def go(self):
        num = 8
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Astinkio().my_coroutine(int(num)))
        loop.close()

def main():
    a = Astinkio()
    a.go()


if __name__ == '__main__':
    x = cProfile.run(main())
    pstats.Stats.print_stats(x)
