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


status, response = mail.search(
    None, "UNSEEN"
)  # Получаем список всех непрочитанных писем
if status == "OK":
    email_ids = response[0].split()  # Список ID всех писем
    # Проходимся по всем прочитанным письмам
    for email_id in email_ids[-10:-1]:  # прохожусь по последним 10 письмм
        # Получаем сообщение по ID
        status, msg_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (FROM SUBJECT)])")

        if status == "OK":
            # Декодируем полученные заголовки
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Получаем сообщение
                    msg = email.message_from_bytes(response_part[1])

                    # Извлекаем отправителя
                    from_ = msg.get("From")
                    subject = msg.get("Subject")

                    # Декодируем информацию, если она закодирована
                    from_ = decode_header(from_)[0][0] if from_ else None
                    subject = decode_header(subject)[0][0] if subject else None

                    # Преобразуем в строку, если это байты
                    try:
                        if isinstance(from_, bytes):
                            from_ = from_.decode()
                        if isinstance(subject, bytes):
                            subject = subject.decode()
                        print(f"Отправитель: {from_}")
                        print(f"Тема: {subject}")
                    except UnicodeDecodeError:
                        print("I tried to decode message and i failed")

                    print("-" * 50)


# Закрываем соединение
mail.logout()
