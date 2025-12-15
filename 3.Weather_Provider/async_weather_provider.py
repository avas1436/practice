import asyncio
from typing import Any, Dict, List, Literal, Optional, Tuple

import aiohttp


async def openweather_async(
    session: aiohttp.ClientSession,
    lat: float = 32.127594,
    lon: float = 51.456565,
    mode: Optional[Literal["standard", "metric", "imperial"]] = "metric",
    api: str = "c7f76b6aa6f9be23330e085b601b7b20",
) -> Dict[str, Any]:
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": lat,
            "lon": lon,
            "appid": api,
            "units": mode,
        }

        # اصلاح: اضافه کردن params به درخواست GET
        async with session.get(url=url, params=params) as resp:
            if resp.status >= 400:
                err_text = await resp.text()
                # اصلاح: فرمت صحیح دیکشنری خطا
                return {"error": f"HTTP error {resp.status}: {err_text}"}

            data = await resp.json()

            # بررسی خطاهای API (اگر OpenWeatherMap خطا را در JSON برگرداند)
            if "cod" in data and data["cod"] != 200:
                return {
                    "error": f"API error {data.get('cod')}: {data.get('message', 'Unknown error')}"
                }

            return data

    except asyncio.TimeoutError:
        return {"error": "Request timed out."}
    except aiohttp.ClientError as e:
        return {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        # اصلاح: فرمت صحیح دیکشنری خطا
        return {"error": f"Unexpected error: {str(e)}"}


async def main() -> List[Dict[str, Any]]:
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        locations: List[Tuple[float, float]] = [
            (32.127594, 51.456565),  # Borujen
            (35.6892, 51.3890),  # Tehran
            (29.5918, 52.5836),  # Shiraz
            (31.949249, 49.305954),  # Masjed Soleyman
            (32.34651, 51.50449),  # Mobarakeh
            (37.433, 49.550),  # Gilan
            (38.2498, 48.2933),  # Ardabil
        ]

        tasks = [
            openweather_async(session, lat=lat, lon=lon, mode="metric") for (lat, lon) in locations
        ]

        # استفاده از return_exceptions=True برای جلوگیری از crash کل برنامه
        results_raw = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = []
        for result in results_raw:
            if isinstance(result, Exception):
                processed_results.append({"error": f"Exception: {str(result)}"})
            else:
                processed_results.append(result)

        return processed_results


if __name__ == "__main__":
    final_results = asyncio.run(main())
    for i, item in enumerate(final_results, 1):
        print(f"#{i}", item)
        print("-" * 50)
