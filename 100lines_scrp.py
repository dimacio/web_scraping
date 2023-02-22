
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

web = "https://twitter.com/i/flow/login"

driver = webdriver.Firefox()
driver.get(web)
driver.maximize_window()

# wait of 6 seconds to let the page load the content
time.sleep(6)  # this time might vary depending on your computer

# locating username and password inputs and sending text to the inputs
# username
username = driver.find_element("xpath",'//input[@autocomplete ="username"]')
username.send_keys("USERNAME")  # Write Email Here
# username.send_keys(os.environ.get("TWITTER_USER"))

# Clicking on "Next" button
next_button = driver.find_element("xpath",'//div[@role="button"]//span[text()="Next"]')
next_button.click()

# wait of 2 seconds after clicking button
time.sleep(2)

# password
password = driver.find_element("xpath",'//input[@autocomplete ="current-password"]')
password.send_keys("PASSWORD")  # Write Password Here
# password.send_keys(os.environ.get("TWITTER_PASS"))

# locating login button and then clicking on it
login_button = driver.find_element("xpath",'//div[@role="button"]//span[text()="Log in"]')
login_button.click()

time.sleep(10) 


web = "https://twitter.com/CFKArgentina/status/1616437338015662084?cxt=HHwWiIDQ4brM3u4sAAAA"
# web = "https://twitter.com/TwitterSupport"
#Initialize the webdriver

driver.get(web)
driver.maximize_window()

def get_tweet(element):
    try:
        user = element.find_element("xpath",".//span[contains(text(), '@')]").text
        text = element.find_element("xpath",".//div[@data-testid='tweetText']").text
        tweet_data = [user, text] 
    except:
        tweet_data = ['user', 'text']
    return tweet_data

user_data = []
text_data = []
tweet_ids = set()
scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']")))
    #print(len(tweets))
    for tweet in tweets:  # you can change this number with the number of tweets in a website || NOTE: ONLY THOSE LOADED IN THE last page will be considered while those from previous page will be forgotten (example: scroll all the way down and then try to find an @username that it's on top --> it won't find it)
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            print(tweet_list)
            user_data.append(tweet_list[0])
            text_data.append(" ".join(tweet_list[1].split()))

    # Get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # condition 1
        if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
            scrolling = False
            break     
        else:
            last_height = new_height
            break
driver.quit()

df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets_pagination.csv', index=False)
print(df_tweets)
