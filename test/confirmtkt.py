import asyncio

from MultiFeatures.IndianRailway.confirmtkt import Confirmtkt



async def main():
    confirmtkt = Confirmtkt()
    v = await confirmtkt.train_schedule(12625, date="07-07-2024")
    print(v)


if __name__ == "__main__":
    asyncio.run(main())
