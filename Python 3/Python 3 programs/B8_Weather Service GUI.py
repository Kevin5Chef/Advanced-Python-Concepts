import tkinter as tk
from tkinter import messagebox
import random
import time
import logging
from datetime import datetime, timedelta
print("SY-5, Kevin Victor, Roll No.-30")
# ================= LOGGING SETUP =================
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ================= CUSTOM EXCEPTIONS =================

class WeatherAppError(Exception):
    pass

class StationNotFoundError(WeatherAppError):
    pass

class StationOfflineError(WeatherAppError):
    pass

class WeatherTimeoutError(WeatherAppError):
    pass

class NetworkFailureError(WeatherAppError):
    pass

class DataStaleError(WeatherAppError):
    pass

class CorruptDataError(WeatherAppError):
    pass


# ================= WEATHER DATABASE =================

stations = {
    "Pune": {
        "online": True,
        "updated": datetime.now(),
        "data": {
            "Temp": 31,
            "Humidity": 42,
            "RealFeel": 33,
            "Cloud": "Partly Cloudy",
            "Wind": "12 km/h",
            "Rain": "0%",
            "UV": 8
        }
    },
    "Mumbai": {
        "online": True,
        "updated": datetime.now(),
        "data": {
            "Temp": 33,
            "Humidity": 71,
            "RealFeel": 38,
            "Cloud": "Humid haze",
            "Wind": "18 km/h",
            "Rain": "10%",
            "UV": 7
        }
    },
    "Delhi": {
        "online": True,
        "updated": datetime.now() - timedelta(minutes=40),  # stale
        "data": {
            "Temp": 29,
            "Humidity": 36,
            "RealFeel": 30,
            "Cloud": "Clear",
            "Wind": "9 km/h",
            "Rain": "0%",
            "UV": 6
        }
    },
    "New York City": {
        "online": False,  # offline station
        "updated": datetime.now(),
        "data": {}
    },
    "Moscow": {
        "online": True,
        "updated": datetime.now(),
        "data": {
            "Temp": -4,
            "Humidity": 81,
            "RealFeel": -8,
            "Cloud": "Overcast",
            "Wind": "22 km/h",
            "Rain": "Snow showers",
            "UV": 1
        }
    }
}

# ================= SERVICE LAYER =================

def fetch_weather(city):

    try:
        # ---- station existence ----
        if city not in stations:
            raise StationNotFoundError("Station not registered in system")

        station = stations[city]

        # ---- offline station ----
        if not station["online"]:
            raise StationOfflineError("Station heartbeat missing")

        # ---- simulated network issues ----
        if random.random() < 0.15:
            raise NetworkFailureError("Socket unreachable")

        # ---- simulated timeout ----
        delay = random.uniform(0, 4)
        if delay > 3:
            raise TimeoutError("API response exceeded threshold")

        time.sleep(delay)

        # ---- stale data check ----
        if datetime.now() - station["updated"] > timedelta(minutes=30):
            raise DataStaleError("Last update too old")

        # ---- corrupt data simulation ----
        if random.random() < 0.1:
            raise ValueError("Malformed payload")

        return station["data"]

    except TimeoutError as e:
        logging.exception("TIMEOUT_ERROR")
        raise WeatherTimeoutError("Weather service is taking too long") from e

    except NetworkFailureError as e:
        logging.exception("NETWORK_FAILURE")
        raise WeatherAppError("Network connection problem detected") from e

    except StationOfflineError as e:
        logging.exception("STATION_OFFLINE")
        raise WeatherAppError("Weather station is currently offline") from e

    except DataStaleError as e:
        logging.exception("STALE_DATA")
        raise WeatherAppError("Weather data is outdated") from e

    except ValueError as e:
        logging.exception("CORRUPT_DATA")
        raise CorruptDataError("Weather data corrupted") from e

    except StationNotFoundError as e:
        logging.exception("UNKNOWN_STATION")
        raise WeatherAppError("No weather station found for this city") from e


# ================= UI LAYER =================

root = tk.Tk()
root.title("Global Weather Monitor")
root.geometry("500x500")

title = tk.Label(root, text="Weather Station Monitor", font=("Arial", 16, "bold"))
title.pack(pady=10)

search_frame = tk.Frame(root)
search_frame.pack(pady=5)

tk.Label(search_frame, text="Enter City: ").pack(side="left")
city_entry = tk.Entry(search_frame)
city_entry.pack(side="left")

output = tk.Text(root, height=18, width=55)
output.pack(pady=10)

def show_weather():

    city = city_entry.get().strip()

    output.delete("1.0", tk.END)

    try:
        data = fetch_weather(city)

        output.insert(tk.END, f"Weather Report for {city}\n")
        output.insert(tk.END, "-"*35 + "\n")

        for k, v in data.items():
            output.insert(tk.END, f"{k}: {v}\n")

    except WeatherAppError as e:

        # -------- USER-FRIENDLY MESSAGE --------
        msg = str(e)

        hint = ""
        if "offline" in msg.lower():
            hint = "Try again later or check another nearby station."
        elif "network" in msg.lower():
            hint = "Check internet connection or firewall rules."
        elif "outdated" in msg.lower():
            hint = "Station needs refresh. Retry in a few minutes."
        elif "taking too long" in msg.lower():
            hint = "Server overloaded. Retry shortly."
        elif "no weather station" in msg.lower():
            hint = "Check spelling or try a major nearby city."
        else:
            hint = "Contact system admin if issue persists."

        messagebox.showerror(
            "Weather Error",
            f"{msg}\n\nHow to resolve:\n{hint}"
        )

        output.insert(tk.END, "Unable to fetch weather.\nSee popup for details.")

btn = tk.Button(root, text="Get Weather", command=show_weather)
btn.pack(pady=5)

root.mainloop()
