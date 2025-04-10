# Анализатор лог-файла access.log

## Описание

Этот скрипт предназначен для анализа лог-файла `access.log`. 

Он собирает следующую статистику:

- Общее количество выполненных запросов.
- Количество запросов по HTTP-методам: GET, POST, PUT, DELETE, OPTIONS, HEAD.
- Топ 3 IP-адресов с наибольшим количеством запросов.
- Топ 3 самых долгих запросов с указанием метода, URL, IP, длительности и даты/времени.

## Установка

1. Убедитесь, что у вас установлен Python 3.
2. Скачайте архив `access.log`. 
3. Скопируйте скрипт в директорию вашего проекта.

## Описание работы:

1. Используется регулярное выражение для извлечения необходимых полей из каждой строки лога.
2. Подсчитывает общее количество запросов и количество запросов по HTTP-методам
3. Определяет топ 3 IP-адресов с наибольшим количеством запросов. 
4. Определяет топ 3 самых долгих запросов, используя список top_longest, который поддерживает сортировку по длительности.
5. Используется модуль argparse для обработки аргументов командной строки.
6. Если указанный путь является директорией, скрипт ищет все файлы с расширением .log.
7. Если указанный путь является файлом, обрабатывает только этот файл.
8. Для каждого лог-файла выводит результаты в терминал и сохраняет их в отдельный JSON-файл с тем же именем и расширением .json.
9. Результаты сохраняются в формате JSON.

```bash
 python3 parser_web_log.py /Users/userqa/Documents/logs (вставить ваш путь до файла `access.log`

