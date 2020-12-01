import time

from selenium import webdriver

driver = webdriver.Firefox()

# test URL
URL = "https://www.bestbuy.com/site/super-mario-bros-mario-casual-crew-socks-2-pack-styles-may-vary/6333956.p?skuId=6333956"

# RTX 3080
# URL = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"

driver.get(URL)

foundButton = False

numAttempts = 1

while not foundButton:

    addToCartButton = addButton = driver.find_element_by_class_name("add-to-cart-button")
    print("driver element find: ", addToCartButton)
    if "btn-disabled" in addToCartButton.get_attribute("class"):
        # delay or wait some time between tries
        time.sleep(3)  # wait 3 seconds

        # refresh the page
        print("Couldn't add to cart! Refreshing page... (Attempt #", numAttempts, ")")
        numAttempts = numAttempts + 1
        driver.refresh()

        # then go back to look for button again
        addToCartButton = addButton = driver.find_element_by_class_name("add-to-cart-button")
    else:
        foundButton = True

print("Adding to cart!")
# print(addToCartButton)
addToCartButton.click()
time.sleep(2)
driver.get("https://www.bestbuy.com/cart")