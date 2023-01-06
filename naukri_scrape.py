'''
This script scrapes first 50 pages data from naukri.com for data analyst jobs
'''



import time
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScarpeNaukri(webdriver.Chrome):
    def __init__(self, driver_path, teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        super().__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
        self.base_url = "https://www.naukri.com/data-analyst-jobs-{}"
        
    
    def __exit__(self, *args):
        if self.teardown:
            self.quit()
    
    def goto_naukri_site(self, page=1):
        self.get(self.base_url.format(page))

    def scrape(self):
        scrapped_data = []
        num_pages = 50
        for page_no in range(1, num_pages+1):
            self.goto_naukri_site(page=page_no)
            WebDriverWait(self, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            job_cards_list = self.find_element(by=By.CLASS_NAME, value="list")
            job_cards = job_cards_list.find_elements(by=By.TAG_NAME, value="article")
            for job_card in job_cards:
                job_card.click()
                time.sleep(2)

                WebDriverWait(self, 10).until(EC.number_of_windows_to_be(2))
                self.switch_to.window(self.window_handles[1])
                time.sleep(1)

                try:
                    job_title = WebDriverWait(self, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jd-header-title"))
                    ).text
                except:
                    self.close()
                    self.switch_to.window(self.window_handles[0])
                    continue


                company_name = self.find_element(by=By.CLASS_NAME, value="jd-header-comp-name").text
                experience = self.find_element(by=By.CLASS_NAME, value="exp").text
                salary = self.find_element(by=By.CLASS_NAME, value="salary").text
                location = self.find_element(by=By.CLASS_NAME, value="loc").text
                job_description = self.find_element(by=By.CLASS_NAME, value="dang-inner-html").text
                role = self.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[1]/span/a').text
                industry_type = self.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[2]/span/a').text
                department = self.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[3]/span/span').text
                employment_type = self.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[4]/span/span').text
                role_category = self.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[5]/span/span').text
                education = self.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/div[2]/section[2]/div[3]/div[2]/span').text
                key_skills = self.find_element(by=By.CLASS_NAME, value="key-skill")
                key_skills = key_skills.find_elements(by=By.TAG_NAME, value="a")
                key_skills = [key_skill.text for key_skill in key_skills]

                stats_elems = self.find_elements(by=By.CLASS_NAME, value='stat')
                date_posted = None
                num_openings = None
                num_applicants = None
                
                for stat_elem in stats_elems:
                    label = stat_elem.find_element(by=By.TAG_NAME, value='label').text 
                    stat = stat_elem.find_element(by=By.TAG_NAME, value='span').text
                    if label == 'Posted:':
                        date_posted = stat
                    elif label == 'Openings:':
                        num_openings = stat
                    elif label == 'Job Applicants:':
                        num_applicants = stat


                # close the second tab
                self.close()

                # switch to the first tab
                self.switch_to.window(self.window_handles[0])
                current_scraped_data = {
                    "job_title": job_title,
                    "company_name": company_name,
                    "experience": experience,
                    "salary": salary,
                    "location": location,
                    "job_description": job_description,
                    "role": role,
                    "industry_type": industry_type,
                    "department": department,
                    "employment_type": employment_type,
                    "role_category": role_category,
                    "education": education,
                    "key_skills": key_skills,
                    "date_posted": date_posted,
                    "num_openings": num_openings,
                    "num_applicants": num_applicants}
                scrapped_data.append(current_scraped_data)
                time.sleep(2)
                print('-'*50)
                print("Scraped data: ", len(scrapped_data))
                print('-'*50)
        
                with open("naukri_data1.json", "w") as f:
                    json.dump(scrapped_data, f, indent=4)
        return scrapped_data


with ScarpeNaukri(driver_path=r"C:\utils", teardown=False) as bot:
    scrapped_data = bot.scrape()
    with open("naukri_data.json", "w") as f:
        json.dump(scrapped_data, f, indent=4)
