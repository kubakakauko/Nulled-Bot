import time
import argparse
import threading  
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC



parser = argparse.ArgumentParser(description="Nulled.to bot made by Solar enc. ");

parser.add_argument("--tn", default=20, type=int,required=False, help="Number of refreshes before visiting profiles (Default = 20)")
parser.add_argument("--tt", default=20, type=int,required=False, help="Time between tick refresh (Might want to leave this Default = 20)")
parser.add_argument("--mm", required=False, help="Message to be sent into the marketplace | REPLACE SPACES WITH ~ e.g Solar power -> Solar~power | (Leave blank if this feature is to be disabled)")
parser.add_argument("--pv", type=bool, required=False, help="Post viewer (testing)")

args = parser.parse_args()

ticks = args.tn
refresh = args.tt
marketMessage = args.mm

def initialize():
    options = uc.ChromeOptions();
    driver = uc.Chrome(options=options);

    driver.get("https://www.nulled.to/");

    title = driver.title;
    print(title);
        

    print("[!] Waiting for Sign in...");
    WebDriverWait(driver, 200, 1).until(EC.visibility_of_element_located((By.ID, 'user_link')));
    

    name = driver.find_element(By.CSS_SELECTOR, "#user_link > span.hide-mobile");
    print("[*] Welcome %s!" % (name.text));
    return driver;


#Default ticklength is 20s
#Default tickrange is 20
#Total time is 20s * 20 = 7min
def get_members_latest_acticity(driver, tickrange, ticklength):
    print("[!] Gathering user list");
    link = [];
    for x in range(0, tickrange):    
        driver.get("https://www.nulled.to/");
        for member in driver.find_elements(By.CLASS_NAME, "_hovertrigger.url.fn.name"):
            member_link = member.get_attribute('href');
            if member_link != "https://www.nulled.to/user/4668197-jason":
                if member_link not in link:
                    link.append(member_link);
        time.sleep(ticklength);
    
    return link;


def visit_profiles(links, driver):        
    print("[!] Visiting %d profiles" % (len(links)))
    for to_visit in links:
        driver.get(to_visit)
        time.sleep(0.5)
  

#3605 is 60 minutes + 5s for correction. 
def marketplace_messager():
    t = threading.Timer(3605, marketplace_messager)
    t.daemon = True
    t.start()
    
    try:
        print("[!] Sending marketplace message.")
        
        generalButton = WebDriverWait(driver, 3, 1).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div[3]/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]')))
        generalButton.click()
        
        chatbox = WebDriverWait(driver, 2, 1).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div[3]/div[3]/div[1]/div[1]/div[2]/div[2]/div[3]/input[1]')))
        chatbox.click()
        messageFormatted = marketMessage.replace("~", " ")
        chatbox.send_keys(messageFormatted)
        chatbox.send_keys(Keys.ENTER)
    except:
        print("[*] Unable to send marketplace message.")
        return
    

if __name__ == '__main__':                
    driver = initialize()
    
    if(marketMessage):
        marketplace_messager()
    
    while True:
        links = get_members_latest_acticity(driver, ticks, refresh);
        visit_profiles(links, driver);
    