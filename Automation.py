import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Path to chromedriver executable
driver_path = r"C:\Users\hp\Desktop\linkden-auto\chromedriver-win64\chromedriver.exe"

# Read the CSV file containing LinkedIn profile URLs
linkedin_df = pd.read_csv("linkedin.csv")  # Modify this to your CSV file path

# Convert the dataframe column 'profile_url' to a list (URLs are in ascending order as in the file)
linkedin_profile_urls = linkedin_df['profile_url'].tolist()

# List of LinkedIn credentials (email, password) to cycle through
linkedin_credentials = [
    ("example@gmail.com", "Password"), 
    # Add more credentials as needed
]

# Set up Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Disable GPU acceleration
# options.add_argument("--headless")  # (optional) Run Chrome in headless mode (no GUI)
options.add_argument("--start-maximized")  # Start in maximized window
options.add_argument("--disable-infobars")  # Disable info bars

# Function to login to LinkedIn with a given account
def login_to_linkedin(username, password):
    driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
    time.sleep(7)  # Wait for 5 seconds for the login page to load
    # Locate the username (email) and password fields using their element IDs
    username_field = driver.find_element(By.ID, "username")  # Find the email input field by its ID
    password_field = driver.find_element(By.ID, "password")  # Find the password input field by its ID
    # Enter the LinkedIn credentials
    username_field.send_keys(username)  # Use provided email
    password_field.send_keys(password)  # Use provided password

    # turn off keep me logged in
    time.sleep(7)
    try:
        # Locate the <label> element associated with the "Remember me" checkbox using the 'for' attribute
        remember_me_label = driver.find_element(By.CSS_SELECTOR, "label[for='rememberMeOptIn-checkbox']")
        
        # Click the label to toggle the checkbox (if unchecked, it will check it, if checked, it will uncheck it)
        remember_me_label.click()
        print("Toggled the 'Keep me logged in' checkbox via label.")
    
    except Exception as e:
        print(f"Error interacting with checkbox label: {e}")
    time.sleep(6)
    #  
    # Submit the form by sending the ENTER key
    password_field.send_keys(Keys.RETURN)  
    time.sleep(random.randint(4,9))  # Wait for login to complete

# Function to logout from LinkedIn
def logout_from_linkedin():
    driver.get("https://www.linkedin.com/m/logout/")  # LinkedIn logout URL
    time.sleep(random.randint(4,9))  # Wait for logout to complete

# Function to send connection request to a profile
def send_connection_request(profile_url):
    driver.get(profile_url)
    time.sleep(random.randint(4,9))  # Wait for the profile page to load

    # # Check if we are still on the profile page by validating the URL
    # if "linkedin.com/in" not in driver.current_url:
    #     print(f"Warning: Redirected from profile page: {profile_url}")
    #     return False  # If redirected away from the profile, return False

    # Find all the 'Connect' buttons on the profile page
    connect_buttons = driver.find_elements(By.CLASS_NAME, "artdeco-button__text")

    # Iterate through each connect button and send a connection request
    for button in connect_buttons:
        try:
            # Click the 'Connect' button
            button.click()
            time.sleep(random.randint(2, 6))  # Wait for the "Add a note" dialog to appear

            # Click the 'Send without a note' button
            # send_without_a_note_button = driver.find_element(By.XPATH, '//button[@aria-label="Send without a note"]')
            # send_without_a_note_button.click()

            # return True  # Return True when a connection request is successfully sent

        except Exception as e:
            print(f"Error: {e}")
            return False  # Return False if an error occurs

# Create a WebDriver instance
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# Initialize counters
connection_counter = 0  # Count the number of connection requests sent
max_connections_per_account = 2  # Number of connections to send before switching accounts

# Start processing the profile URLs
for profile_url in linkedin_profile_urls:
    # Cycle through the list of LinkedIn credentials and log in with a new account each time
    

    # Log in with the selected credentials
    if connection_counter >= max_connections_per_account or connection_counter == 0:
      linkedin_username, linkedin_password = random.choice(linkedin_credentials)
      login_to_linkedin(linkedin_username, linkedin_password)
      time.sleep(5)


    # Send connection requests to the current profile URL
    # send_connection_request(profile_url)
    driver.get(profile_url) 
    time.sleep(6)

    connect_buttons = driver.find_elements(By.CLASS_NAME, "artdeco-button__text")

        # Send a connection request to each person
    for button in connect_buttons:
        try:
                # Click the 'Connect' button
            button.click()
            time.sleep(random.randint(2, 9))
        except Exception as e:
            print(f"Error: {e}")
            continue

    connection_counter += 1
    # Increment the connection counter if the request was successful
    # if connection_sent:
    
    # print(f"Connection request sent to: {profile_url}. Total connections: {connection_counter}")

    # Check if we have reached the max connections for the current account
    if connection_counter >= max_connections_per_account:
        # print(f"Max connections reached for {linkedin_username}. Logging out...")
        logout_from_linkedin()  # Log out after sending max connections
        time.sleep(3)  # Wait for the logout to complete
        connection_counter = 0  # Reset the connection counter

# Quit the driver after completing the tasks
driver.quit()
