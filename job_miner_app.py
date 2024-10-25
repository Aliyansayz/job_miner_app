import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget,
                             QPushButton, QComboBox, QLineEdit, QLabel, QTabWidget, QStackedWidget)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSlot
from datetime import datetime, timedelta

from keyword_email_store import manage_store, run_agent_exceute


class SidebarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.run_agent_btn = QPushButton("Run Agent")
        self.dashboard_btn = QPushButton("Dashboard")
        self.settings_btn = QPushButton("Settings")
        self.market_status_btn = QPushButton("Get Market Daily Status")

        layout.addWidget(self.run_agent_btn)
        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.market_status_btn)
        layout.addStretch()


class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Create Tab Widget
        self.tabs = QTabWidget()
        self.handle_keywords =  manage_store()
        self.api_config_tab = self.create_api_config_tab()
        self.email_list_tab = self.create_email_list_tab()
        self.email_config_tab = self.create_email_config_tab()
        self.keywords_tab  = self.create_keywords_tab()

        # Add Tabs to the TabWidget
        self.tabs.addTab(self.keywords_tab, "Keywords tab")
        self.tabs.addTab(self.email_list_tab, "Email List")
        self.tabs.addTab(self.email_config_tab, "Email Config")
        self.tabs.addTab(self.api_config_tab, "API Config")

        # Add Tabs to the main layout
        layout.addWidget(self.tabs)


    def create_api_config_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        layout.addWidget(self.api_key_input)
        self.save_api_btn = QPushButton("Save API Key")
        self.save_api_btn.clicked.connect(self.save_api_settings)
        layout.addWidget(self.save_api_btn)
        layout.addStretch()
        return tab

    def save_api_settings(self):
        api_key = self.api_key_input.text()
        print(f"API Key saved: {api_key}")

    def create_email_list_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Email List:"))
        self.email_list_input = QLineEdit()
        layout.addWidget(self.email_list_input)
        self.save_email_list_btn = QPushButton("Save Email List")
        layout.addWidget(self.save_email_list_btn)
        layout.addStretch()
        return tab

    def create_email_config_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("SMTP Server:"))
        self.smtp_input = QLineEdit()
        layout.addWidget(self.smtp_input)
        layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit()
        layout.addWidget(self.port_input)
        layout.addWidget(QLabel("Email: "))
        self.email_config_input = QLineEdit()
        layout.addWidget(self.email_config_input)
        layout.addWidget(QLabel("Email Password:"))
        self.email_config_password_input = QLineEdit()
        layout.addWidget(self.email_config_password_input)


        email, password = self.handle_keywords.get_email_config()

        self.email_config_input.setText(str(email))
        self.email_config_password_input.setText(str(password))


        self.save_email_config_btn = QPushButton("Save Email Config")

        self.save_email_config_btn.clicked.connect(self.save_keywords)
        layout.addWidget(self.save_email_config_btn)
        layout.addStretch()


        return tab

    def create_keywords_tab(self):

        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Keywords :"))
        self.keyword_input = QLineEdit()
        layout.addWidget(self.keyword_input)

        layout.addWidget(QLabel("Email List :"))
        self.email_list_input = QLineEdit()

        layout.addWidget(self.email_list_input)

        try :
            # find a file if there is any list
            pass
        except: pass

        # self.keyword_input.setText("A,B,C,D")

        keywords_list = self.keyword_input.text()

        keywords_list = keywords_list.split(',')
        email_list  = self.email_list_input.text().split(',')
        # keywords_list = eval(keywords_list)

        print(type(keywords_list))

        print(f"Keyword list saved: {keywords_list}")

        self.save_keyword_btn = QPushButton("Save Keywords")

        # self.save_keyword_btn.clicked.connect(self.sav)

        layout.addWidget(self.save_keyword_btn)

        # Table setup
        self.table = QTableWidget(0, 3)  # 3 columns
        self.table.setHorizontalHeaderLabels(["id", "keywords", "emails"])

        # Buttons
        self.add_button = QPushButton('Add Record')
        self.edit_button = QPushButton('Edit Record')
        self.delete_button = QPushButton('Delete Record')

        # self.add_button.clicked.connect()
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)


        layout.addWidget(self.table)
        layout.addLayout(button_layout)



        # Button signals
        # self.edit_button.clicked.connect(self.edit_row)
        # self.delete_button.clicked.connect(self.delete_row)
        #
        # self.add_table_data(" auto increment id here", "keyword list here", "emails here in a list")
        # self.add_table_data("Jane Smith", "25", "Designer")


        layout.addStretch()

        return tab

    def save_email_config(self):

        pass
        email = self.email_config_input.text()
        password = self.email_config_password_input.text()

        self.handle_keywords.update_email_config(email, password)

    def save_keywords(self):
        """Save or update the input keywords and emails into the table with auto-incrementing or current ID."""

        if ',' in self.keyword_input.text():  keywords_list = self.keyword_input.text().split(',')
        else : keywords_list = list(self.keyword_input.text())

        if ',' in self.email_list_input.text():  email_list = self.email_list_input.text().split(',')
        else:  email_list = list(self.keyword_input.text())

        if not keywords_list or not email_list:
            print("Please enter both keywords and email list.")
            return

        store , max_id = self.handle_keywords.get_keyword_email_store()

        if max_id is not None: self.current_id = max_id + 1
        else: self.current_id = 1

        self.add_record(self.current_id, keywords_list, email_list)


        print(f"Keywords: {keywords_list}, Emails: {email_list} saved.")


    def add_record(self, id_value, keywords, emails):
        """Add a row with the given ID, keywords, and emails to the table."""
        # self.save_keywords()

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(str(id_value)))
        self.table.setItem(row_position, 1, QTableWidgetItem(', '.join(keywords)))
        self.table.setItem(row_position, 2, QTableWidgetItem(emails))


    def update_row(self, id_value, keywords, emails):
        """Update the existing row with the provided ID."""
        row_count = self.table.rowCount()

        for row in range(row_count):
            id_item = self.table.item(row, 0)
            if id_item and int(id_item.text()) == id_value:
                self.table.setItem(row, 1, QTableWidgetItem(', '.join(keywords)))
                self.table.setItem(row, 2, QTableWidgetItem(emails))
                print(f"Row {row} with ID {id_value} updated.")
                return



