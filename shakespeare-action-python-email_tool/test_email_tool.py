from email_tool import send_email, receive_email
import sys


assets = {
    "username": "17602143142@163.com",
    "password": "123456",
    "smtp_host": "smtp.163.com",
    "smtp_port": None,
    "imap_host": "imap.163.com",
    "imap_port": None,
    "ssl": True
}

params = {
    "sender": "",
    "receiver": "17602143142@163.com",
    "subject": "test",
    "text_body": "hello"
}

# result = send_email(params, assets, context_info={})
params = {}
result = receive_email(params, assets, context_info={})
print(result)


