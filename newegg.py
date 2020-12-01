import asyncio
import sys
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from arsenic import get_session
from arsenic.browsers import Firefox
from arsenic.services import Geckodriver

driver = webdriver.Firefox()

myEmail = '' # newegg email
myPass = '' # newegg password

currNumAddToCarts = 3

# test URL - pair of super mario socks
# URL = "https://www.newegg.com/p/1JZ-02P3-00012?Item=9SIAPSJBSU5996&Description=headband&cm_re=headband-_-9SIAPSJBSU5996-_-Product&quicklink=true"

# rx 6800 xt link
URL = "https://www.newegg.com/msi-radeon-rx-6800-xt-rx-6800-xt-16g/p/N82E16814137607?Description=6800%20xt&cm_re=6800_xt-_-14-137-607-_-Product&quicklink=true"

# scrolls down and clicks 'continue to payment' button
# async def scrollAndClick(className):
#     async with get_session(Geckodriver(), Firefox()) as session:
#         await driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#         continueToPayment = driver.find_element_by_class_name(className)
#         continueToPayment.click()

# logs in to your newegg account
def logIn():
    time.sleep(1)
    emailAddress = driver.find_element_by_id('labeled-input-signEmail')
    emailAddress.send_keys(myEmail)
    signInButton = driver.find_element_by_id('signInSubmit')
    signInButton.click()
    time.sleep(2)
    password = driver.find_element_by_id('labeled-input-password')
    password.send_keys(myPass)
    signInButton = driver.find_element_by_id('signInSubmit')
    signInButton.click()

# clicks the 'checkout' button
def clickCheckout():
    continueToPayment = driver.find_element_by_class_name('checkout-step-action-done')
    continueToPayment.click()

# main function that refreshes indefinitely until an item is in stock, then tries to place your order.
def autoBuy():
    print('Auto Buyer program started...')
    driver.get("https://www.newegg.com/")
    time.sleep(2)

    # clicks the sign in button on the newegg.com home page in the navigation bar
    signInLink = driver.find_element_by_class_name("nav-complex-title")
    signInLink.click()
    logIn()
    # driver.get("https://www.newegg.com/")
    driver.get(URL)

    foundButton = False

    numAttempts = 1

    while not foundButton:
        numAddToCarts = 0
        # driver.find_element_by_class_name("btn-wide")
        # driver.find_element_by_xpath("//button['Add to Cart']")
        addToCartButtonRef = driver.find_elements_by_xpath("//button['Add to Cart']")
        for item in addToCartButtonRef:
            if (item.get_attribute('innerHTML') == 'Add to cart <i class="fas fa-caret-right"></i>'):
                numAddToCarts = numAddToCarts + 1
            # print(item.get_attribute('innerHTML'))
        soldOutRef = driver.find_element_by_xpath("//button['Sold Out']")
        addToCartButton = addButton = addToCartButtonRef
        # print("driver element find: ", addToCartButton)
        # print(addToCartButton.get_attribute('innerHTML'))
        # if addButton == 0 or len(addButton) == 0:
        print("numAddToCarts: ", numAddToCarts)
        if numAddToCarts < currNumAddToCarts:
            # delay or wait some time between tries
            time.sleep(3)  # wait 3 seconds

            # refresh the page
            print("Couldn't add to cart! Refreshing page... (Attempt #", numAttempts, ")")
            numAttempts = numAttempts + 1
            driver.refresh()

            # then go back to look for button again
            addToCartButton = addButton = addToCartButtonRef
        else:
            foundButton = True

    # close any pop-up that obstructs the bot from clicking the 'add to cart' button
    popupDialog = driver.find_element_by_id('popup-wrapper')
    if popupDialog != 0:
        print('closing popup!')
        popupDialog.close()

    # adding the item to the cart
    # print(addToCartButton)
    addToCartButton = driver.find_element_by_class_name("btn-wide")
    print("Adding to cart!")
    addToCartButton.click()

    # navigate to your cart
    driver.get("https://secure.newegg.com/shop/cart")

    # click 'Secure Checkout' button
    addToCartButton = driver.find_element_by_class_name("btn-wide")
    addToCartButton.click()
    time.sleep(1)
    print('signing in!')
    logIn()
    time.sleep(2)

    # scroll down the page and click the 'continue to payment button' - still have scrollable view issues
    try:
        # # WebDriverWait(driver, 60).until(driver.execute_script("window.scrollTo(0,document.body.scrollHeight)"))
        #
        # continueToPayment = driver.find_element_by_class_name('checkout-step-action-done')
        # print("find this button: ", continueToPayment)
        # ActionChains(driver).move_to_element(continueToPayment).click(continueToPayment).perform()
        # # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'checkout-step-action-done'))).click()
        #
        # continueToPayment.click()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        clickCheckout()
        # scrollAndClick('checkout-step-action-done')

    except:
        print("Unable to checkout:", sys.exc_info()[0])
        # driver.close()

    print('AutoBuyer program terminated')


def main(run):
    try:
        print('Starting autobuy run#', run)
        autoBuy()
    except:
        print("Run# ", run, " failed:", sys.exc_info()[0])
        run = run + 1
        main(run)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(autoBuy())
    # loop.close()

if __name__ == '__main__':
    run = 1
    main(run)