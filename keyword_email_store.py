import pickle
import os



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

def saving_html(record_info, keyword):

    # import pickle
    # with open(f"record_{keyword}.txt", 'w') as file:
    #     pickle.dump(record_info, file)


    html_content = generate_html(record_info, keyword)

    folder_path = "reports"
    filename = f"Job_Mining_{keyword}.html"

    if not os.path.exists(folder_path): os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)

    # Start counter for potential duplicate file names
    counter = 1
    file_root, file_extension = os.path.splitext(file_path)

    # While loop to check if file exists, and increment counter if it does
    while os.path.exists(file_path):
        file_path = f"{file_root}_{counter}{file_extension}"
        counter += 1

    with open(file_path, "w") as file:
        file.write(html_content)
