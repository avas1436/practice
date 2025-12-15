import json
from typing import Dict, Literal, Optional

import requests
from rich.console import Console
from rich.table import Table


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


def extract_data(data: Dict) -> Dict:
    """Extract fields safely and return as dictionary"""
    weather_info = {
        "id": data.get("id"),
        "date": data.get("dt"),
        "country": data.get("sys", {}).get("country"),
        "city": data.get("name"),
        "longitude": data.get("coord", {}).get("lon"),
        "latitude": data.get("coord", {}).get("lat"),
        "weather": data.get("weather", [{}])[0].get("main"),
        "description": data.get("weather", [{}])[0].get("description"),
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "min_temp": data.get("main", {}).get("temp_min"),
        "max_temp": data.get("main", {}).get("temp_max"),
        "pressure": data.get("main", {}).get("pressure"),
        "humidity": data.get("main", {}).get("humidity"),
        "sea_level": data.get("main", {}).get("sea_level"),
        "ground_level": data.get("main", {}).get("grnd_level"),
        "visibility": data.get("visibility"),
        "wind_speed": data.get("wind", {}).get("speed"),
    }
    return weather_info


# data = openweather()
all_weather_data = []


# فرضاً چند بار داده گرفتیم
all_weather_data.append(extract_data(openweather(lat=32.127594, lon=51.456565)))  # Borujen
all_weather_data.append(extract_data(openweather(lat=35.6892, lon=51.3890)))  # Tehran
all_weather_data.append(extract_data(openweather(lat=29.5918, lon=52.5836)))  # shiraz
all_weather_data.append(extract_data(openweather(lat=31.949249, lon=49.305954)))  # Masjed Soleyman
all_weather_data.append(extract_data(openweather(lat=32.34651, lon=51.50449)))  # Mobarakeh
all_weather_data.append(extract_data(openweather(lat=37.433, lon=49.550)))  # Gilan
all_weather_data.append(extract_data(openweather(lat=38.2498, lon=48.2933)))  # Ardabil


# Print with Rich table
console = Console()
table = Table(title="Weather Data")

# اضافه کردن ستون‌ها
table.add_column("Field", style="cyan", no_wrap=True)
table.add_column("Borujen", style="green")
table.add_column("Tehran", style="red")
table.add_column("Shiraz", style="blue")
table.add_column("Masjed Soleyman", style="magenta")
table.add_column("Mobarakeh", style="yellow")
table.add_column("Gilan", style="bright_cyan")
table.add_column("Ardabil", style="bright_green")

# اضافه کردن ردیف‌ها
for field in all_weather_data[0].keys():
    borujen_value = str(all_weather_data[0].get(field))
    tehran_value = str(all_weather_data[1].get(field))
    shiraz_value = str(all_weather_data[2].get(field))
    masjed_soleyman_value = str(all_weather_data[3].get(field))
    mobarakeh_value = str(all_weather_data[4].get(field))
    gilan_value = str(all_weather_data[5].get(field))
    ardabil_value = str(all_weather_data[6].get(field))

    table.add_row(
        field,
        borujen_value,
        tehran_value,
        shiraz_value,
        masjed_soleyman_value,
        mobarakeh_value,
        gilan_value,
        ardabil_value,
    )

console.print(table)
