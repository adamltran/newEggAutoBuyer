import sys
import time
import tkinter

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotInteractableException

from selenium.webdriver.support.ui import WebDriverWait

import json
from tkinter import *

# load credentials file
with open('account.json') as f:
  account = json.load(f)

# credentials
myEmail = account['email']
myPass = account['password']
cvvNum = account['cvv']
refreshSlow = int(account['refreshSlow'])
refreshFast = int(account['refreshFast'])

low = 2
high = 3

cardPurchased = False
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()

def getRandomInt(low, high):
    return random.uniform(low, high)

def sleepRandTime():
    return time.sleep(getRandomInt(low, high))

def refreshRandTime():
    return random.uniform(refreshSlow, refreshFast)

currNumAddToCarts = 0
numAttempts = 1
# test URL - pair of super mario socks
# URL = "https://www.newegg.com/p/1JZ-02P3-00012?Item=9SIAPSJBSU5996&Description=headband&cm_re=headband-_-9SIAPSJBSU5996-_-Product&quicklink=true"

# test URL - bubble tea straws
# URL = "https://www.newegg.com/p/0EC-01A3-00007?Description=bubble%20tea%20straws&cm_re=bubble_tea%20straws-_-9SIAPSCBXY9433-_-Product&quicklink=true"

# rx 6800 xt link
# URL = "https://www.newegg.com/msi-radeon-rx-6800-xt-rx-6800-xt-16g/p/N82E16814137607?Description=6800%20xt&cm_re=6800_xt-_-14-137-607-_-Product&quicklink=true"

# rtx 3080 link
# URL = "https://www.newegg.com/asus-geforce-rtx-3080-rog-strix-rtx3080-o10g-gaming/p/N82E16814126457?Description=3080&cm_re=3080-_-14-126-457-_-Product&quicklink=true"
URL = "https://www.newegg.com/asus-geforce-rtx-3080-rog-strix-rtx3080-o10g-gaming/p/N82E16814126457?Description=asus%203080&cm_re=asus_3080-_-14-126-457-_-Product"

# URL = "https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518?Description=3080&cm_re=3080-_-14-487-518-_-Product"
# URL = "https://www.newegg.com/xfx-radeon-rx-6800-rx-68xlatbd9/p/N82E16814150845?Description=6800%20speedster&cm_re=6800_speedster-_-14-150-845-_-Product&quicklink=true"
# URL = "https://www.newegg.com/asus-geforce-rtx-3080-rog-strix-rtx3080-o10g-gaming/p/N82E16814126457?Description=3080&cm_re=3080-_-14-126-457-_-Product&quicklink=true"
# URL = "https://www.newegg.com/xfx-radeon-rx-6800-xt-rx-68xtacbd9/p/N82E16814150844"

def closePopup():
    global driver
    try:
        # print('running popup check...')
        driver.find_element_by_id('popup-close').click()
        print('closing home page popup!')
    except NoSuchElementException:
        # print('no home page popup found...')
        pass
def closeCartPopup():
    try:
        # print('running popup check...')
        driver.find_element_by_class_name('close').click()
        print('closing cart popup!')
    except NoSuchElementException:
        # print('no cart popup found...')
        pass
# logs in to your newegg account
def login(paying):
    global driver, delay
    time.sleep(.5)
    print('logging in...')
    emailAddress = driver.find_element_by_id('labeled-input-signEmail')
    emailAddress.send_keys(myEmail)
    if paying == False:
        sleepRandTime()

    try:
        driver.find_element_by_id('signInSubmit').click()
        try:
            driver.find_element_by_class_name('recaptcha-checkbox-border').click()
        except:
            print('no captcha detected')

        # sleepRandTime()
        # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'labeled-input-password')))
        password = driver.find_element_by_id('labeled-input-password')
        password.send_keys(myPass)
        # sleepRandTime()
        # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'signInSubmit')))
        signInButton = driver.find_element_by_id('signInSubmit')
        signInButton.click()
    except:
        try:
            driver.find_element_by_id('signInSubmit').click()
            time.sleep(.5)
            password = driver.find_element_by_id('labeled-input-password')
            password.send_keys(myPass)
            signInButton = driver.find_element_by_id('signInSubmit')
            signInButton.click()
        except:
            print('Could not submit username or got stuck on CAPTCHA: ', sys.exc_info()[0])

# clicks the 'checkout' button
def clickCheckout():
    global driver
    continueToPayment = driver.find_element_by_class_name('checkout-step-action-done')
    continueToPayment.click()

def loadHome():
    global driver
    # print('loading new egg home page...')
    # driver.get('https://whatismyipaddress.com/')
    driver.get("https://www.newegg.com/")
    # WebDriverWait(driver, 10)
    time.sleep(5)
    # sleepRandTime()
    closePopup()

def signInFromHome():
    try:
        signInLink = driver.find_element_by_class_name("nav-complex-title")
        print('clicking sign in link...')
        signInLink.click()
    except:
        print('Encountered error signing in on home page: ', sys.exc_info()[0])

def loadItem():
    try:
        driver.get(URL)
        WebDriverWait(driver, 2)
        closePopup()
    except:
        print('Could not render item page : ', sys.exc_info()[0])


