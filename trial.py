import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pathlib



def login(driver):
    # driver.implicitly_wait(10)
    driver.get("http://eclasses.ravindrababuravula.com/login/index.php")
    username = driver.find_element_by_xpath("//input[@id='username']")
    username.send_keys("username")
    password = driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys("password")
    logIn = driver.find_element_by_xpath("//button[@id='loginbtn']")
    logIn.click()


def subjectFolders(driver,path):
    d = dict()
    wait = WebDriverWait(driver, 15)
    try:
        i=1
        while(i):
            link = "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/aside[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div["+str(i)+"]"
            subName = wait.until(
                EC.presence_of_element_located((By.XPATH,link+"/div[1]/div[1]/a[1]/span[4]"))
            )
            sublink = wait.until(
                EC.presence_of_element_located((By.XPATH,link+"/a[1]"))
            )
            
            folderName = str(i)+"-"+subName.text
            folderName = "".join(folderName.split())
            d[folderName] = str(sublink.get_attribute("href"))

            directory = os.path.join(path,folderName)
            if not os.path.exists(directory):
                os.makedirs(directory)
            i+=1
    except Exception as e:
        pass
    finally:
        return d


def chapterFolders(driver,path,subjectLink):
    driver.get(subjectLink)
    d = dict()
    link = 0
    wait = WebDriverWait(driver,1)
    for i in range(1,len(driver.find_elements_by_tag_name("li"))):
        try:
            link = wait.until(
                EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/ul[1]/li["+str(i)+"]/div[3]/h3[1]/a[1]"))
            )
            folderName = str(i)+"-"+link.text
            folderName = "".join(folderName.split())
            d[folderName] = link.get_attribute("href")
            directory = os.path.join(path,folderName)
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            pass 
    return d


    

def download(driver):
    pass
    # wait = WebDriverWait(driver, 10)
    # driver.get("http://eclasses.ravindrababuravula.com/mod/page/view.php?id=2287")

    # iframe = wait.until(lambda driver: driver.find_element(By.TAG_NAME, "iframe"))
    # driver.switch_to.frame(iframe)
    
    # try:
    #     wait.until(
    #         EC.presence_of_element_located((By.XPATH,"//button[@class='ext_dl-button rounded-box']"))
    #     ).click()
    #     link = wait.until(
    #         EC.presence_of_element_located((By.XPATH,"//a[4]"))
    #     )
    #     urllib.request.urlretrieve(link.get_attribute("href"),link.get_attribute("download"))
    #     print(link.get_attribute("download"))
    
    # except Exception as e:
    #     print("exception block ",e)
    
    # finally:
    #     driver.quit()




if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_extension('extension.crx')
    with webdriver.Chrome(chrome_options=options) as driver:

        login(driver)

        ###############################################
        ## To Delete Other
        window1 = driver.current_window_handle
        for handle in driver.window_handles:
            if(handle!=window1):
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(window1)
        ###############################################
        
        path = os.path.join(os.getcwd(),"download")
        
        subjectLinks = subjectFolders(driver,path)

        # for k in subjectLinks:
        #     chapters = chapterFolders(driver,os.path.join(path,k),subjectLinks[k])
        
        k = list(subjectLinks.keys())[0]
        chapters = chapterFolders(driver,os.path.join(path,k),subjectLinks[k])

        driver.quit()
        
        