# class Settings_Controller(SettingsWidget):
#     super().__init__()
#

class DashboardLogic:
    @staticmethod
    def generate_dashboard_html(timeframe, updated=False):
        tf = timeframe
        tz = "GMT"
        current_time = datetime.utcnow()

        if updated:
            assets_dict = {
                "BTC/USD": {
                    "action": "buy",
                    "timeframe": tf,
                    "datetime": (current_time + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
                    "strategy": "Moving Average Crossover",
                    "take_profit": "45000",
                    "stop_loss": "40000"
                },
                "ETH/USD": {
                    "action": "sell",
                    "timeframe": tf,
                    "datetime": (current_time + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                    "strategy": "RSI Overbought",
                    "take_profit": "2800",
                    "stop_loss": "3200"
                },
                "XRP/USD": {
                    "action": "buy",
                    "timeframe": tf,
                    "datetime": (current_time + timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
                    "strategy": "Support Bounce",
                    "take_profit": "0.65",
                    "stop_loss": "0.55"
                }
            }
        else:
            assets_dict = {
                "BTC/USD": {
                    "action": "sell",
                    "timeframe": tf,
                    "datetime": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "strategy": "Resistance Rejection",
                    "take_profit": "38000",
                    "stop_loss": "42000"
                },
                "ETH/USD": {
                    "action": "buy",
                    "timeframe": tf,
                    "datetime": (current_time + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
                    "strategy": "Golden Cross",
                    "take_profit": "3500",
                    "stop_loss": "3000"
                }
            }

        return DashboardLogic.generate_html(assets_dict, tf, tz)

    @staticmethod
    def generate_html(jobs_dict, job_types, current_type_index):
        """
        Generates an HTML string for the Job Mining Dashboard with pagination for job types.

        :param jobs_dict: Dictionary of job types and their associated jobs.
        :param job_types: List of job types to paginate through.
        :param current_type_index: Index of the current job type in the pagination.
        :return: HTML string with job details and pagination controls.
        """
        current_job_type = "Python"
        #job_types = list(jobs_dict.keys())
        # current_type_index = 0
        # current_job_type = job_types[current_type_index]
        # jobs = jobs_dict[current_job_type]

        head = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Job Mining Dashboard - {current_job_type}</title>
                <style>
                    body {{
                        font-family: 'Raleway', sans-serif;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                    }}
                    .container {{
                        width: 100%;
                        max-width: 900px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        color: #333;
                    }}
                    .job {{
                        background-color: #f9f9f9;
                        margin-bottom: 15px;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .job h2 {{
                        margin: 0;
                        font-size: 24px;
                        color: #333;
                    }}
                    .job .price {{
                        font-size: 18px;
                        color: #007bff;
                        margin-top: 10px;
                    }}
                    .collapsible {{
                        background-color: #f1f1f1;
                        color: #333;
                        cursor: pointer;
                        padding: 15px;
                        width: 100%;
                        border: none;
                        text-align: left;
                        outline: none;
                        font-size: 18px;
                        font-weight: 600;
                        margin-top: 15px;
                        border-radius: 5px;
                    }}
                    .content {{
                        padding: 15px;
                        display: none;
                        overflow: hidden;
                        background-color: #f9f9f9;
                        margin-bottom: 10px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .pagination {{
                        text-align: center;
                        margin-top: 20px;
                    }}
                    .pagination button {{
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        cursor: pointer;
                        margin: 0 5px;
                        border-radius: 5px;
                    }}
                    .pagination button:disabled {{
                        background-color: #ddd;
                        cursor: not-allowed;
                    }}
                </style>
                <script>
                    function toggleContent(id) {{
                        var content = document.getElementById(id);
                        if (content.style.display === "none") {{
                            content.style.display = "block";
                        }} else {{
                            content.style.display = "none";
                        }}
                    }}
                </script>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Job Mining Dashboard - {current_job_type}</h1>
                    </div>
        '''

        job_items = ''
        jobs = {}
        # Generate job listings for the current job type
        for job_id, job_info in jobs.items():
            job_price = job_info.get('value', 'N/A')
            job_type = job_info.get('type', 'N/A')
            job_price = f"{job_price} {job_type}"

            job_description = job_info.get('description', 'No description available.')
            job_proposal = job_info.get('proposal', 'No proposal available.')
            job_title = job_info.get('title', 'N/A')
            job_link = job_info.get('url', 'N/A')

            job_items += f'''
                <div class="job">
                    <a href="{job_link}">{job_title}</a>
                    <div class="price"><strong>Price:</strong> {job_price}</div>
                    <button class="collapsible" onclick="toggleContent('{job_title}_desc')">Job Description</button>
                    <div class="content" id="{job_title}_desc">{job_description}</div>
                    <button class="collapsible" onclick="toggleContent('{job_title}_proposal')">Job Proposal</button>
                    <div class="content" id="{job_title}_proposal">{job_proposal}</div>
                </div>
            '''

        # Pagination controls
        pagination = '''
            <div class="pagination">
        '''

        # if current_type_index > 0:
        #     pagination += f'<button onclick="window.location.href=\'/previous?index={current_type_index - 1}\'">Previous</button>'
        # else:
        #     pagination += '<button disabled>Previous</button>'
        #
        # if current_type_index < len(job_types) - 1:
        #     pagination += f'<button onclick="window.location.href=\'/next?index={current_type_index + 1}\'">Next</button>'
        # else:
        #     pagination += '<button disabled>Next</button>'
        #
        # pagination += '</div>'

        footer = '''
                <div class="footer">
                    <p>&copy; 2024 Job Mining Dashboard. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        '''

        whole_html = head + job_items + "pagination" + footer
        return whole_html


class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.web_view = QWebEngineView()
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["15m", "1h", "4h", "1d"])
        self.update_button = QPushButton("Update Dashboard")

        layout.addWidget(self.web_view)
        layout.addWidget(self.timeframe_combo)
        layout.addWidget(self.update_button)

    def load_dashboard(self, updated=False):
        html_content = DashboardLogic.generate_dashboard_html(self.timeframe_combo.currentText(), updated)
        self.web_view.setHtml(html_content)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Dashboard With Sidebar Settings")
        self.setGeometry(100, 100, 1200, 800)

        self.handle_keywords = manage_store()


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        self.sidebar = SidebarWidget()
        main_layout.addWidget(self.sidebar, 1)

        # Main content area
        self.content_stack = QStackedWidget()
        self.dashboard_widget = DashboardWidget()
        self.settings_widget = SettingsWidget()  # Use the new SettingsWidget class
        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.settings_widget)
        main_layout.addWidget(self.content_stack, 4)

        # Connect signals
        self.sidebar.run_agent_btn.clicked.connect( self.run_agent )
        self.sidebar.dashboard_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.dashboard_widget))
        self.sidebar.settings_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.settings_widget))
        self.sidebar.market_status_btn.clicked.connect(self.get_market_daily_status)
        self.dashboard_widget.update_button.clicked.connect(self.update_dashboard)



        # Connect settings save button actions
        # self.settings_widget.save_api_btn.clicked.connect(self.save_api_settings) # save api button is node of -> settings widget
        self.settings_widget.save_email_list_btn.clicked.connect(self.save_email_list) # and button method connect -> to function that runs
        self.settings_widget.save_email_config_btn.clicked.connect(self.save_email_config)
        self.settings_widget.save_keyword_btn.clicked.connect(self.save_keywords_list)
        self.retrieve_record()

        # Initial load of the dashboard
        self.dashboard_widget.load_dashboard()

    @pyqtSlot()
    def update_dashboard(self):
        self.dashboard_widget.load_dashboard(updated=True)

    # def save_settings(self):
    #     api_key = self.settings_widget.api_key_input.text()
    #     # Here you would typically save the API key securely
    #     print(f"API Key saved: {api_key}")

    def get_market_daily_status(self):
        # Placeholder function for getting market daily status
        pass

    @pyqtSlot()
    def update_dashboard(self):
        self.dashboard_widget.load_dashboard(updated=True)

    def save_api_settings(self):
        api_key = self.settings_widget.api_key_input.text()
        print(f"API Key saved: {api_key}")

    def save_email_list(self):
        email_list = self.settings_widget.email_list_input.text()
        print(f"Email list saved: {email_list}")

    def save_email_config(self):
        smtp = self.settings_widget.smtp_input.text()
        port = self.settings_widget.port_input.text()
        username = self.settings_widget.username_input.text()
        password = self.settings_widget.password_input.text()
        print(f"Email config saved: {smtp}, {port}, {username}, {password}")

    def save_keywords_list(self):
        """Save or update the input keywords and emails into the table with auto-incrementing or current ID."""

        if ',' in self.settings_widget.keyword_input.text():  keywords_list = self.settings_widget.keyword_input.text().split(',')
        else : keywords_list = list(self.settings_widget.keyword_input.text())

        if ',' in self.settings_widget.email_list_input.text():  email_list = self.settings_widget.email_list_input.text().split(',')
        else:  email_list = list(self.settings_widget.email_list_input.text())

        if not keywords_list or not email_list:
            print("Please enter both keywords and email list.")
            return

        print(f"Keyword saved: {keywords_list}")

        print(f"Email list saved: {email_list}")

        store , max_id = self.handle_keywords.get_keyword_email_store()

        if max_id is not None: current_id = max_id + 1
        else: current_id = 1

        store[current_id] = {"keywords": keywords_list, "email_list": email_list}
        self.handle_keywords.push_into_keyword_email_store(store)
        # self.settings_widget.table
        self.add_record(current_id, keywords_list, email_list)
        print(f"Keywords: {keywords_list}, Emails: {email_list} saved.")

    # def save_keywords_list(self):
    #
    #     keywords_list = self.settings_widget.keyword_input.text()
    #
    #     self.settings_widget.table
    #
    #     # keywords_list = self.keyword_input.text()
    #     keywords_list = keywords_list.split(',')
    #
    #     print(f"License Key saved: {keywords_list}")
    #     email_list = self.settings_widget.email_list_input.text()
    #     print(f"Email list saved: {email_list}")

    def retrieve_record(self):

        store, max_id = self.handle_keywords.get_keyword_email_store()
        print("Store record", store)
        for i in range(1, max_id+1):
            pass
            keywords = store[i]["keywords"]
            emails   = store[i]["email_list"]
            self.add_record(i, keywords, emails)

    def add_record(self, id_value, keywords, emails):
        """Add a row with the given ID, keywords, and emails to the table."""
        # self.save_keywords()

        row_position = self.settings_widget.table.rowCount()
        self.settings_widget.table.insertRow(row_position)

        self.settings_widget.table.setItem(row_position, 0, QTableWidgetItem(str(id_value)))
        self.settings_widget.table.setItem(row_position, 1, QTableWidgetItem(', '.join(keywords)))
        self.settings_widget.table.setItem(row_position, 2, QTableWidgetItem(emails))

    def run_agent(self):
        executor = run_agent_exceute()
        executor.run_job_miner()
        
        pass


    def get_market_daily_status(self):
        # Placeholder function for getting market daily status
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
