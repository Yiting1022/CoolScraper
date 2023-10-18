import re
import os
import threading
from selenium import webdriver
import json
import argparse


if __name__ == "__main__":
    base_url = "https://cool.ntu.edu.tw/courses/"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    lock = threading.Lock()


    parser = argparse.ArgumentParser(description='Web scraper for cool.ntu.edu.tw/courses/')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--cookie', action='store_true', help='Use cookie for authentication')
    parser.add_argument('--counts', type=int, default=25, help='Number of threads for multi-threading')
    args = parser.parse_args()

    VERBOSE = args.verbose
    def vprint(*args, **kwargs):
        if VERBOSE:
            print(*args, **kwargs)
    cookies = None

    if args.cookie:
        try:
            with open("cookie.json", "r") as file:
                cookies = json.load(file)
        except:
            cookies = None
            
    num_threads = args.counts

def set_cookies(driver):
    if not cookies:  
        return

    driver.get(base_url)
    for cookie in cookies:
        cookie_dict = {
            'name': cookie['name'],
            'value': cookie['value'],
            'path': cookie['path'],
            'domain': cookie['domain'],
            'secure': cookie['secure'],
            'id': cookie['id'],
        }
        if "expirationDate" in cookie:
            expiry_value = cookie["expirationDate"]
            cookie_dict['expiry'] = int(expiry_value)
        try:
            driver.add_cookie(cookie_dict)
        except Exception as e:
            vprint(f"Failed to add cookie {cookie['name']} due to {e}")

def fetch_courses(start, end):
    driver = webdriver.Chrome(options=options)
    set_cookies(driver)  
    with open(f"output_{start}_{end}.txt", "w") as output_file:
        for i in range(start, end):
            vprint(f"Fetching {i}")
            url = base_url + str(i)
            driver.get(url)
            driver.implicitly_wait(1)

            page_source = driver.page_source
            pattern = r'"COURSE":\{"id":"(\d+)","long_name":"([^"]+)"'
            pattern1 = r'<h2 class="pull-left">(.*?)</h2>'
            matches = re.findall(pattern, page_source)
            matches1 = re.findall(pattern1, page_source)

            for match in matches:
                course_id = match[0]
                course_name = match[1].split(" - ")[0]   
            if len(matches) == 0:
                for match in matches1:
                    course_name = match
                    course_id = i
            if len(matches) == 0 and len(matches1) == 0:
                continue
            print(f"{course_id}: {course_name}")
            with lock:
                write_str = f"{course_id}: {course_name}\n"
                output_file.write(write_str)
                    
    driver.quit()





thread_list = []

chunk_size = (35000 - 0) // num_threads
for i in range(num_threads):
    start = 0 + i * chunk_size
    end = start + chunk_size
    thread = threading.Thread(target=fetch_courses, args=(start, end))
    thread_list.append(thread)
    thread.start()

for t in thread_list:
    t.join()
 
with open("final_output.txt", "w") as final_file:
    for i in range(num_threads):
        start = 0 + i * chunk_size  
        end = start + chunk_size
        output_file_name = f"output_{start}_{end}.txt"
        with open(output_file_name, "r") as temp_file:
            final_file.write(temp_file.read())
        os.remove(output_file_name)
