import requests
import sys
import os

# Функция для выполнения поиска
def search_query(query):
    url = f'https://aydym.com/api/v3/search?mask={query}'
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print("Aýdymlar tapyldy.")
            results = response.json()
            return results
        else:
            print("Ýalňyşlyk döredi:", response.status_code)
            return None
    except Exception as e:
        print("Ýalňyşlyk:", str(e))
        return None

# Функция для отображения песен
def display_songs(results):
    if 'songs' in results and 'data' in results['songs']:
        songs = results['songs']['data']
        if songs:
            for index, song in enumerate(songs, start=1):
                song_name = song.get('name', 'Aýdymyň ady belli däl')
                print(f"Aýdym: {index}: {song_name}")
            return songs  # Возвращаем список песен для дальнейшей работы
        else:
            print("Aýdym tapylmady.")
            return []
    else:
        print("Aýdym tapylmady.")
        return []

# Функция для скачивания песни с прогрессом
def download_song(song_url, song_name, save_dir):
    try:
        response = requests.get(song_url, stream=True)  # Получаем поток данных
        response.raise_for_status()  # Проверяем, успешен ли запрос
        
        # Формируем имя файла для сохранения
        filename = f"{song_name}.mp3"  # Имя файла берём из названия песни
        file_path = os.path.join(save_dir, filename)  # Полный путь для сохранения
        total_size = int(response.headers.get('content-length', 0))  # Получаем общий размер файла
        downloaded_size = 0  # Количество уже загруженных данных

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)  # Записываем данные в файл
                downloaded_size += len(chunk)  # Обновляем количество загруженных данных
                
                # Вычисляем процент завершения
                percent = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                sys.stdout.write(f"\rÝüklenýä... {percent:.2f}%")
                sys.stdout.flush()  # Обновляем вывод

        print(f"\nÝüklenip boldy: {file_path}")
    except Exception as e:
        print(f"Ýalňyşlyk: {str(e)}")

# В основном блоке программы
if __name__ == "__main__":
    user_query = input("Aýdymyň ady: ")
    
    # Выполняем поиск
    search_results = search_query(user_query)
    
    # Показываем только названия песен
    if search_results:
        print("Serwerda tapylanlar:")
        songs = display_songs(search_results)

        if songs:  # Проверяем, есть ли найденные песни
            song_number = input("Haýsy aýdymy ýüklemeli bolsa sanyny ýaz: ")
            try:
                song_number = int(song_number)  # Преобразуем ввод в целое число
                if 1 <= song_number <= len(songs):
                    song_name = songs[song_number - 1]['name']  # Получаем имя песни
                    song_url = songs[song_number - 1]['audioFile']['url']  # Получаем URL песни
                    
                    # Определяем директорию для сохранения
                    save_dir = '/sdcard/Music/Amanoff'
                    os.makedirs(save_dir, exist_ok=True)  # Создаем директорию, если она не существует

                    download_song(song_url, song_name, save_dir)  # Вызываем функцию для скачивания
                else:
                    print("Ýaňlyş san.")
            except ValueError:
                print("Dogry san ýaz.")