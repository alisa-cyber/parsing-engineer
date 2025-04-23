import imaplib
import email
from email.header import decode_header
from collections import Counter
import re
import os
import sys


sender_counter = Counter()

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

#  Получаем количество непрочитанных писем
status, response = mail.search(None, "UNSEEN")  # Получаем список всех непрочитанных писем
if status == "OK":
    email_ids = response[0].split()  # Список ID всех писем
    num_emails = len(email_ids)  # Количество писем
    print(f"1.Количество непрочитанных писем: {num_emails}")

#  Получаем количество прочитанных писем 
status, response = mail.search(None, "SEEN")  # Получаем список всех писем
if status == "OK":
    email_ids = response[0].split()  # Список ID всех писем
    num_emails = len(email_ids)  # Количество писем
    print(f"2.Количество прочитанных писем: {num_emails}")
    # Проходимся по всем прочитанным письмам
    for email_id in email_ids:
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
                    try:
                        email_address = re.search(r"<(.+?)>", from_)
                        if email_address:
                            from_ = email_address.group(1)  # Адрес электронной почты
                            sender_counter[
                                from_
                            ] += 1  # Добавляем отправителя в Counter
                    except:
                        continue

# Получаем топ-5 отправителей
top_senders = sender_counter.most_common(5)
print("Топ 5 отправителей:")
for sender, count in top_senders:
    print(f"{sender}: {count} писем")


# Закрываем соединение
mail.logout()
