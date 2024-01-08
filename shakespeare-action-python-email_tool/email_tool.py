import os
import uuid
import email
import smtplib
import imaplib
from traceback import format_exc
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.header import Header
from action_sdk_for_cache.action_cache_sdk import HoneyGuide


class EmailReceiveClient:

    def __init__(self, username, password, imap_server, imap_port, need_ssl=False):
        """
        构造函数
        :param username: 邮箱登录账号
        :param password: 邮箱登录密码
        :param imap_server: 邮箱服务器
        :param imap_port: 邮箱服务器端口
        :param need_ssl: 是否需要ssl加密
        """
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.need_ssl = need_ssl
        self.imap_port = imap_port
        self.imap_client = None

    def imap_login(self):
        """
        imap 登录邮箱, 登录后默认选择操作收件箱,
        备注参考: https://blog.csdn.net/jony_online/article/details/108638571
        :return: 登录结果, dict, eg: {"status_code": 200, "message": "imap login ok"}
        """
        try:
            imaplib.Commands['ID'] = 'AUTH'
            if self.need_ssl:
                server = imaplib.IMAP4_SSL(host=self.imap_server, port=self.imap_port)
            else:
                server = imaplib.IMAP4(host=self.imap_server, port=self.imap_port)
            server.login(self.username, self.password)
            args = ("name", "python_email_tool", "contact", "17602143142@163.com",
                    "version", "1.0.0", "vendor", "myclient")
            typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
            print(server._untagged_response(typ, dat, 'ID'))
        except Exception as e:
            error_info = "imap login fail for the reason of: {0}, detail reason: {1}"
            return {"status_code": 400, "message": error_info.format(repr(e), format_exc())}
        self.imap_client = server
        self.select(section="INBOX")    # 默认解析收件箱信息
        return {"status_code": 200, "message": "imap login ok"}

    def show_folders(self):
        """
        返回邮箱所有文件夹
        :return: tuple, eg:
        ("ok", [b'() "/" "INBOX"', b'(\\Drafts) "/" "&g0l6P3ux-"',
        b'(\\Sent) "/" "&XfJT0ZAB-"', b'(\\Trash) "/" "&XfJSIJZk-"',
        b'(\\Junk) "/" "&V4NXPpCuTvY-"', b'() "/" "&dcVr0mWHTvZZOQ-"'])
        """
        return self.imap_client.list()

    def select(self, section):
        """
        选择解析信息的区域,不清楚可以调用show_folders查看已有区域
        :param section: str, eg: "INBOX"
        :return: tuple, eg: ('OK', [b'1'])
        """
        return self.imap_client.select(section)

    def search(self, charset, *criteria):
        """
        搜索邮件(参照RFC文档http://tools.ietf.org/html/rfc3501#page-49)
        """
        return self.imap_client.search(charset, *criteria)

    def get_unread(self):
        """
        返回所有未读的邮件列表(返回的是包含邮件序号的列表),注意邮箱系统可能默认只能接收最近30天的邮件,
        所以可能会看到这里为空的
        :returns tuple, eg: ('OK', [b'1 2'])
        """
        return self.search(None, "Unseen")  # Unseen 表示未读邮件,ALL 表示所有邮件

    def get_email_format(self, num):
        """
        以RFC822协议格式返回邮件详情的email对象
        :param num: str, digit, eg: "1"
        :return dict, eg: {"status_code": 200, "message": format_result}
        """
        print(type(num), "aaa {0} bbb".format(num))
        data = self.imap_client.fetch(num, 'RFC822')
        status = data[0]
        content = data[1]
        if status == 'OK':
            return {"status_code": 200, "message": email.message_from_string(str(content[0][1], encoding="utf-8"))}
        else:
            return {"status_code": 400, "message": "fetch error, error info: {0}".format(content)}

    @staticmethod
    def get_sender_info(msg):
        """
        返回发送者的信息——元组（邮件称呼，邮件地址）
        :param msg: email对象
        :return: tuple, eg: ("eason", "17000000000@163.com")
        """
        print("msg from: ", msg["from"])
        name = email.utils.parseaddr(msg["from"])[0]
        decode_name = email.header.decode_header(name)[0]
        if decode_name[1] is not None:
            name = str(decode_name[0], decode_name[1])
        address = email.utils.parseaddr(msg["from"])[1]
        return name, address

    @staticmethod
    def get_receiver_info(msg):
        """
        返回接受者的信息——元组（邮件称呼，邮件地址）
        :param msg: email对象
        :return: tuple
        """
        name = email.utils.parseaddr(msg["to"])[0]
        decode_name = email.header.decode_header(name)[0]
        if decode_name[1] is not None:
            name = str(decode_name[0], decode_name[1])
        address = email.utils.parseaddr(msg["to"])[1]
        return name, address

    @staticmethod
    def get_subject_content(msg):
        """
        返回邮件的主题(参数msg是email对象，可调用get_email_format获得)
        :param msg: email对象
        :return: str
        """
        decode_content = email.header.decode_header(msg['subject'])[0]
        if decode_content[1] is not None:
            return str(decode_content[0], decode_content[1])
        return decode_content[0]

    @staticmethod
    def parse_attachment(message_part):
        """
        判断是否有附件，并解析（解析email对象的part）
        返回列表（内容类型，大小，文件名，数据流）
        :param message_part: email对象的part
        :return: dict, keys: content_type, size, name, data
        """
        content_disposition = message_part.get("Content-Disposition", None)
        if content_disposition:
            dispositions = content_disposition.strip().split(";")
            print("dispositions: ", dispositions)
            invalid_character = r'<>:"/\|?* '
            if bool(content_disposition and dispositions[0].lower() == "attachment"):
                if 'message/rfc822' == message_part.get_content_type():
                    payload = message_part.get_payload()
                    attachment = {
                        "content_type": message_part.get_content_type(),
                    }
                    print("payload: ", payload)
                    for mail in payload:
                        mail2 = email.message_from_bytes(mail.as_bytes())
                        subject = EmailReceiveClient.get_subject_content(mail2)
                        for char in invalid_character:
                            subject = subject.replace(char, '')
                        # filename = subject + ".eml"
                        mail_content = mail.as_bytes()
                        attachment["size"] = len(mail_content)
                        attachment["name"] = subject + "_" + str(uuid.uuid1()) + ".eml"
                        attachment["data"] = mail_content
                else:
                    file_data = message_part.get_payload(decode=True)
                    attachment = {"content_type": message_part.get_content_type(),
                                  "size": len(file_data)
                                  }
                    print("attachment: ", attachment)
                    decode_name = email.header.decode_header(message_part.get_filename())[0]
                    name = decode_name[0]
                    if decode_name[1] is not None:
                        name = str(decode_name[0], decode_name[1])
                    for char in invalid_character:
                        name = name.replace(char, '')
                    attachment["name"] = os.path.splitext(name)[0] + "_" + str(uuid.uuid1()) \
                        + os.path.splitext(name)[1]
                    attachment["data"] = file_data
                return attachment
        return None

    def get_mail_info(self, num):
        """
        返回邮件的解析后信息部分
        返回列表包含（主题，纯文本正文部分，html的正文部分，发件人元组，收件人元组，附件列表）
        :param num: str, digit,表示检索区域的邮件编号
        :return: dict, eg:
        {"status_code": 200,
         "message": {"subject": "", "body": "", "html": "", "from": "", "to": "", "attachments": []}
        }
        """
        msg = self.get_email_format(num)
        if msg["status_code"] == 200:
            msg = msg["message"]
        else:
            return {"status_code": 400, "message": msg["message"]}
        attachments = []
        body = None
        html = None
        try:
            for part in msg.walk():
                charset = part.get_content_charset()
                if charset is None:
                    charset = part.get_charset()
                if not charset:
                    charset = "utf-8"
                attachment = self.parse_attachment(part)
                if attachment:
                    attachments.append(attachment)
                elif part.get_content_type() == "text/plain":
                    if body is None:
                        body = ""
                    try:
                        body += str(part.get_payload(decode=True), encoding=charset)
                    except UnicodeDecodeError:
                        try:
                            if charset == "utf-8":
                                body += str(part.get_payload(decode=True), encoding="gb2312")
                            elif charset == "gb2312":
                                body += str(part.get_payload(decode=True), encoding="utf-8")
                        except UnicodeDecodeError:
                            body += str(part.get_payload(decode=True))
                elif part.get_content_type() == "text/html":
                    if html is None:
                        html = ""
                    try:
                        html += str(part.get_payload(decode=True), encoding=charset)
                    except UnicodeDecodeError:
                        try:
                            if charset == "utf-8":
                                html += str(part.get_payload(decode=True), encoding="gb2312")
                            elif charset == "gb2312":
                                html += str(part.get_payload(decode=True), encoding="utf-8")
                        except UnicodeDecodeError:
                            html += str(part.get_payload(decode=True))
        except Exception as e:
            self.mark_unseen(num=str(num))
            error_info = "receive email failed, exception: {0}, detail: {1}".format(repr(e), format_exc())
            return {"status_code": 400, "message": error_info}
        return {"status_code": 200,
                "message": {
                    'subject': self.get_subject_content(msg),
                    'body': body,
                    'html': html,
                    'from': self.get_sender_info(msg),
                    'to': self.get_receiver_info(msg),
                    'attachments': attachments
                    }
                }

    def mark_unseen(self, num):
        """
        将指定邮件标记为未读
        :param num: 指定区域邮件的编号
        :return: None
        """
        self.imap_client.store(num, '-FLAGS', r'\Seen')


