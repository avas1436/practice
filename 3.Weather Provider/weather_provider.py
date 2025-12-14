import json
from typing import Literal, Optional

import requests


def openweather(
    lat: float = 32.127594,
    lon: float = 51.456565,
    mode: Optional[Literal["standard", "metric", "imperial"]] = "metric",
    api: str = "c7f76b6aa6f9be23330e085b601b7b20",
):
    try:
        url = (
            rf"https://api.openweathermap.org/data/2.5/weather?"
            rf"lat={lat}&lon={lon}&appid={api}&units={mode}"
        )
        response = requests.get(url, timeout=10)

        # Raise HTTP error if status code is not 200
        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        return {"error": "Request timed out."}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Please check your internet."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


print(openweather())
