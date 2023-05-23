import re
from selenium import webdriver
from bs4 import BeautifulSoup

# Установите путь к веб-драйверу для выбранного браузера
webdriver_path = 'C:\\Windows\\chromedriver.exe'
# Создание экземпляра веб-драйвера
driver = webdriver.Chrome(executable_path=webdriver_path)

while True:
    # Чтение следующей ссылки из файла input.txt
    with open('input.txt', 'r+', encoding='utf-8') as input_file:
        lines = input_file.readlines()
        # Проверка, если ссылка пустая, то выход из цикла
        if not lines:
            break

        url = lines[0].strip()
        # Удаление прочитанной строки из файла
        input_file.seek(0)
        input_file.writelines(lines[1:])
        input_file.truncate()

    # url = 'https://1ww.frkp.live/film/1009536/'

    # Перейти на страницу
    driver.get(url)

    # Получение кода, который виден в инспекторе браузера
    html = driver.page_source

    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Находим ссылку в iframe из div с классом kinobox__menuItem
    iframe = soup.find('div', class_='kinobox__menuItem')

    # Получаем значение атрибута 'data-iframe-url' у найденного элемента
    iframe_src = iframe['data-iframe-url']

    # Перейти на страницу
    driver.get(iframe_src)

    # Получение кода, который виден в инспекторе браузера
    iframe_html = driver.page_source

    # Используем регулярное выражение для поиска ссылки с шаблоном "title: " и ","
    pattern_title = r'title:\s*"([^"]*)"'
    match_title = re.search(pattern_title, iframe_html)

    # Используем регулярное выражение для поиска ссылки с шаблоном "hls: " и ","
    pattern_hls = r'hls:\s*"([^"]*)"'
    match_hls = re.search(pattern_hls, iframe_html)

    if match_title and match_hls:
        title = match_title.group(1).replace(' ', '_')
        link_hls = match_hls.group(1)
        download_link = 'https://dl.getzend.digital/video-download?m=' + link_hls + '&name=' + title

        # Запись ссылки в файл out.txt
        with open('out.txt', 'a', encoding='utf-8') as output_file:
            output_file.write(download_link + '\n')
    else:
        print("Ссылка и/или заголовок не найдены")

# Закрытие браузера
driver.quit()
