def make_dashboard(jobs_dict, job_type=""):
    """
    Generates an HTML string for the Job Mining Dashboard.

    :param jobs_dict: Dictionary where keys are job titles and values are dictionaries containing job details
                      like pricing, description, and proposal draft.
    :return: HTML string
    """
    # HTML template parts
    head = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Job Mining Dashboard {job_type} </title>'''+\
                '''<style>
                    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap');
                    body {
                        font-family: 'Raleway', sans-serif;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                    }
                    .container {
                        width: 100%;
                        max-width: 900px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    .header {
                        text-align: center;
                        margin-bottom: 20px;
                    }
                    .header h1 {
                        margin: 0;
                        font-size: 28px;
                        color: #333;
                        font-weight: 700;
                    }
                    .job {
                        background-color: #f9f9f9;
                        margin-bottom: 15px;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    .job h2 {
                        margin: 0;
                        font-size: 24px;
                        color: #333;
                    }
                    .job .price {
                        font-size: 18px;
                        color: #007bff;
                        margin-top: 10px;
                    }
                    .collapsible {
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
                    }
                    .content {
                        padding: 15px;
                        display: none;
                        overflow: hidden;
                        background-color: #f9f9f9;
                        margin-bottom: 10px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    .footer {
                        text-align: center;
                        font-size: 14px;
                        color: #777;
                        margin-top: 20px;
                        border-top: 1px solid #ddd;
                        padding-top: 10px;
                    }
                </style>
                <script>
                    function toggleContent(id) {
                        var content = document.getElementById(id);
                        if (content.style.display === "none") {
                            content.style.display = "block";
                        } else {
                            content.style.display = "none";
                        }
                    }
                </script>
            </head>'''+\
            f'''<body>
                <div class="container">
                    <div class="header">
                        <h1>Job Mining Dashboard {job_type} </h1>
                    </div>
    '''

    job_items = ''


    for job_id, job_info in jobs_dict.items():

        job_posted = job_info.get('posted', 'N/A')
        if job_posted not in ['minutes', 'hours', 'hour', 'minute'] :
                continue

        job_price = job_info.get('value', 'N/A')
        job_type  = job_info.get('type', 'N/A')
        job_price = job_price + f" {job_type}"

        job_description = job_info.get('description', 'No description available.')
        job_proposal = job_info.get('proposal', 'No proposal available.')
        job_proposal_numbers = job_info.get('job_proposals', 'N/A')
        job_title = job_info.get('title', 'N/A')
        job_link =  job_info.get('url', 'N/A')
        job_items += f'''
            <div class="job">
                <a href="{job_link} ">{job_title}</a>
                <div class="price"><strong>Price:</strong> {job_price}</div>
                <div class="price"><strong>Price:</strong> {job_proposal_numbers}</div>
                <button class="collapsible" onclick="toggleContent('{job_title}_desc')">Job Description</button>
                <div class="content" id="{job_title}_desc">{job_description}</div>

                <button class="collapsible" onclick="toggleContent('{job_title}_proposal')">Job Proposal</button>
                <div class="content" id="{job_title}_proposal">{job_proposal}</div>
            </div>
        '''

    footer = '''
                <div class="footer">
                    <p>&copy; 2024 Job Mining Dashboard. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
    '''

    whole_html = head + job_items + footer
    return whole_html
