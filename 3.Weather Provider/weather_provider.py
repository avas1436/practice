import json
from typing import Literal, Optional
from urllib import response

import requests


def openweather(
    lat: float = 32.127594,
    lon: float = 51.456565,
    mode: Optional[Literal["standard", "metric", "imperial"]] = "metric",
    api: str = "c7f76b6aa6f9be23330e085b601b7b20",
):
    url = (
        rf"https://api.openweathermap.org/data/2.5/weather?"
        rf"lat={lat}&lon={lon}&appid={api}&units={mode}"
    )
    response = requests.get(url=url)
    print(response)
    return response.json()


print(openweather())
