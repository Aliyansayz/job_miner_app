import pickle
import os
# from dashboard_function import make_dashboard
import asyncio
# from miner_execute import job_miner_execute


class manage_store:

    def __init__(self):
        folder_path, filename = "storage", "store.bin"
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        self.file_path = os.path.join(folder_path, filename)

        config_folder, filename = "config", "email_config.bin"
        if not os.path.exists(config_folder): os.makedirs(config_folder)
        self.email_config = os.path.join(config_folder, filename)


    def get_keyword_email_store(self):

        # folder_path, filename = "storage", "store.bin"
        # if not os.path.exists(folder_path): os.makedirs(folder_path)
        # cls.file_path = os.path.join(folder_path, filename)
        #
        try:
            pass
            with open(self.file_path, 'rb+') as f:
                store = pickle.load(f)

        except:
            store = {}
            with open(self.file_path, 'wb+') as f:
                pickle.dump(store, f)
            # store[1] = { "keywords": [], "email_list": [] }
            pass

        if not store:
            max_id = 0
        else:
            max_id = max(store.keys())

        print(store)

        return store, max_id

    def push_into_keyword_email_store(self, store):

        # store, _ = self.get_keyword_email_store()

        # store[id] = record

        # store[1] = {"keywords": [], "email_list": []}

        with open(self.file_path, 'wb+') as f:
            pickle.dump(store, f)

        # record = { 'keywords': [vd], 'emails': [dzv] }
        # record = 1
        # store[id] = record

    def get_email_config(self):

        try:
            pass
            with open(self.email_config, 'rb') as f:
                email_config = pickle.load(f)

        except:
            email_config = {"email": "", "password": "", "smtp_server":"", "port": ""}

            with open(self.email_config, 'wb') as f:
                pickle.dump(email_config, f)



        return email_config

    def update_email_config(self, email, password, smtp_server, port):

        with open(self.email_config, 'rb') as f:  email_config = pickle.load(f)

        email_config["email"] = email
        email_config["password"] = password
        email_config["smtp_server"] = smtp_server
        email_config["port"] = port

        with open(self.email_config, 'wb') as f:  pickle.dump(email_config, f)
        pass


class dashboard_email_report:
    pass


html_content_list = []
# for keyword in keywords:
#     html_content = saving_html(record_info, keyword)
#     saving_html(record_info, keyword)
#     html_content_list.append(html_content)

# for email in emails:




class run_agent_exceute(manage_store):


    def run_job_miner(self):
        store = self.get_keyword_email_store()
        for key, value in  store.items():
            keyword_list = value["keywords"]
            recipient_email_list = value["email_list"]
            html_content_list = self.fetch_and_save_reports(keyword_list=keyword_list, multi_keyword=True)
            send_email_with_html( html_content_list, keyword_list, recipient_email_list)
            # send_email




    def fetch_and_save_reports(self, keyword_list, allowed=["upwork"], ):
        html_store = {}
        for platform in allowed:
            if platform == "upwork":
                pass
                asyncio.run(job_miner_execute(keyword=keyword_list, multi_keyword=True))
                html_content_list = [self.reading_html(keyword, platform="upwork") for keyword in keyword_list]
                title_list = [self.compile_title(keyword) for keyword in keyword_list ]
                return html_content_list
        pass

    def compile_title(self, keyword):

        title = f"{keyword} Job Report"
        return title

    def reading_html(self, keyword, platform="upwork"):
        folder_path = f"{platform}_reports"
        filename = f"Job_Mining_{keyword}.html"

        if not os.path.exists(folder_path): os.makedirs(folder_path)
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "rb+") as file: html_content = file.read()
        # Start counter for potential duplicate file names

        return html_content


    def saving_html(record_info, keyword):

        pass
    # import pickle
    # with open(f"record_{keyword}.txt", 'w') as file:
    #     pickle.dump(record_info, file)

    def send_email_with_html(self, html_content_list, keyword_list, recipient_email_list):
        import smtplib, ssl
        from email.mime.text import MIMEText

        email_config = self.get_email_config()

        sender_email, sender_password = email_config["email"], email_config["password"]
        smtp_server, port_num = email_config["smtp_server"], email_config["port"]
        # sender_email = sender_info['email']
        # sender_password = sender_info['password']
        # recipient_email
        if not isinstance(recipient_email_list, list): recipient_email_list = [recipient_email_list]

        # html_message['From'] = sender_email
        # smtp_server
        # port_num
        smtp = smtplib.SMTP(f"{smtp_server}", port=port_num) # port_num smtp_server
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        for target_email in recipient_email_list: # for person A , one keyword jobs then second keyword job report will be emailed
            for html_content, keyword in zip(html_content_list, keyword_list):
                subject = f"{keyword} Report "
                html_message = MIMEText(html_content, 'html')
                html_message['Subject'] = subject

                html_message['To'] = target_email
                # print(target_email)
                smtp.sendmail(sender_email, target_email, html_message.as_string())
        smtp.quit()
