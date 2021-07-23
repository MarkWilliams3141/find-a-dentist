#! /usr/bin/env python3

import tabulate as tabulate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import argparse
import sys

# Application Settings
nhs_website_url = "https://www.nhs.uk/service-search/find-a-dentist"
driver_path = './driver/chromedriver.exe'  # Path to Chrome driver]
delay = 200  # Delay between HTTP requests
headless = True  # Headless browser window


# Print progress bar in terminal
def progress(count, total, suffix=""):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "█" * filled_len + "-" * (bar_len - filled_len)

    sys.stdout.write("[%s] %s%s ...%s\r" % (bar, percents, "%", suffix))
    sys.stdout.flush()


# Setup selenium driver
def get_driver():
    options = Options()
    options.headless = headless
    options.add_argument("--window-size=800,600")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    return browser


# Search NHS dentists by postcode
def dentist_search(postcode):
    browser = get_driver()
    browser.get(nhs_website_url)
    availabilities = []
    try:
        WebDriverWait(browser, delay).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "nhsuk-button")))
        browser.find_element_by_class_name("nhsuk-input").send_keys(postcode)
        browser.find_element_by_class_name("nhsuk-u-margin-bottom-4").click()
        local_dentists_elements = browser.find_elements_by_css_selector(".results__item .results__name a")
        list_of_dentist_urls = [a.get_attribute("href") for a in local_dentists_elements]

        #  If no dentists are found, probably an invalid postcode
        if len(list_of_dentist_urls) == 0:
            print(f"\033[91mPostcode '{postcode}' appears invalid. "
                  f"If the place you searched for is in England, you could: \n"
                  f" * check your spelling and try again\n"
                  f" * try a different postcode\033[0m")
            sys.exit()

        for index, dentist_url in enumerate(list_of_dentist_urls):
            browser.get(dentist_url)
            dentist_name = browser.find_elements_by_css_selector("#page-heading-org-name")
            dentist_status = browser.find_elements_by_css_selector("#dentist_taking_patients_header ~ *")
            availabilities.append({
                "dentist_name": dentist_name[0].text,
                "dentist_status": dentist_status[0].text,
                "dentist_url": dentist_url
            })
            progress(index, len(list_of_dentist_urls), suffix="")

    except TimeoutException:
        print("ERROR: nhs.gov website timed out")
        browser.quit()
        return None

    return availabilities


# Script entrypoint
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logging", help="logging mode, save results", action="store_true")
    parser.add_argument("-s", "--silent", help="hide console output", action="store_true")
    parser.add_argument("-p", "--postcode", help="postcode for search area", action="store")
    args = parser.parse_args()

    if args.postcode:
        postcode_search = args.postcode
    else:
        postcode_search = input("Enter postcode: ")

    print(f"Scanning for NHS dentists near {postcode_search}: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    dentist_availabilities = dentist_search(postcode_search)
    header = dentist_availabilities[0].keys()
    rows = [x.values() for x in dentist_availabilities]

    #  print results in terminal
    if not args.silent:
        print(tabulate.tabulate(rows, header, tablefmt='grid'))

    #  if logging mode enabled save the result
    if args.logging:
        log_path = f"./results/dentist-availability-{postcode_search}.log"
        with open(log_path, 'a') as file:
            print(tabulate.tabulate(rows, header, tablefmt='grid'), file=file)
        print(f"\nSaved result to {log_path}")
