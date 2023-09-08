
from playwright.sync_api import *

tags = {"SEARCH BOX": "xpath=//*[@id='twotabsearchtextbox']",
        "SEARCH": "xpath=//*[@id='nav-search-submit-button']",
        "RATINGS": "xpath =//li[@id='p_72/1318476031']",
        "LAPTOPS LIST": "xpath=//span[@class='a-size-medium a-color-base a-text-normal']",
        "CART BTN": "xpath=//*[@id='add-to-cart-button']",
        "CART ICON": "xpath=//*[@class='nav-cart-icon nav-sprite']",
        "PRICE_TAG": "xpath=//*[@id='sc-subtotal-amount-buybox']/span",
        "LAPTOP_AMT" : "xpath=//span[@id='tp_price_block_total_price_ww']/descendant::span[@class='a-price-whole']"

        }


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=5000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.amazon.in/")  # containing url

    page.locator(tags["SEARCH BOX"]).fill("hp laptops")
    page.locator(tags["SEARCH"]).click()
    page.locator(tags["RATINGS"]).click()
    all_laptops = page.locator(tags["LAPTOPS LIST"])
    amount = []
    for i in range(all_laptops.count()):
        if i == 3:
            break
        else:
            all_laptops.nth(i).click()
            p = context.pages
            amt = p[1].locator(tags["LAPTOP_AMT"]).inner_text()
            amount.append(float(amt.replace(",","")))
            p[1].locator(tags["CART BTN"]).click()
            p[1].close()
    page.locator(tags["CART ICON"]).click()
    final_price = page.locator(tags["PRICE_TAG"]).inner_text()
    price = final_price.replace(",","")
    cart_amt = float(price)
    laptop_amt = sum(amount)
    assert laptop_amt==cart_amt,"amount not matching"
    print("testcases passed")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