class EmailSendClient:

    def __init__(self, username, password, smtp_server, smtp_port, sender, need_ssl=False, need_tsl=False):
        """
        构造函数
        :param username: 邮箱登录用户名, str, eg: EasonXiao@qq.com
        :param password: 邮箱登录密码,或授权码, str
        :param smtp_server: smtp邮箱服务器, str, eg: smtp.qq.com
        :param smtp_port: smtp邮箱服务器端口, int, eg: 25
        :param sender: 发件人,有时登录用户名是不带@xxx的, 所以需要设置发件人信息
        :param need_ssl: 是否需要ssl加密, boolean, 默认 False
        """
        self.username = username
        self.password = password
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.need_ssl = need_ssl
        self.need_tsl = need_tsl
        self.smtp_client = None
        self.msg = MIMEMultipart()

    def smtp_login(self):
        """
        smtp登录邮箱
        :return: 返回登录结果, dict, eg: {"status_code": 200, "message": "smtp login ok"}
        """
        try:
            if self.need_ssl:
                server = smtplib.SMTP_SSL(host=self.smtp_server, port=int(self.smtp_port))
            else:
                server = smtplib.SMTP(host=self.smtp_server, port=int(self.smtp_port))
                if self.need_tsl:
                    server.starttls()
            server.ehlo()
            server.set_debuglevel(debuglevel=1)
            server.login(self.username, self.password)
        except Exception as e:
            error_info = "smtp login fail for the reason of: {0}, detail reason: {1}"
            return {"status_code": 400, "message": error_info.format(repr(e), format_exc())}
        self.smtp_client = server
        return {"status_code": 200, "message": "smtp login ok"}

    # def __del__(self):
    #    """
    #    对象销毁时，关闭邮箱服务器的连接
    #    :return: None
    #    """
    #    self.smtp_client.close()

    def re_init_mail_info(self):
        """
        重新初始化邮件信息部分
        :return: None
        """
        self.msg = MIMEMultipart()

    def set_mail_info(self, receiver, subject, sender=None, text=None, html=None, cc=None,
                      bcc=None, attachment_file_paths=None):
        """
        设置邮件的基本信息(收件人,主题,文本正文,html正文,cc,bcc,附件路径列表)
        :param receiver: 收件人, str, 多个收件人,用英文逗号隔开, eg: eason@qq.com,xiao@qq.com
        :param subject: 邮件主题, str, eg: 发工资啦!
        :param sender: 发件人, str, default None, 不填则为登录用户名, eg: xiao@qq.com
        :param text: 邮件文本正文, str, default None, eg: 您本月工资单如下 xxx
        :param html: 邮件html正文, str, default None, eg: <html><body><h1>您本月工资单如下</h1></body></html>
        :param cc: 邮件抄送对象, str, 多个对象用英文逗号隔开, eg: eason@qq.com,xiao@qq.com
        :param bcc: 邮件暗送对象, str, 多个对象用英文逗号隔开, eg: eason@qq.com,xiao@qq.com
        :param attachment_file_paths: 邮件附件, list, default None,表示无附件信息, eg: ["/home/eason/selfile.jpg"]
        :return: None
        """
        if sender is None:
            self.msg['From'] = self.username
        else:
            self.msg["From"] = sender
        self.msg['To'] = receiver
        if cc is not None:
            self.msg["cc"] = cc
        if bcc is not None:
            self.msg["bcc"] = bcc
        self.msg['Subject'] = subject
        if text is not None:
            self.add_text_part(text=text, text_type="plain")
        if html is not None:
            self.add_text_part(text=html, text_type="html")
        if attachment_file_paths is None:
            attachment_file_paths = []
        for attachment_file_path in attachment_file_paths:
            self.msg.attach(self.get_attachment_from_file(attachment_file_path))

    def add_text_part(self, text, text_type, text_charset="utf-8"):
        """
        自定义邮件正文信息(正文内容,正文内容格式html或者plain)
        :param text: 正文内容, str
        :param text_type: 正文内容格式, str
        :param text_charset: 内容编码, str, 默认utf-8
        :return: None
        """
        self.msg.attach(MIMEText(text, text_type, _charset=text_charset))

    def add_attachment(self, filename, file_data):
        """
        增加附件（以流形式添加，可以添加网络获取等流格式）参数（文件名，文件流）
        :param filename: 附件名称, str, eg: selife.jpg, 文件名,不带路径
        :param file_data: 数据流, eg: open("selife.jpg", "rb").read()
        :return: None
        """
        part = MIMEBase('application', "octet-stream")
        part.set_payload(file_data)
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(str(Header(filename, 'utf8'))))
        self.msg.attach(part)

    def add_part(self, part):
        """
        通用方法添加邮件信息(MIMETEXT，MIMEIMAGE,MIMEBASE...)
        :param part: MIMETEXT，MIMEIMAGE,MIMEBASE等对象
        :return:
        """
        self.msg.attach(part)

    @staticmethod
    def get_attachment_from_file(attachment_file_path):
        """
        添加附件
        :param attachment_file_path: 附件文件名(带路径), str, eg: /home/selfile.jpg
        :return: MIMEBase object
        """
        if not os.path.exists(attachment_file_path):
            raise ValueError("待添加的附件不存在,请确认文件名是否正确,是否带文件路径")
        part = MIMEBase('application', "octet-stream")
        with open(attachment_file_path, "rb") as f:
            part.set_payload(f.read())
        filename = os.path.basename(attachment_file_path)
        encode_base64(part)
        # part.add_header('Content-Disposition',
        #                 'attachment; filename="{0}"'.format(str(Header(filename, 'utf8')))
        #                 )
        part.add_header("Content-Disposition", "attachment", filename="{0}".format(str(Header(filename, 'utf8'))))
        return part

    def send_mail(self):
        """
        发送邮件
        :return: 发送邮件结果, dict, eg: {"status_code": 200, "message": "smtp email sent"}
        """
        try:
            all_to = self.msg["To"].split(",")
            if self.msg["cc"]:
                all_to.extend(self.msg["cc"].split(","))
            if self.msg["bcc"]:
                all_to.extend(self.msg["bcc"].split(","))
            if self.smtp_client is None:
                self.smtp_login()
            self.smtp_client.sendmail(self.sender, all_to, self.msg.as_string())
            return {"status_code": 200, "message": "smtp email sent"}
        except Exception as e:
            error_info = "smtp email sent fail for the reason of: {0}, detail reason: {1}"
            return {"status_code": 400, "message": error_info.format(repr(e), format_exc())}


