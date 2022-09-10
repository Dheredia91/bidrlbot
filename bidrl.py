
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Get environment variables
LOGIN_USER = os.environ.get("LOGIN_USER")
LOGIN_PW = os.environ.get("LOGIN_PW")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
YOUR_TWILIO_PHONE_NUMBER = os.environ.get("YOUR_TWILIO_PHONE_NUMBER")
TEXT_RECIEVING_NUMBER = os.environ.get("SPECIFIC_NUMBER_TO_SEARCH")

def time_string_to_seconds(time_string):
    total_seconds = 0

    # Split the string into individual components (e.g., "5 Days", "12 Hours", "32 Minutes")
    components = time_string.split(', ')
    for component in components:
        # Extract the value and unit (e.g., "5" and "Days") from each component
        value, unit = component.strip().split(' ')
        value = int(value)

        # Convert each unit to seconds and add to the total_seconds variable
        if unit.lower() == 'days':
            total_seconds += value * 86400
        elif unit.lower() == 'hours':
            total_seconds += value * 3600
        elif unit.lower() == 'minutes':
            total_seconds += value * 60

    return total_seconds

def send_text(message_str):

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
                .create(
                     body = message_str,
                     from_= YOUR_TWILIO_PHONE_NUMBER,
                     to = TEXT_RECIEVING_NUMBER
                 )    
    

def search_and_delete_message():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Retrieve the list of incoming messages from the specified number
    messages = client.messages.list(
        to = YOUR_TWILIO_PHONE_NUMBER,  # Your Twilio phone number
        from_= TEXT_RECIEVING_NUMBER,  # The specific number you want to search for
    )

    if messages:
        # Assuming you want to handle only the latest message
        latest_message = messages[0]

        # Store the body text of the latest message into a variable
        message_body = latest_message.body

        # Delete the message
        latest_message.delete()

        return message_body
    else:
        return None

## get to page
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://bidrl.com/login")
driver.refresh()
time.sleep(2)


## login
username = driver.find_element(By.NAME, "username")
username.click()
username.clear()
username.send_keys(LOGIN_USER)
password = driver.find_element(By.NAME, "password")
password.click()
password.clear()
password.send_keys(LOGIN_PW)
driver.find_element(By.XPATH, "//button[@type='submit']").click()


## navigate to recent bids page
time.sleep(2)
driver.find_element(By.XPATH, "//a[@href='https://www.bidrl.com/myaccount/']").click()
driver.find_element(By.XPATH, "//a[normalize-space()='My Bids']").click()
driver.find_element(By.XPATH, "//a[normalize-space()='hide closed items']").click()

## navigate to auction item
time.sleep(2)

i = 2
while True:
    try:
        # gather variables
        prod = driver.find_element(By.XPATH, f"//tbody/tr[{i}]/td[3]//span").text       
        bid_status = driver.find_element(By.XPATH, f"//tbody/tr[{i}]/td[5]//span").text 

        # item id
        item_id = driver.find_element(By.XPATH, f"//tbody/tr[{i}]/td[2]/a[1]").get_attribute('href').split('-')
        item_id = item_id[-1]

        # if proxy not found, then no proxy bid at present
        try:
            prox = driver.find_element(By.XPATH, f"//tbody/tr[{i}]/td[3]/div[1]/div/label[2]").text
            separator = prox.index(":")
            prox = prox[separator + 1:]
            prox = prox[1:]
            print(prox)
        except NoSuchElementException:
            prox = "no proxy bid"


        # time remaining
        time_left = driver.find_element(By.XPATH, f"//tbody/tr[{i}]/td[7]//span").text
        seconds = time_string_to_seconds(time_left)

        # current highest bid
        cur_bid = driver.find_element(By.XPATH, f"//tbody/tr[{i}]/td[4]//span").text
        cur_bid = cur_bid[1:]

        i += 1

        if bid_status != "winning":

            # Call the function to send the text message
            send_text(f"product: {prod} , current bid: {cur_bid}, time left: {time_left}, to extend reply 'y'.")
            time.sleep(30)

            # Read messages from the specified sender
            message_body = search_and_delete_message()

            start_time = time.time()
            timeout_minutes = 5

            # Check reply for up to 5 minutes 
            while message_body is None:
                time.sleep(1)
                message_body = search_and_delete_message()

                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout_minutes * 60:
                    break  # Exit the loop if five minutes have passed

            # If reply = y then extend the bid
            if message_body == "y" or "Y":
                extend_bid = float(cur_bid) + 3
                proxy_field = driver.find_element(By.ID, f"iitem{item_id}")
                proxy_field.click()
                proxy_field.clear()
                proxy_field.send_keys(str(extend_bid))      


    except NoSuchElementException:
        # NoSuchElementException will be raised when the element is not found, meaning the </tbody> tag is detected
        break


try:
    ## submit any proxy extensions made
    driver.find_element(By.XPATH, "//input[@data-uw-rm-form='submit']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@id='modal']//button[@class='ok']").click()

except NoSuchElementException:
    print("There are no bids at the moment.") 



