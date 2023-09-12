from behave import *
from playwright.sync_api import Playwright, sync_playwright

"""......................all the locators......................"""

tags = {"SEARCH BOX": "xpath=//*[@id='twotabsearchtextbox']",
        "SEARCH": "xpath=//*[@id='nav-search-submit-button']",
        "RATINGS": "xpath =//li[@id='p_72/1318476031']",
        "LAPTOPS LIST": "xpath=//span[@class='a-size-medium a-color-base a-text-normal']",
        "CART BTN": "xpath=//*[@id='add-to-cart-button']",
        "CART ICON": "xpath=//*[@class='nav-cart-icon nav-sprite']",
        "PRICE_TAG": "xpath=//*[@id='sc-subtotal-amount-buybox']/span",
        "LAPTOP_AMT": "xpath=//span[@id='tp_price_block_total_price_ww']/descendant::span[@class='a-price-whole']"
        }
""".............................................................."""


amount = []  # to store the  amount of each laptop

# start playwright
start = sync_playwright().start()
browser = start.chromium.launch(headless=False)


@step('User is on the Amazon website')
def visit_amazon_homepage(context):
    context.tab = browser.new_context()
    context.page = context.tab.new_page()
    context.page.goto("https://www.amazon.in/")  # amazon homepage


@step('User search for "{search_query}"')
def search_for_laptops(context, search_query):
    context.page.locator(tags["SEARCH BOX"]).fill(search_query)  # search query contains the laptop brands
    context.page.locator(tags["SEARCH"]).click()


@step('User filter by ratings')
def filter_by_ratings(context):
    context.page.locator(tags["RATINGS"]).click()  # all laptops above 4star


@step('add top "{number}" laptops to the cart')
def add_laptops_to_cart(context, number):
    all_laptops = context.page.locator(tags["LAPTOPS LIST"])  # above 4star rating laptops

    for i in range( int(number)):
        with context.page.expect_popup() as page1_info:
            all_laptops.nth(i).click()  # click on each laptop
        context.page1 = page1_info.value  # going to next tab
        amt = context.page1.locator(tags["LAPTOP_AMT"]).inner_text()
        amount.append(float(amt.replace(",", "")))  # storing each laptop value in float
        context.page1.locator(tags["CART BTN"]).click()  # adding the laptop in cart
        context.page1.close() # closing the new tab


@step('the total amount in the cart should match the laptop prices')
def verify_cart_total(context):
    context.page.locator(tags["CART ICON"]).click() # going to cart
    final_price = context.page.locator(tags["PRICE_TAG"]).inner_text()  # extracting the total price
    price = final_price.replace(",", "")
    cart_amt = float(price)
    laptop_amt = sum(amount)
    assert laptop_amt == cart_amt, "Amount not matching"
    print("Test case passed")
