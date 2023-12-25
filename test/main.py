import asyncio
import json

from MultiFeatures.IndianRailway import confirmtkt

confirmtkt = confirmtkt.Confirmtkt()



def main():
    k = confirmtkt.livestatusall(
        trainno="83212",
        doj="25-12-2023",
        locle="en"
    )
    print(json.dumps(k, indent=4))

if __name__ == "__main__":
    main()
