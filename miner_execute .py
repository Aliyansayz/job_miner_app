import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import lxml , os, pickle
import html5lib
from playwright.async_api import async_playwright
from job_dashboard import generate_html
import re


def save_into_job_store():
    pass

def create_job_store():

    job_store = {}
    
    return job_store


def filter_special_chars(input_string):
    # Define a regex pattern for allowed characters (letters, numbers, spaces, common punctuation)
    pattern = re.compile(r'[^a-zA-Z0-9\s,.!?\'"(){}[\]\-:;@&%#+/*|<>_=]')  # Add allowed special chars as needed

    # Substitute anything that doesn't match the allowed pattern with an empty string
    filtered_string = pattern.sub('', input_string)

    return filtered_string


def duplicate_files_fix(default_filename):

    counter = 1
    frag = default_filename.split('.')
    name = frag[0]
    ext = frag[1]
    if os.path.exists(default_filename):
        updated_path = f"{name}_{counter}.{ext}"
        # current_path = default_filename
        while os.path.exists(updated_path):
            # current_path = updated_path

            updated_path = f"{name}_{counter}.{ext}"
            counter += 1
        os.rename(default_filename, updated_path)

def update_job_store(job_store, word):

    if word not in job_store:
        job_store[word] = {}
        max_id = 0
        pass

    else : max_id = max(job_store[word].keys())

    record_id = max_id + 1
    # with open('job_store.bin', 'wb') as f:
    #     dill.dump(job_store, f)

    return job_store, record_id



def job_store_save(job_store):

    df = pd.DataFrame.from_dict(job_store)

    # Save DataFrame to CSV
    default_filename = 'job_store.csv'
    df.to_csv(default_filename, index=False)


def scrape_upwork_html(job_store, word, response):

    
    job_store, record_id = update_job_store(job_store, word)

    if word not in job_store:
        job_store[word] = {}
        max_id = 0
        pass

    else : max_id = max(job_store[word].keys())

    record_id = max_id + 1

    # Parse the page content
    soup = BeautifulSoup(response, 'html.parser')
    all_article_tag = soup.find_all('article', class_='job-tile')


    for j, tag in enumerate(all_article_tag):
        job_details = tag.select_one(
            'div[data-test="JobTileDetails"]:nth-child(2) div[data-test="UpCLineClamp JobDescription"] p').text
        job_link_title = tag.select_one('div:nth-child(1) > div:nth-child(1) > div:nth-child(2) a')
        job_type = tag.select_one(
            'div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="job-type-label"]>strong').text
        job_value = tag.select('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="is-fixed-price"] strong')
        job_posted = tag.select('small[data-test="job-pubilshed-date"] >span:nth-of-type(2)')

        job_url = job_link_title.get('href')
        job_url = f"https://www.upwork.com/"+f"{job_url}"
        # Process job value

        if isinstance(job_value, list):
            job_value_str = "".join([str(element.text) for element in job_value])
        else:
            job_value_str = job_value.text

        # Print the job details
        title = job_link_title.text

        title = filter_special_chars(title)
        job_type = filter_special_chars(job_type)
        job_value_str = filter_special_chars(job_value_str)
        job_details   = filter_special_chars(job_details)

        job_store[word][record_id] = {}
        job_store[word][record_id]["title"] = title
        job_store[word][record_id]["type"]  = job_type
        job_store[word][record_id]["value"] = job_value_str
        job_store[word][record_id]["description"] = job_details
        job_store[word][record_id]["job_posted"]  = job_posted

        job_store[word][record_id]["proposal"] = ""
        job_store[word][record_id]["url"]  = f"https://www.upwork.com/" + f"{job_url}"

        job_store[word][record_id]["meta"] = f" 'record_id': {record_id}, 'title': {title}, 'job_type': {job_type}"

        # record_info[record_id]["job_proposals"] = await get_job_proposals_info(record_info[record_id]["url"])
        record_id += 1

    with open('job_store.bin', 'w') as f: pickle.dump(job_store, f)
    # print(record_info)



async def get_job_proposals_info(url):

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, channel='chrome')
        page = await browser.new_page()
        await page.goto(url)
        await page.mouse.wheel(0, 25000)
        response = await page.content()
        soup = BeautifulSoup(response, 'html.parser')
        proposal_info = soup.select('li.ca-item:nth-child(1) > span.value')
        if proposal_info == "" or proposal_info == [] : proposal_info = "apply immediate"

        await browser.close()

    return proposal_info



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

# Scrape job data from a specific keyword
async def job_miner_execute(keyword, multi_keyword=False):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False, channel='chrome')
        page    = await browser.new_page()


        if multi_keyword and isinstance(keyword, list):
            # page1 = await browser.new_page()
            # page2 = await browser.new_page()
            # page3 = await browser.new_page()
            # page4 = await browser.new_page()
            # page5 = await browser.new_page()
            # page_instance = [page1, page2, page3, page4, page5]
            job_store = create_job_store()

            for i, word in enumerate(keyword):
                target_url = f"https://www.upwork.com/nx/search/jobs/?q={word}"
                # page = page_instance[i]
                page = await browser.new_page()

                await page.goto(target_url)
                await page.mouse.wheel(0, 25000)
                await page.screenshot(path=f"{word}_jobs_page.png")
                response = await page.content()

                scrape_upwork_html(word, response)

                await page.wait_for_timeout(2000)

                # page = page_instance[i]
                # page = await browser.new_page()

                # if curr_page != pages_num :
                #     await current_page_instance.click(f'li.air3-pagination-nr:nth-child({5+i}) > button:nth-child(1) > span:nth-child(1) > span:nth-child(2)')

                # response = await page.content()
                # scrape_upwork_html(word, response)

                await page.wait_for_timeout(2000)
                # await browser.close()
                    # saving_html(record_info, word)

                # await page.wait_for_timeout(2000)


            await browser.close()
            pass


        else: return
        # Generate URL for the keyword

        # for i in range(pages_num):
        #     curr_page = i + 1
        #     if curr_page > 1: target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}&page={curr_page}"
        #     else: target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
        #     pass


        # url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
        # url_page_2_onward = f"https://www.upwork.com/nx/search/jobs/?q={keyword}&page={2}"
        # else:
        #     target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
        #     await page.goto(target_url)
        #     await page.mouse.wheel(0, 25000)  # Scroll down the page to load more jobs
        #     # await page.screenshot(path=f"{keyword}_jobs_page.png")  # Save a screenshot for each keyword
        #     response = await page.content()
        #
        #
        #     await asyncio.sleep(5)
        #
        #     record_info = scrape_upwork_html(record_info, record_id, response)
        #     saving_html(record_info, keyword)
        #
        #     await page.wait_for_timeout(2000)
        #     await page.close()
        #     await asyncio.sleep(3)



        await browser.close()



# Main function to run scraping for multiple keywords serially with delay
# async def get_jobs_upwork(keywords, pages_num=2):
#     for keyword in keywords:
#         await scrape_keyword(keyword, pages_num)
#         print(f"Finished scraping for keyword: {keyword}. Waiting for 30 seconds before the next keyword...")
#         await asyncio.sleep(30)  # Wait for 30 seconds before the next request

# List of keywords to search for
# "ruby on rails",

keywords = [ "ruby on rails", "python-visualization", "python-database", "tableau"]
# keywords = ['ruby on rails']
# Run the scraping process
asyncio.run(job_miner_execute(keyword=keywords, multi_keyword=True))