def health_check(params, assets, context_info):
    """
    健康检查
    """
    # smtp服务器信息,如smtp.163.com
    smtp_host = assets["smtp_host"]
    # 发件人信息
    sender = assets["sender"]
    # 邮箱登录账号
    username = assets["username"]
    # 是否使用ssl,默认不使用
    need_ssl = assets["ssl"] if "ssl" in assets and assets["ssl"] is not None else False
    # 是否使用tsl,默认不使用
    need_tsl = assets["tsl"] if "tsl" in assets and assets["tsl"] is not None else False
    # smtp服务器端口,不填ssl为True则默认465,False则默认为25
    smtp_port = int(assets["smtp_port"]) if "smtp_port" in assets and assets["smtp_port"] else None
    if smtp_port is None:
        if need_ssl:
            smtp_port = 465
        elif need_tsl:
            smtp_port = 587
        else:
            smtp_port = 25
    # 邮箱登录密码或授权码
    password = assets["password"]
    json_ret = {"code": 200, "msg": "", "data": {"result": ""}}
    send_client = EmailSendClient(
        username=username, password=password, sender=sender,
        smtp_server=smtp_host, smtp_port=smtp_port, need_ssl=need_ssl, need_tsl=need_tsl
    )
    smtp_login_result = send_client.smtp_login()
    if smtp_login_result["status_code"] == 200:
        json_ret["data"]["result"] = "登录成功,资产健康"
    else:
        json_ret["code"] = smtp_login_result["status_code"]
        json_ret["msg"] = smtp_login_result["message"]
        json_ret["data"]["result"] = "登录失败,资产异常"
    return json_ret 


