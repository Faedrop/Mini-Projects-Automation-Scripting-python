import requests
from tkinter import messagebox,ttk
import tkinter as tk
import threading


API_KEY = "bbf8a73e3970c8fedbe8b30f8fa2072d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return None  # City not found or other HTTP error
    except Exception:
        return None 

if __name__ == "__main__":
    print("App running")
# --gui
root = tk.Tk()
root.title("Weather APP")
root.geometry("500x400")
main_frame = ttk.Frame(root)
main_frame.pack(pady=20)


input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Enter City Name:").pack(side=tk.LEFT, padx=5)
city_entry = ttk.Entry(input_frame)
city_entry.pack(side=tk.LEFT, padx=5)
city_entry.focus()

weather_frame = ttk.Frame(main_frame)
weather_frame.pack(pady=10)

city_label = ttk.Label(weather_frame, text="Weather Info:")
city_label.pack()
temp_label = ttk.Label(weather_frame, text="")
temp_label.pack()

condition_label = ttk.Label(weather_frame, text="", font=('Arial', 14))
condition_label.pack(pady=5)

details_label = ttk.Label(weather_frame, text="", font=('Arial', 12))
details_label.pack(pady=5)

error_label = ttk.Label(weather_frame, text="", font=('Arial', 12), foreground='red')
error_label.pack(pady=10)

def clear_weather_display():
    """Clear all weather labels and hide error."""
    city_label.config(text="")
    temp_label.config(text="")
    condition_label.config(text="")
    details_label.config(text="")
    error_label.config(text="")

def display_weather(data):
    """Display weather data in the individual labels."""
    clear_weather_display()
    
    weather_desc = data['weather'][0]['description'].title()
    temperature = data['main']['temp']
    city_found = data['name']
    humidity = data['main']['humidity']
    feels_like = data['main']['feels_like']
    
   
    city_label.config(text=city_found)
    temp_label.config(text=f"{temperature}°C")
    condition_label.config(text=weather_desc)
    details_label.config(text=f"Humidity: {humidity}% | Feels like: {feels_like}°C")

def display_error(message):
    """Display an error message."""
    clear_weather_display()
    error_label.config(text=message)

def get_weather_gui():
    city_name = city_entry.get().strip()
    if not city_name:
        display_error("⚠️ Please enter a city name.")
        return
        
    get_weather_button.config(state="disabled")
    clear_weather_display()
    error_label.config(text="⏳ Fetching weather data...")
    root.update_idletasks()  # Force GUI update
    
    data = get_weather(city_name)
    
    if data:
        display_weather(data)
    else:
        display_error(f" Could not find weather for '{city_name}'. Please check the city name.")
    
    get_weather_button.config(state="normal")

get_weather_button = ttk.Button(input_frame, text="Get Weather", command=get_weather_gui)
get_weather_button.pack(side=tk.LEFT, padx=10)


root.bind('<Return>', lambda event: get_weather_gui())
root.mainloop()