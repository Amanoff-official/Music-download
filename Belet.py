import requests
import os
import sys
import webbrowser
from colorama import Fore, Style

os.system("clear")

def check_and_install_packages():
    try:
        import colorama
        from colorama import Fore, Style
    except ImportError:
        print("Serwerdan zatlar ustanowka edilýä...")
        os.system("pip install colorama requests")
        import colorama
        from colorama import Fore, Style
    colorama.init()

check_and_install_packages()

# Функция для выполнения поиска
def search_query(query):
    url = 'https://web1.ma.st.com.tm/api/v1/search_by_track?page=1&offset=300'
    headers = {
        'User-Agent': 'Dart/3.5 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Authorization': 'd9191bc83b89e75db1f9cc6c67ec5611075a10b41c0ce608bc28cfc280e53a8e',
        'Music-App-Unique-User-Key': '5a1c3a7d-bb2f-4e0b-a2c9-7a8b67d28307'
    }
    payload = {'title': query}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(Fore.GREEN + "Aýdymlar tapyldy." + Style.RESET_ALL)
            results = response.json()
            return results
        else:
            print(Fore.RED + f"Ýalňyşlyk döredi: {response.status_code}" + Style.RESET_ALL)
            return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Ошибка при запросе: {str(e)}" + Style.RESET_ALL)
        return None

# Функция для отображения первых 10 песен
def display_songs(results):
    if results and 'tracks' in results:
        tracks = results['tracks'][:10]  # Показываем только первые 10 песен
        for i, track in enumerate(tracks, start=1):
            song_name = track.get('title', 'Aýdymyň ady belli däl')
            artist_name = track['artists'][0].get('art_name', 'Belli däl') if 'artists' in track and track['artists'] else 'Belli däl'
            file_size = track.get('bit_rate', 'Belli däl')
            print(Fore.YELLOW + f"{i}. Aýdym: {song_name} - {artist_name}")
        return tracks
    else:
        print(Fore.RED + "Aýdym tapylmady." + Style.RESET_ALL)
        return None

# Функция для скачивания песни с проверкой на 404 ошибку
def download_song(song_url, song_name, save_dir):
    try:
        response = requests.get(song_url, stream=True)
        
        if response.status_code == 404:
            print(Fore.RED + f"Ýalňyşlyk: {song_name} aýdym üçin url ýalňyş." + Style.RESET_ALL)
            return
        
        response.raise_for_status()
        
        filename = f"{song_name}.mp3"
        file_path = os.path.join(save_dir, filename)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded_size += len(chunk)
                
                percent = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                sys.stdout.write(Fore.GREEN + f"\rÝüklenýä... {percent:.2f}% " + Style.RESET_ALL)
                sys.stdout.flush()

        print(Fore.GREEN + f"\nÝüklenip boldy: {file_path}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ýalňyşlyk: {str(e)}" + Style.RESET_ALL)

# Функция для выбора способа скачивания
def download_option(song_url, song_name):
    while True:
        download_choice = input(Fore.YELLOW + "\nNäme bilen ýüklemeli? (1 - Telegram bot; 2 - skrypt): " + Style.RESET_ALL)
        
        if download_choice == '1':
            print(Fore.CYAN + "\nBota iwermeli sylka: " + song_url + Style.RESET_ALL)
            print(Fore.GREEN + "Telegram bot: @uploadbot" + Style.RESET_ALL)
            break
        
        elif download_choice == '2':
            save_dir = '/sdcard/Music/Amanoff'
            os.makedirs(save_dir, exist_ok=True)
            download_song(song_url, song_name, save_dir)
            break
        
        else:
            print(Fore.RED + "Ýalňyş saýlaw! Saýlawlaryň arasynda bolmaly." + Style.RESET_ALL)

# Основной блок программы
if __name__ == "__main__":
    user_query = input(Fore.BLUE + "Aýdymyň ady: " + Style.RESET_ALL)
    
    search_results = search_query(user_query)
    
    if search_results:
        print(Fore.GREEN + "Serwerda tapylanlar:" + Style.RESET_ALL)
        song_data = display_songs(search_results)

        if song_data:
            try:
                choice = int(input(Fore.BLUE + "\nAýdym saýlaň (1-10): " + Style.RESET_ALL))
                if 1 <= choice <= 10:
                    selected_song = song_data[choice - 1]
                    song_url = selected_song.get('audio_url', '')
                    song_name = selected_song.get('title', 'Aýdymyň ady belli däl')
                    artist_name = selected_song['artists'][0].get('art_name', 'Belli däl') if 'artists' in selected_song and selected_song['artists'] else 'Belli däl'
                    file_size = selected_song.get('bit_rate', 'Belli däl')

                    print(Fore.CYAN + f"Ýüklenýän aýdym: {song_name} - {artist_name} (Bitrate: {file_size} bps)" + Style.RESET_ALL)

                    # Выбор способа скачивания
                    download_option(song_url, song_name)
                else:
                    print(Fore.RED + "Ýalňyş san girizildi. Saýlawlaryň arasynda bolmaly." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Ýalňyş san girizildi." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Ýalňyşlyk: Aýdymlar tapylmady." + Style.RESET_ALL)