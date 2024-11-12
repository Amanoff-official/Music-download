import requests
import os
import sys
from colorama import Fore, Style

os.system("clear")

# Функция для выполнения поиска
def search_query(query):
    url = f'https://m.horjuntv.com.tm/cellphone/tm/songs?page=1&search={query}'
    
    try:
        response = requests.get(url)
        
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
    if results and 'songs' in results:
        tracks = results['songs'][:10]  # Показываем только первые 10 песен
        for i, track in enumerate(tracks, start=1):
            song_name = track.get('music_name', 'Aýdymyň ady belli däl')
            artist_name = track['music_awtor'][0].get('awtor', 'Belli däl') if 'music_awtor' in track and track['music_awtor'] else 'Belli däl'
            print(Fore.YELLOW + f"{i}. Aýdym: {song_name} - {artist_name}" + Style.RESET_ALL)
        return tracks
    else:
        print(Fore.RED + "Aýdym tapylmady." + Style.RESET_ALL)
        return None

# Функция для скачивания песни с проверкой на 404 ошибку
def download_song(song_url, song_name, save_dir):
    try:
        response = requests.get(song_url, stream=True)
        
        if response.status_code == 404:
            print(Fore.RED + f"Ýalňyşlyk: Аýdym {song_name} ýok. URL tapylmady." + Style.RESET_ALL)
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
                    song_url = selected_song.get('music', '')
                    song_name = selected_song.get('music_name', 'Aýdymyň ady belli däl')
                    artist_name = selected_song['music_awtor'][0].get('awtor', 'Belli däl') if 'music_awtor' in selected_song and selected_song['music_awtor'] else 'Belli däl'
                    
                    print(Fore.CYAN + f"Ýüklenýän aýdym: {song_name} - {artist_name}" + Style.RESET_ALL)

                    # Выбор способа скачивания
                    download_option = input(Fore.YELLOW + "\nNäme bilen ýüklemeli? (1 - Telegram bot; 2 - skrypt) " + Style.RESET_ALL)
                    
                    if download_option == '1':
                        print(Fore.CYAN + "\nBota iwermeli sylka: " + song_url + Style.RESET_ALL)
                        print(Fore.GREEN + "Telegram bot: @uploadbot" + Style.RESET_ALL)
                    
                    elif download_option == '2':
                        save_dir = '/sdcard/Music/Amanoff'
                        os.makedirs(save_dir, exist_ok=True)
                        download_song(song_url, song_name, save_dir)
                    else:
                        print(Fore.RED + "Ýalňyş saýlaw! Saýlawlaryň arasynda bolmaly." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Ýalňyş san girizildi." + Style.RESET_ALL)
