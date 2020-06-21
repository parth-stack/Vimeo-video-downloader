import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def login(driver):
    # driver.implicitly_wait(10)
    driver.get("http://eclasses.ravindrababuravula.com/login/index.php")
    username = driver.find_element_by_xpath("//input[@id='username']")
    username.send_keys("username")
    password = driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys("password")
    logIn = driver.find_element_by_xpath("//button[@id='loginbtn']")
    logIn.click()


def download(link):
    downloadName = link.get_attribute("download")
    downloadLink = link.get_attribute("href")
    fileName = "C:/Users/PRI/Desktop/rvr/"+ downloadName
    print(downloadName)
    urllib.request.urlretrieve(downloadLink,fileName)
def snatchVideoLink(driver):
    wait = WebDriverWait(driver,50)
    # switching to iframe
    try:
        iframe = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        # find video link
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH,"//button[@class='ext_dl-button rounded-box']"))
            ).click()      
            link = wait.until(
                EC.presence_of_element_located((By.XPATH,"//a[4]"))
            )
            download(link)
        except Exception as e:
            print("\n exception in snatchVideoLink (link problem) \n",e)
        finally:
            driver.switch_to.default_content()
    except Exception as e:
        print("\n exception in snatchVideoLink (iframe problem) \n",e)
    
def landingPage(driver,link):
    driver.get(link)
    print(link)
    window = driver.current_window_handle
    wait = WebDriverWait(driver,50)
    nextLink = None
    try:
        snatchVideoLink(driver)
        nextLink = wait.until(
            EC.presence_of_element_located((By.ID,"next-activity-link"))
        )
        landingPage(driver,nextLink.get_attribute("href"))
    except Exception as e:
        print("\n exception in landingPage \n ",e)





if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_extension('extension.crx')
    driver_path = 'chromedriver.exe'
    with webdriver.Chrome(executable_path=driver_path,chrome_options=options) as driver:
        # Login
        login(driver)
        
        # To Delete Other Tabs
        window1 = driver.current_window_handle
        for handle in driver.window_handles:
            if(handle!=window1):
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(window1)
        
        #
        print("Enter the Landing Page :: ",end="")
        link = str(input())
        landingPage(driver,link)
        
        # quit all processes
        driver.quit()
