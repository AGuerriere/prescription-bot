'''This is a program to order my prescriptions online from my GP'''

#The os module is needed to say it's done in the end
import os
import sys
# Config is a module I created to store the GP Url and credentials
import config
import chromedriver_auto_update
import datetime # Datetime module needed to log the time and date of the last order in the log.txt file

import tkinter as tk
# since tkinter won't let you change background color when clicking button, 
# we can use ttk, however even that is not perfect, and tkmacosx would be better but unnecessary in this case
from tkinter import ttk


# # update to the latest chromedriver
print('updating homebrew' + '🍺')
os.system('brew update')
os.system('brew upgrade chromedriver')


from selenium import webdriver
#the following import allows the program to send text to the browser including enter.
from selenium.webdriver.common.keys import Keys
#this is needed for waiting for the page to fully load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def order_prescriptions():
    #now we tell python where to find chromedriver on the computer
    driver = webdriver.Chrome(chromedriver_auto_update.PATH)

    #This opens the target website
    driver.get(config.target_website)
    #This finds the entrybox where we want to enter the login username
    search = driver.find_element_by_name('ctl00$ContentPlaceHolder1$logon_email')
    search.send_keys(config.user)
    #This finds the entrybox where we want to enter the login password
    search = driver.find_element_by_name('ctl00$ContentPlaceHolder1$logon_password')
    search.send_keys(config.password)
    #press enter
    search.send_keys(Keys.RETURN)

    #click on next page - We use try and except to wait for 5 seconds, in case the page doesn't load in time for the click
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_TabContainer1_Panel1 > div:nth-child(1) > div > input"))
        )
        element.click()
    except:
        driver.quit()

    #click on next page again
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_TabContainer1_Panel2 > div > div > input:nth-child(1)"))
        )
        element.click()
    except:
        driver.quit()

    #This clicks or 'request email confirmation'
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_TabContainer1_Panel3_confirmation"))
        )
        element.click()
    except:
        driver.quit()

    #This is the final confirmation click - If you don't want to actually send the request, comment it out
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_TabContainer1_Panel3_buttonSend"))
        )
        element.click()

        # This logs the last time I ordered my prescriptions only when I actually order them
        date = datetime.datetime.now()
        log_date = open('log.txt', "a")
        # The %x below is used to use the local date format and the %X is used to add local time format see here for more formats: https://www.w3schools.com/python/python_datetime.asp
        log_date.write(f"{date.strftime('%x')} - {date.strftime('%X')}\n")
        log_date.close()

    except:
        driver.quit()


    #This says out loud "it's done"
    os.system('say It is done')
    #This exits the program at the end. Comment it out if you want to stay on the last page before leaving.
    sys.exit()

root = tk.Tk()
root.title('Prescription Bot')
root.configure(background='white')
#root.bind("<FocusIn>")


btn1 = ttk.Button(root, text='Yes', command=order_prescriptions)
btn2 = ttk.Button(root, text='Exit',command=sys.exit)

lbl = ttk.Label(root, text='Are you sure you want to proceed?')

lbl.grid(row=0, column=0, padx=100, pady=10)
btn1.grid(row=1, column=0, padx=40, pady=10)
btn2.grid(row=2, column=0, padx=40, pady=10)

root.mainloop()

