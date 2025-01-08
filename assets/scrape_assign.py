
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from filewriter_assign import FileWriterTool
import time
import re


file_writer_tool = FileWriterTool()
# Initialization of chrome driver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")


class Assign:

    def task_scrape(self):
        search_website = "finviz.com"  #by core, we are using finviz website only. This code version is compatible for this website as an assignment part.
        with open('company_info.txt', 'r') as file:
            content = file.read()  

        pattern = r"Company name:\s*([A-Za-z0-9]+),"    # extracting company name value from .txt file

        company = re.findall(pattern, content)
        company=company[0]  #handling list and hash errors during processing

        if company:
            print(f"company name found: {company}")
        else:
            print("No company names found. Default taken is NFLX")
            company="NFLX"  # by default it will take netflix as processing section in case of no company name.
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        print(f"Processing query: {search_website}")

        search_url = f"https://www.google.com/search?q={search_website}"  #searching on google
        driver.get(search_url)
        time.sleep(2)  # Wait for the page to load

        try:
            # Wait for search results to load
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#search div.g')))
            elements = driver.find_elements(By.CSS_SELECTOR, 'div#search div.g a')
            screenshot=1
            driver.save_screenshot("scrn"+str(screenshot)+".png")  #saving the screenshot
            # Get the first link for searched query on google
            links = [element.get_attribute('href') for element in elements[0:1]]
            for link in links:
                print(f"Scraping initiated:")
                driver.get(link)
                time.sleep(2)  # Wait for the page to load
                screenshot=screenshot+1  # incrementing the screenshot counter
                driver.save_screenshot("scrn"+str(screenshot)+".png")
                ## searching for the "search" by ID. So to enter "company name".
                search_bar_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "search"))
                )

                # Locate the input field within the search bar container
                search_bar_input = search_bar_container.find_element(By.TAG_NAME, "input")

                # Send keys to the input field
                search_bar_input.send_keys({company})
                search_bar_input.send_keys(Keys.RETURN)
                time.sleep(2)
                screenshot=screenshot+1 # incrementing the screenshot counter
                driver.save_screenshot("scrn"+str(screenshot)+".png")
                main_content = driver.find_element(By.TAG_NAME, "body").text
                main_content = re.sub(r'\s+', ' ', main_content)  # Cleaning up content to be passed to an agent

                # Go back to search results
                driver.back()
                time.sleep(2)  # Wait for the search results to load again
                # it will handle several handshaking errors, but wil not in case of captchas and hyper security by the browser.
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#search div.g')))

        except Exception as e:
            print(f"Error: {e}")

        driver.quit()
        print(type(main_content))
        print(main_content)  # to lookout on the console screen

        args = {
        "filename": "example.md",
        "content": main_content,
        "directory": ".",  # Specify the directory (optional)
        "overwrite": "True"  # Set overwrite to True (allow overwriting the file)
        }
        result = file_writer_tool._run(**args)  #writing to .md file
        print("result:____",result)
        return "done execution of scraping and web browser section"
