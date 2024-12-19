import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import random

# 날씨 API 호출 (예: OpenWeatherMap)
def get_weather(city):
    api_key = open('apikey', 'r').readline()  # OpenWeatherMap API 키를 넣으세요
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temperature = data["main"]["temp"]
            weather = data["weather"][0]["main"]
            return temperature, weather
        else:
            raise Exception("City not found")
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None, None

# 날씨에 따른 노래 리스트
def recommend_music(weather):
    music_recommendations = {
        "Rain": ["Rainy day - PATEKO (파테코) Feat. ASH ISLAND, Skinny Brown", "우산 - 에픽하이(Feat.윤하)", "Paris in the Rain - LAUV"],
        "Clear": ["우주를 줄게 - 볼빨간사춘기", "Happy - Pharrell Williams", "파도 - 폴킴"],
        "Clouds": ["Warm On A Cold Night - HONNE", "Life Goes ON - BTS", "Coldplay - Fix You"],
        "Snow": ["눈이 오잖아 - 이무진(Feat.헤이즈)", "첫눈 - EXO", "Snowman - Sia"],
        "Drizzle": ["Paris - The Chainsmokers", "비오는날 듣기 좋은노래 - 에픽하이(Feat.콜드)"],
        "Thunderstorm": ["Thunder - Imagine Dragons", "Bohemian Rhapsody - Queen"],
        "Mist": ["Lucid Dreams - Juice WRLD", "Daylight - David Kushner"]
    }
    song_list = music_recommendations.get(weather, ["Classical Music Playlist", "A generic relaxing mix"])
    return random.choice(song_list)  # 랜덤으로 한 곡 반환

# 날씨에 따른 이미지 선택
def select_image(weather):
    images = {
        "Rain": "images/rain.jpg",
        "Clear": "images/clear.jpg",
        "Clouds": "images/clouds.jpg",
        "Snow": "images/snow.jpg",
        "Drizzle": "images/drizzle.jpg",
        "Thunderstorm": "images/thunderstorm.jpg",
        "Mist": "images/mist.jpg"
    }
    return images.get(weather, "images/default.jpg")

# 날씨 정보와 음악 추천을 가져오는 함수
def fetch_and_recommend():
    city = city_entry.get()
    if city:
        temp, weather = get_weather(city)
        if weather:
            song = recommend_music(weather)  # 랜덤으로 한 곡 반환
            image_path = select_image(weather)  # 날씨에 따른 이미지 경로 가져오기
            display_image(image_path)  # 이미지 업데이트
            result_label.config(
                text=f"날씨: {weather}\n추천된 노래: {song}"  # 불필요한 줄바꿈 제거
            )
        else:
            result_label.config(text="Could not fetch weather data.")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

# 이미지 표시
def display_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((400, 300))  # 이미지 크기 조정
        photo = ImageTk.PhotoImage(img)
        weather_image_label.config(image=photo)
        weather_image_label.image = photo  # 이미지 참조 유지
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image: {e}")

# UI 초기화
root = tk.Tk()
root.title("Weatherfy")
root.geometry("500x600")
root.config(bg="#f0f0f0")

# 제목 레이블
title_label = tk.Label(root, text="Weatherfy", font=("Helvetica", 16, "bold"), bg="#81b71a", fg="white", padx=5, pady=5)
title_label.pack(pady=10)

# 도시 입력 레이블
city_label = tk.Label(root, text="도시를 입력해주세요:", font=("Helvetica", 12), bg="#f0f0f0")
city_label.pack(pady=5)

# 도시 입력 텍스트 박스
city_entry = tk.Entry(root, font=("Helvetica", 12), width=20)
city_entry.pack(pady=5)

# 추천 버튼
recommend_button = tk.Button(root, text="Get Music", font=("Helvetica", 12), command=fetch_and_recommend, bg="#4CAF50", fg="white", padx=10, pady=5)
recommend_button.pack(pady=20)

# 날씨 이미지 표시 레이블
weather_image_label = tk.Label(root, bg="#f0f0f0")
weather_image_label.pack(pady=10)

# 결과 레이블
result_label = tk.Label(root, text="날씨: \n추천된 노래: ", font=("Helvetica", 12), bg="#f0f0f0", justify="left")
result_label.pack(pady=10)

# 앱 실행
root.mainloop()
