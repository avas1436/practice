import asyncio
from typing import Dict, List, Tuple

import aiohttp
from aiohttp import ClientError
from rich.console import Console
from rich.table import Table


async def openweather(
    lon: float,
    lat: float,
    base_url: str = r"https://api.openweathermap.org/data/2.5/weather",
    api: str = r"15a70b773b728dbada35622d2fc6d130",
):
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": api,
                "units": "metric",
            }
            async with session.get(url=rf"{base_url}", params=params) as response:
                if response.status != 200:
                    raise RuntimeError(f"Bad status code: {response.status}")

                data = await response.json()

                return data if data else None
        except asyncio.TimeoutError:
            print("Error: Request timed out")

        except ClientError as e:
            print(f"Client error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")


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


async def scrape_bulk(inputs: List[Tuple[float, float]]):
    data = []
    tasks = [openweather(lat=input[0], lon=input[1]) for input in inputs]
    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            data.append(extract_data(data=result))

    return data


def rich_print(data: List):
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
    for field in data[0].keys():
        borujen_value = str(data[0].get(field))
        tehran_value = str(data[1].get(field))
        shiraz_value = str(data[2].get(field))
        masjed_soleyman_value = str(data[3].get(field))
        mobarakeh_value = str(data[4].get(field))
        gilan_value = str(data[5].get(field))
        ardabil_value = str(data[6].get(field))

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


if __name__ == "__main__":
    inputs = [
        (32.127594, 51.456565),  # Borujen
        (35.6892, 51.3890),  # Tehran
        (29.5918, 52.5836),  # Shiraz
        (31.949249, 49.305954),  # Masjed Soleyman
        (32.34651, 51.50449),  # Mobarakeh
        (37.433, 49.550),  # Gilan
        (38.2498, 48.2933),  # Ardabil
    ]
    data = asyncio.run(main=scrape_bulk(inputs=inputs))
    rich_print(data=data)