def addToCart():
    global numAttempts
    foundButton = False

    while not foundButton:
        numAddToCarts = 0
        # driver.find_element_by_class_name("btn-wide")
        # driver.find_element_by_xpath("//button['Add to Cart']")
        closePopup()
        try:
            # WebDriverWait(driver, 5)
            addToCartButtonRef = driver.find_elements_by_xpath("//button['Add to Cart']")
            # print('found the add to cart button...')
            for item in addToCartButtonRef:
                if (item.get_attribute('innerHTML') == 'Add to cart <i class="fas fa-caret-right"></i>'):
                    numAddToCarts = numAddToCarts + 1
            addToCartButton = addButton = addToCartButtonRef
            # print("numAddToCarts: ", numAddToCarts)
            if numAddToCarts < currNumAddToCarts:
                # delay or wait some time between tries
                # time.sleep(3)  # wait 3 seconds

                # refresh the page
                print("Couldn't add to cart! Refreshing page... (Attempt #", numAttempts, ")")
                numAttempts = numAttempts + 1
                driver.refresh()

                # then go back to look for button again
                addToCartButton = addButton = addToCartButtonRef
            else:
                # print('Found the button!')
                foundButton = True
                break;
        except:
            print('Encountered error: ', sys.exc_info())
    # closePopup()
    try:
        print('Attempting to add the item to the cart!')
        driver.find_element_by_xpath('//*[@id="ProductBuy"]/div/div[2]/button').click()
        goToCart()
    except ElementNotInteractableException:
        print('Something popped up and blocked adding the item to the cart : ', sys.exc_info())
    except:
        print('Encountered error adding item to cart: ', sys.exc_info())

def goToCart():
    driver.get("https://secure.newegg.com/shop/cart")
    time.sleep(1)
    closeCartPopup()

def secureCheckout():
    driver.find_element_by_class_name("btn-wide").click()

def continueToPayment():
    print('continuing to payment...')
    try:

        print('locating payment button...')
        payButton = driver.find_element_by_class_name('checkout-step-action-done')
        print(payButton)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            time.sleep(.5)
            print('trying to click payment button')

            driver.find_element_by_xpath("/html/body/div[6]/div/section/div/div/form/div[2]/div[1]/div[2]/div[2]/div/div[3]/button").click()
        except:
            print('found but could not click payment button: ', sys.exc_info())
    except:
        print('Could not find payment button at all: ', sys.exc_info())
# /html/body/div[6]/div/section/div/div/form/div[2]/div[1]/div[2]/div[2]/div/div[3]/button xpath of continue to payment button

def reviewOrder():
    print('reviewing order...')
    try:
        time.sleep(2)
        print('locating review order button...')
        payButton = driver.find_element_by_class_name('checkout-step-action-done')
        print(payButton)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            time.sleep(.5)
            print('entering CVV')
            cvvBox = driver.find_element_by_class_name('mask-cvv-4')
            print('entering this cvv: ', cvvNum)
            cvvBox.click()
            cvvBox.send_keys(cvvNum)
            print('trying to click review order button')
            driver.find_element_by_xpath("/html/body/div[6]/div/section/div/div/form/div[2]/div[1]/div[2]/div[3]/div/div[3]/button").click()
        except:
            print('found but could not click review order button: ', sys.exc_info())
    except:
        print('Could not find review order button at all: ', sys.exc_info())

def placeOrder():
    global cardPurchased

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        placeOrderButton = driver.find_element_by_id('btnCreditCard')
        print('Found the place order button: ', placeOrderButton)
        placeOrderButton.click()
        print('Successfully placed your order!')
        cardPurchased = True
    except:
        print('Ran into an error clicking the place order button: ', sys.exc_info())

def loopReviewOrder():
    try:
        reviewOrder()
    except:
        loopReviewOrder()

def loopPlaceOrder():
    try:
        placeOrder()
    except:
        loopPlaceOrder()

def keepAdding():
    global run, driver, cardPurchased

    while not cardPurchased:
        # loadItem()
        addToCart()
        try:
            secureCheckout()
            login(True)
            continueToPayment()
            loopReviewOrder()
            loopPlaceOrder()
        except:
            waitMe = refreshRandTime()
            print('Waiting for '+str(waitMe)+' seconds before refreshing again...')
            time.sleep(waitMe)
            print("Starting Run# ", run)
            run = run + 1
            driver.refresh()

# main function that refreshes indefinitely until an item is in stock, then tries to place your order.
def autoBuy():
    global driver
    print('Auto Buyer program started...')
    driver.maximize_window()
    loadHome()
    # signInFromHome()
    # login(False)
    time.sleep(5)
    loadItem()
    keepAdding()

    print('AutoBuyer program terminated')

def main():
    global run, driver

    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome()
        autoBuy()
    except WebDriverException:
        print("Run# ", run, " failed:", sys.exc_info())
        run = run + 1
        print('Something went wrong attempting to connect to the web page: ', sys.exc_info())
        driver.quit()
        print('Restarting...')
        main()
    except ElementNotInteractableException:
        print('Something popped up and blocked the screen : ', sys.exc_info())
    except:
        print("Run# ", run, " failed:", sys.exc_info())
        run = run + 1
        time.sleep(5)
        driver.quit()

# def click():
#     print('button clicked')
#     main()

# def close_window():
#     global driver
#     window.destroy()
#     driver.quit()
#     exit()

if __name__ == '__main__':
    run = 1
    # window = Tk()
    # window.title("Newegg Autobuying Bot")
    # window.configure(background="black")
    # Label (window, text="Enter your newegg email:", bg="black", fg="white", font="none 12 bold") .grid(row=1, column=0, sticky=W)
    # textEntry = Entry(window, width=20, bg="white")
    # textEntry.grid(row=2, column=0, sticky=W)
    # Button(window, text="START BOT", width=11, command=click) .grid(row=3, column=0, sticky=W)
    # output = Text(window, width=75, height=6, wrap=WORD, background="white")
    # output.grid(row=5, column=0, columnspan=2, sticky=W)
    # Button(window, text="EXIT", width=11, command=close_window).grid(row=3, column=0, sticky=E)
    # window.mainloop()
    main()