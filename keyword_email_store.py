import pickle, json
import os
# from dashboard_function import make_dashboard
import asyncio
# from miner_execute import job_miner_execute
from urllib.request import urlopen

class manage_store:

    def __init__(self):
        folder_path, filename = "storage", "store.bin"
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        self.file_path = os.path.join(folder_path, filename)

        config_folder, filename = "config", "email_config.bin"
        if not os.path.exists(config_folder): os.makedirs(config_folder)
        self.email_config = os.path.join(config_folder, filename)

        filename = "schedule_config.bin"
        self.schedule_config = os.path.join(config_folder, filename)

    def save_schedule_config(self, schedule_mode):
        with open(self.schedule_config, 'wb') as f: pickle.dump(schedule_mode, f)

        pass

    def get_schedule_mode_status(self):
        try :
            with open(self.schedule_config, 'rb')as f: schedule_mode = pickle.load(f)

        except:
            schedule_mode = { "status": False, "interval": 0 }
            with open(self.schedule_config, 'wb')as f: pickle.dump(schedule_mode,f)
        return schedule_mode

    def get_keyword_email_store(self):

        # folder_path, filename = "storage", "store.bin"
        # if not os.path.exists(folder_path): os.makedirs(folder_path)
        # cls.file_path = os.path.join(folder_path, filename)
        #
        try:
            pass
            with open(self.file_path, 'rb') as f:
                store = pickle.load(f)

        except:
            store = {}
            with open(self.file_path, 'wb') as f:
                pickle.dump(store, f)
            # store[1] = { "keywords": [], "email_list": [] }
            pass

        if not store:
            max_id = 0
        else:
            max_id = max(store.keys())

        print(store)
        print(max_id)
        return store, max_id

    def push_into_keyword_email_store(self, store):

        # store, _ = self.get_keyword_email_store()

        # store[id] = record

        # store[1] = {"keywords": [], "email_list": []}

        with open(self.file_path, 'wb') as f:
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

    def create_registry_string_value(self, current_date_str):

        # import yfinance as yf
        import calendar
        # Create a ticker object for gold
        # ticker_symbol = "EUR=X"

        # Fetch data
        # data = yf.download(tickers=ticker_symbol, interval="1D", period="1d")
        current_date = current_date_str

        current_year = current_date_str[0:4]

        current_month = current_date_str[5:7]


        def get_month_info(month, year):
            # Get the name of the month
            month_name = calendar.month_name[month]
            # Get the first day of the month
            first_day = calendar.weekday(year, month, 1)
            weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                        3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

            return month_name, weekdays.get(first_day)


        current_day = current_date_str[8:10]
        # if int(current_day) < 15:
        month_name, first_day = get_month_info(month=int(current_month), year=int(current_year))
        string_value = f"{first_day}+{month_name}+01+{current_year}+job_mining"  # Monday_April_01_2024

        return string_value
        # else:
        #     month_name, first_day = get_month_info_15(month=int(current_month), year=int(current_year))
        #     string_value = f"{first_day}_{month_name}_15_{current_year}"

    def get_registry_status(self):

        print("checking registry status")
        from datetime import datetime
        import yfinance as yf
        import calendar
        # Get the current date
        current_date = datetime.now().date()
        ticker_symbol = "EUR=X"

        # Fetch data
        # data = yf.download(tickers=ticker_symbol, interval="1D", period="5d")
        res = urlopen('http://just-the-time.appspot.com/')

        date_ = str(res.read().strip()).split('b')

        print(date_)
        current_date_str = str(date_[1][1:11])

        comparison_date_str = "2025-12-24"  # Comparison date in string format
        print(current_date_str)
        print(comparison_date_str)
        print(type(current_date_str))
        print(type(comparison_date_str))

        # Define the comparison date
        # comparison_date = datetime(2024, 12, 14).date()



        # Convert string dates to datetime objects
        comparison_date = datetime.strptime(comparison_date_str, "%Y-%m-%d")
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")


        # Check if the current date is before December 14, 2024
        if current_date > comparison_date:
            string_value = self.create_registry_string_value(current_date_str)
            status = self.compare_pass(string_value)
            return status
        else:
            return True

    def compare_pass(self, string_value):

        import hashlib

        try :
            with open("license.txt", "r") as f:
                user_input = f.read()
        except:
            user_input = "123"
            with open("license.txt", "w") as f:
                 f.write(user_input)


        hex_string = string_value.encode().hex()
        # print(month_name, hex_string)
        salt_value = len(string_value)

        salt = str(salt_value).encode()

        # Create a password hash using SHA-256
        password_hash = hashlib.sha256(hex_string.encode() + salt).hexdigest()

        if user_input == password_hash:
            return True
        else:
            return False


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
