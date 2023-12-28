## Install

```sh
pip install -U multifeatures
```

## Documentation
  - Documenttation available here: [https://multifeatures.devh.in/](https://multifeatures.devh.in/)

## Example Usage

```py
from MultiFeatures.IndianRailway import confirmtkt
confirmtkt_object = confirmtkt.Confirmtkt()
try:
    live_status_data = confirmtkt_object.live_train_status(train_no="12345", doj="01-01-2023", locale="en")
    print(live_status_data)
except NotAValidTrainNumber as error:
    print(f"Error: {error}")
except InternetUnreachable:
    print("Error: Connectivity issue. Please check your internet connection.")
except HTTPErr:
    print("Error: ran into an issue. Please try again later, or Check the data.")
```

