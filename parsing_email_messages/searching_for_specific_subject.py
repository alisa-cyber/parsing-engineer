import imaplib
import email
from email.header import decode_header
from collections import Counter
import re
import os
import sys

# Меняю текущую рабочую директорию на эту, чтобы прочитать файл с логином и паролем
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(current_dir)

# нужно создать свой файл credentials.txt и положить туда логин почты и пароль для приложения
with open("credentials.txt", "r", encoding="utf-8") as file:
    EMAIL_ACCOUNT = file.readline().rstrip()
    PASSWORD = file.readline().rstrip()

my_server = "yandex.ru"  # альтернативно можно использовать mail.ru
# Данные для подключения
IMAP_SERVER = "imap.yandex.ru" if my_server == "yandex.ru" else "imap.mail.ru"

# Устанавливаем соединение с почтовым сервером
mail = imaplib.IMAP4_SSL(IMAP_SERVER)

# Логинимся
mail.login(EMAIL_ACCOUNT, PASSWORD)

# Выбираем папку "Входящие"
mail.select("inbox")


status, response = mail.search(None, "SEEN")

# Слово для поиска в письмах
search_word = "скидки"

if status == "OK":
    email_ids = response[0].split()  # Список ID всех писем
    print(f"Темы писем, содержащие слово '{search_word}':")
    for email_id in email_ids:
        # Получаем сообщение по ID
        status, msg_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (SUBJECT)])")
        # print(msg_data)

        if status == "OK":
            # Декодируем полученные заголовки
            for response_part in msg_data:

                if isinstance(response_part, tuple):
                    # Получаем сообщение
                    msg = email.message_from_bytes(response_part[1])

                    # Извлекаем тему письма
                    try:
                        subject, encoding = decode_header(msg.get("Subject"))[0]
                    except:
                        continue

                    # Если тема закодирована в base64 или другой кодировке
                    if isinstance(subject, bytes):
                        try:
                            subject = subject.decode(encoding or "utf-8")
                        except:
                            continue

                    # Проверяем, если в теме содержится слово "Фильмы"
                    if subject and search_word.lower() in subject.lower():
                        print(f"Тема (содержит слово '{search_word}'): {subject}")


# Закрываем соединение
mail.logout()