def send_email(params, assets, context_info):
    """
    发送邮件
    """
    # smtp服务器信息,如smtp.163.com
    smtp_host = assets["smtp_host"]
    # 发件人信息
    sender = assets["sender"]
    # 邮箱登录账号
    username = assets["username"]
    # 是否使用ssl,默认不使用
    need_ssl = assets["ssl"] if "ssl" in assets and assets["ssl"] is not None else False
    # 是否使用tsl,默认不使用
    need_tsl = assets["tsl"] if "tsl" in assets and assets["tsl"] is not None else False
    # smtp服务器端口,不填ssl为True则默认465,False则默认为25
    smtp_port = int(assets["smtp_port"]) if "smtp_port" in assets and assets["smtp_port"] else None
    if smtp_port is None:
        if need_ssl:
            smtp_port = 465
        elif need_tsl:
            smtp_port = 587
        else:
            smtp_port = 25
    # 邮箱登录密码或授权码
    password = assets["password"]
    json_ret = {"code": 200, "msg": "", "data": {"result": ""}}
    send_client = EmailSendClient(
        username=username, password=password, sender=sender,
        smtp_server=smtp_host, smtp_port=smtp_port, need_ssl=need_ssl, need_tsl=need_tsl
    )
    smtp_login_result = send_client.smtp_login()
    if smtp_login_result["status_code"] != 200:
        json_ret["code"] = smtp_login_result["status_code"]
        json_ret["msg"] = smtp_login_result["message"]
        return json_ret
    # 收件人
    receiver = params["receiver"]
    # 抄送
    cc = params["cc"] if "cc" in params and params["cc"] else None
    # 暗送
    bcc = params["bcc"] if "bcc" in params and params["bcc"] else None
    # 邮件主题
    subject = params["subject"]
    # 邮件内容
    text_body = params["text_body"] if "text_body" in params and params["text_body"] else None
    html_body = params["html_body"] if "html_body" in params and params["html_body"] else None
    # 邮件附件,如果附件文件需要自己从本地上传,添加多个附件可以压缩在一个文件中,
    # 如果附件在服务器上,多个附件则用英文逗号隔开即可,此时注意文件带上绝对路径,eg: /home/a.jpg,/home/b.jpg
    attachment = params["attachment"] if "attachment" in params and params["attachment"] else None
    if attachment:
        attachment = attachment.split(",")
    # 发件人,不填则默认用邮箱用户名作为发件人
    sender = params["sender"] if "sender" in params and params["sender"] else username
    send_client.set_mail_info(
        receiver=receiver, subject=subject, sender=sender, text=text_body,
        html=html_body, cc=cc, bcc=bcc, attachment_file_paths=attachment
    )
    send_result = send_client.send_mail()
    if send_result["status_code"] == 200:
        json_ret["data"]["result"] = "邮件发送成功"
    else:
        json_ret["code"] = send_result["status_code"]
        json_ret["msg"] = send_result["message"]
    return json_ret 


