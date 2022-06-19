from datetime import datetime
from operator import getitem
import requests
import urllib.request
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pyautogui
from PIL import Image
import chromedriver_binary  # Adds chromedriver binary to path
import threading
import random
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import selenium.webdriver
import csv

commentlist = ["Nice Post! Seems like you would enjoy @gentlemanboners.daily", "Nice Post! Seems like you would enjoy @gentlemanboners.daily ", "Awesome! consider checking out @gentlemanboners.daily","Great Post! @gentlemanboners.daily", "check out @gentlemanboners.daily", "❤️❤️ @gentlemanboners.daily",  "awesome @gentlemanboners.daily"]

def getTime():
    now = datetime.now()
    timeString = now.strftime("%H:%M:%S")
    return timeString

def runOneAccount(accountname , password, hashtag):
    while True:
        try:

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

            driver = webdriver.Chrome(options=chrome_options)
            actions = ActionChains(driver)


            
            driver.get("https://www.instagram.com")
            time.sleep(7)
            # cookies laden
            if os.path.exists(accountname + '.pkl'):
                cookies = pickle.load(open(accountname +".pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
                time.sleep(5)
            else:
                #login
                s = driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
                s.click()

                time.sleep(6)

                elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
                elem.send_keys(accountname)
                time.sleep(6)
                elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
                elem.send_keys(password)
                # sleep randomly between 10 and 15 seconds
                time.sleep(random.randint(10, 15))

                s = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
                s.click()

                time.sleep(10)
                pickle.dump(driver.get_cookies(), open(accountname + ".pkl", "wb"))
                print("Cookies saved")


  

            # get hashtag page
            time.sleep(10)
            driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
            time.sleep(5)

            #first recent
            s = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
            s.click()
            time.sleep(8)

            #write comment
            inputElement = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/button')
            time.sleep(1)
            inputElement.click()

            randomComment = random.choice(commentlist)
            driver.find_element_by_tag_name('body').send_keys(randomComment)
            print("Commented:", randomComment , "here:" ,  driver.current_url)
            time.sleep(7)

            # press post comment button
            sendButton = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/button')
            sendButton.click()
            time.sleep(5)
            
            
            #loop over x recent posts 
            for i in range(0, 8):
            # next post button
                nextButton = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/button')
                nextButton.click()
                time.sleep(5)
                
                randomComment = random.choice(commentlist)
                #write comment
                inputElement = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/button')
                inputElement.click()
                driver.find_element_by_tag_name('body').send_keys(randomComment)
                time.sleep(7)

                # press post comment button
                sendButton = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/button')
                sendButton.click()
                time.sleep(15)

                print("Commented:", randomComment , "here:" ,  driver.current_url)

           
            driver.quit()
            # sleep a random timne between 3 and 6 hours
            time.sleep(random.randint(1, 2) * 60 * 60) # sleep for 3 to 6 hours

        except Exception as e:
            print(e)
            driver.quit()
            print("sleeping due to exeption")
            time.sleep(random.randint(1, 2) * 60 * 60) # sleep for 3 to 6 hours
            pass


# loop through all rows of csv file accs.csv file and print the first and second column
with open('agednew.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'{row[0]} {row[1]}')
            line_count += 1
            runOneAccount(row[0], row[1], "#erfolg") # evtl ohne das #
            time.sleep(2) # sleep time between accs
    print(f'Processed {line_count} lines.')

