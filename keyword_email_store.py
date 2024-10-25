import pickle
import os
from dashboard_function import make_dashboard
import asyncio
from miner_execute import job_miner_execute


class manage_store_send_email:

    def get_keyword_email_store(self):

        try:
            pass
            with open('store.bin', 'r') as f: store = pickle.load(f)

        except :
            store = {}
            with open('store.bin', 'w') as f: pickle.dump(store, f)
            # store[1] = { "keywords": [], "email_list": [] }
            pass

        if not store: max_id = 0
        else:  max_id = max(store.keys())

        return store, max_id



    def push_into_keyword_email_store(self, id, record):


        store, _ = self.get_keyword_email_store()

        store[id] = record

        store[1] = {"keywords": [], "email_list": []}

        with open('store.bin', 'w') as f:
                pickle.dump(store, f)

        # record = { 'keywords': [vd], 'emails': [dzv] }
        # record = 1
        # store[id] = record



    def get_email_config(self):

        try:
            pass
            with open('email_config.bin', 'r') as f:  email_config = pickle.load(f)

        except:
            email_config = { "email": "",  "password": ""}

            with open('email_config.bin', 'w') as f:  pickle.dump(email_config, f)

        email = email_config["email"]
        password = email_config["password"]

        return email, password


    def update_email_config(self, email, password):


        with open('email_config.bin', 'r') as f:  email_config = pickle.load(f)

        email_config["email"]    = email
        email_config["password"] = password

        with open('email_config.bin', 'w') as f:  pickle.dump(email_config, f)
        pass



class dashboard_email_report:

    pass

html_content_list = []
for keyword in keywords:
      html_content = saving_html(record_info, keyword)
      saving_html(record_info, keyword)
      html_content_list.append(html_content)

for email in emails: 
    

def send_email_with_html(cls, html_content_list, keyword_list sender_info, recipient_email, tf=""):
        import smtplib, ssl
        from email.mime.text import MIMEText

        sender_email = sender_info['email']
        sender_password = sender_info['password']
        # recipient_email
        if isinstance(recipient_email, list): recipient_email = list(recipient_email)

        
        html_message['From']  = sender_email
        
        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        for target_email in recipient_email:
            for html_content, keyword in zip(html_content_list, keyword_list):
                subject = f"{keyword} Report "
                html_message = MIMEText(html_content, 'html')
                html_message['Subject'] = subject
            
                html_message['To'] = target_email
                print(target_email)
                smtp.sendmail(sender_email, target_email, html_message.as_string())
        smtp.quit()


def run_job_miner():

    for key, value in store.items():
        keyword_list  = value["keywords"]
        email_list    = value["email_list"]
        html_content_list = fetch_and_save_reports(keyword=keyword_list, multi_keyword=True)
        send_email
    
    title = f"{keyword} Job Report"
    
def fetch_and_save_reports(keyword=keyword_list, allowed=["upwork"], ):
    html_store = {}
    for platform in allowed:
        if platform == "upwork":
            pass
            asyncio.run(job_miner_execute(keyword=keyword_list, multi_keyword=True))
            html_content_list =  [ reading_html(keyword, platform="upwork") for keyword in keyword_list ] 
            return html_content_list 
    pass    
    
def reading_html(keyword, platform="upwork"):

    folder_path = f"{platform}_reports"
    filename = f"Job_Mining_{keyword}.html"


    if not os.path.exists(folder_path): os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "r") as file: html_content = file.read()
    # Start counter for potential duplicate file names

    return html_content
    
def saving_html(record_info, keyword):

    # import pickle
    # with open(f"record_{keyword}.txt", 'w') as file:
    #     pickle.dump(record_info, file)


    