def receive_email(params, assets, context_info):
    """
    接收指定用户邮件
    """
    # imap服务器信息,如imap.163.com
    imap_host = assets["imap_host"]
    # 邮箱登录账号
    username = assets["username"]
    hg_client = HoneyGuide(context_info=context_info)
    hg_client.fileCache.localFilePath()
    validate_save_dir = hg_client.fileCache.localFilePath()
    # 是否使用ssl,默认不使用
    need_ssl = assets["ssl"] if "ssl" in assets and assets["ssl"] is not None else False
    # imap服务器端口,不填ssl为True则默认993,False则默认为143
    imap_port = int(assets["imap_port"]) if "imap_port" in assets and assets["imap_port"] else None
    if imap_port is None:
        if need_ssl:
            imap_port = 993
        else:
            imap_port = 143
    # 邮箱登录密码或授权码
    password = assets["password"]
    json_ret = {"code": 200, "msg": "", "data": {"result": [], "column": []}}
    receive_client = EmailReceiveClient(
        username=username, password=password,
        imap_server=imap_host, imap_port=imap_port, need_ssl=need_ssl
    )
    # 收件箱中发件人
    sender = params["sender"] if "sender" in params and params["sender"] else None
    # 标题
    subject = params["subject"] if "subject" in params and params["subject"] else None
    # 其他邮件筛选条件, eg: {""}
    # filter_condition = params["filter_condition"]
    login_result = receive_client.imap_login()
    if login_result["status_code"] != 200:
        json_ret["code"] = login_result["status_code"]
        json_ret["msg"] = login_result["message"]
        return json_ret
    unread_data = receive_client.get_unread()
    if unread_data[0] != "OK":
        json_ret["code"] = 400
        json_ret["msg"] = "get unread email failed, reason: {0}".format(unread_data[1])
        return json_ret
    all_results = []
    print(unread_data[1][0])
    for num in str(unread_data[1][0], encoding="utf-8").split(' '):
        tmp_result = dict()
        if num:
            mail_info = receive_client.get_mail_info(num)
            if mail_info["status_code"] != 200:
                receive_client.mark_unseen(num=str(num))
                continue
            mail_info = mail_info["message"]
            if subject and mail_info["subject"] != subject:
                receive_client.mark_unseen(num=str(num))
                continue
            if sender and mail_info["from"] not in sender.split(","):
                receive_client.mark_unseen(num=str(num))
                continue
            try:
                file_path = os.path.join(validate_save_dir, "sender_{0}".format(mail_info["from"][1]))
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                attachment_list = []
                # 遍历附件列表
                for attachment in mail_info['attachments']:
                    filename = os.path.join(file_path, attachment["name"])
                    with open(filename, "wb") as f:
                        f.write(attachment['data'])
                    attachment_list.append({"name": attachment["name"], "file_path": filename})
                tmp_result["sender"] = mail_info["from"][1]
                tmp_result["subject"] = mail_info["subject"]
                tmp_result["body"] = mail_info["body"]
                tmp_result["html"] = mail_info["html"]
                tmp_result["attachments"] = attachment_list
            except Exception as e:
                receive_client.mark_unseen(num=str(num))
                json_ret["code"] = 400
                json_ret["msg"] = "receive email failed, exception: {0}, detail: {1}".format(repr(e), format_exc())
                return json_ret
        all_results.append(tmp_result)
    json_ret = {"code": 200, "msg": "", "data": {"result": all_results, "column": []}}
    json_ret["data"]["column"] = ["sender", "subject", "body", "html", "attachments"]
    return json_ret
