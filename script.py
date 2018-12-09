from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
import time
import random
import sys

#config
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium"
if sys.platform.startswith('win'):
    driver = webdriver.Chrome("windows_chrome_driver/chromedriver.exe")
elif sys.platform.startswith('linux'):
    driver = webdriver.Chrome("linux_chrome_driver/chromedriver")
elif sys.platform.startswith('darwin'):
    driver = webdriver.Chrome("macos_chrome_driver/chromedriver")
else:
    print('System not supportet by webdriver')

driver.maximize_window()
driver.implicitly_wait(15)
emailLogin = 'your@mail.com' 
password = 's3cr3tP@ssword!'
adressPage = 'https://promocje.woah.com/'
fileNameWithPromotionCodes = "promotion_codes.txt"
separatorForSplittingPromotionCodes = '...'
fileLogs = "logs.txt"
randomSecondToAddCodeFrom = 5
randomSecondToAddCodeTo = 8
numberCode = 0
wait = WebDriverWait(driver, 10)

#go to site and check url
driver.get(adressPage)
time.sleep(2)
url = driver.current_url
if 'https://promocje.woah.com/' in url:
    print('The page opened https://promocje.woah.com/.')
else:
    print('The website address is not valid.')

 
#close cookies alert
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.optanon-alert-box-wrapper > div.optanon-alert-box-bottom-top > div > a'))).click()
time.sleep(2.5)  

#login to page
try:
    driver.find_element_by_xpath('//*[@id="capture_signin_link"]').click()
    driver.find_element_by_id('capture_signIn_traditionalSignIn_emailAddress').send_keys(emailLogin)
    driver.find_element_by_id('capture_signIn_traditionalSignIn_password').send_keys(password)
    driver.find_element_by_id('capture_signIn_traditionalSignIn_signInButton').click()

#input promotion code to field from file and confirm 
    print('Script working...')
    file = open(fileNameWithPromotionCodes, "r")
    logs = open(fileLogs, "a")
    dateAndTime = datetime.datetime.now()
    logs.write("\n\n------------------------------ Logs of {} ------------------------------".format(str(dateAndTime)) + "\n\n")

    if len(separatorForSplittingPromotionCodes) > 0:
        allPromotionCodes = file.read().replace('\n', '').split(separatorForSplittingPromotionCodes)
    else:
        allPromotionCodes = file.read().split()
    numberOfCodes = len(allPromotionCodes)
    #open poup to send promotion code
    driver.find_element_by_class_name('js-dodaj-nowy-kod').click()

    #add promotion codes with logs
    for promotionCode in allPromotionCodes:
        numberCode += 1
        sizeCode = len(promotionCode)
        dateAndTime = datetime.datetime.now()
        if sizeCode != 12:
            print(('{} ###### The code {} does not have the required 12 characters! Current size: {}\n').format(dateAndTime, promotionCode, str(sizeCode)))
            logs.write(('{} ###### The code {} does not have the required 12 characters! Current size: {}\n').format(dateAndTime, promotionCode, str(sizeCode)))
            continue
        if not promotionCode.isalnum():
            print(('{} ###### The code {} contains characters other than alphanumeric! Code ommited.\n').format(dateAndTime, promotionCode))
            logs.write(('{} ###### The code {} contains characters other than alphanumeric! Code ommited.\n').format(dateAndTime, promotionCode))
            continue 
        randomSecondsPause = round(random.uniform(randomSecondToAddCodeFrom, randomSecondToAddCodeTo), 2)
        logs.write(('{} ###### Adding promotion code numer {} from {} : {}\n').format(str(dateAndTime), str(numberCode), numberOfCodes, promotionCode))
        print(('{} ###### Adding promotion code numer {} from {} : {}\n').format(str(dateAndTime), str(numberCode), numberOfCodes, promotionCode))
        inputField = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'form-control')))
        inputField.clear()
        inputField.send_keys(promotionCode)
        inputField.send_keys(Keys.ENTER)
        logs.write('Waiting for {} seconds\n'.format(randomSecondsPause))
        print('Waiting for {} seconds\n'.format(randomSecondsPause))
        time.sleep(randomSecondsPause)
        popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'o-container')))
        message = popup.text
        if 'Kod dodano prawidłowo.' in message:
            numberOfPoints = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#popupbox > div > div > p:nth-child(3) > strong')))
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#popupbox > div > div > a'))).click()
            logs.write(('Promotional code added correctly. You currently have {} points.\n').format(numberOfPoints.text)) #.text
            print(('Promotional code added correctly. You currently have {} points.\n').format(numberOfPoints.text))
        else:
            driver.save_screenshot(("./screenshots/{}_screenshot.png").format(promotionCode))
            logs.write('The code could not be added. Saved screen shot.\n')
            print('The code could not be added. Saved screen shot.\n')
        if 'KONTO CZASOWO ZABLOKOWANE.' in message:
            print('Blocked account. I interrupt the script. Saved screen shot.\n')
            logs.print('Blocked account. I interrupt the script. Saved screen shot.\n')
            break
except Exception as e:
    print('Script stopped\nError: Incorrect login or blocked account or ' + str(e))
    logs.write('Script stopped\nError: Incorrect login or blocked account or ' + str(e))

logs.write('\nScript stopped\n')

file.close()
logs.close()

print(' Script stopped')

driver.quit()
