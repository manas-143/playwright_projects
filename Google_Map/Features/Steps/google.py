from behave import *
from playwright.sync_api import Playwright, sync_playwright
import csv

tags = {
    "INPUT_AREA": "xpath=//*[@jslog='11886']",
    "SEARCH_BTN": "xpath=//*[@jslog='11887']",
    "SEARCH ITEMS": "xpath=//*[@class='Nv2PK THOPZb CpccDe ']/a",
    "PLACE_NAME": "//h1[@class='DUwDvf lfPIob']",
    "RATINGS": "(//span[@class='ceNzKf']//preceding-sibling::span)[1]",
    "REVIEW": "(//div[@class='F7nice ']//span)[9]",
    "ADDRESS": "(//div[@class='rogA2c ']//div)[1]"

}

start = sync_playwright().start()
browser = start.chromium.launch(headless=False, slow_mo=4000)


@given(u'User is on the google map website')
def launching_browser(context):
    context.tab = browser.new_context()
    context.page = context.tab.new_page()
    context.page.goto("https://www.google.com/maps")  # google maps homepage


@when(u'User search for "{places}"')
def searching_for_places(context, places):
    context.search = places
    context.page.locator(tags["INPUT_AREA"]).fill(places)
    context.page.locator(tags["SEARCH_BTN"]).click()


@when(u'add top "{number}" places with its information')
def adding_places_with_information(context, number):
    context.L = []  # List of all places
    num = int(number)  # Converting string to int

    while True:
        all_item = context.page.query_selector_all(tags["SEARCH ITEMS"])  # all displayed items
        all_item[0].click()
        context.page.keyboard.press("End")  # Scrolling for displaying more items
        if len(all_item) > num:
            break

    # adding the desire number of place details
    for i in range(num):
        D = {}  # adding the place details in dictionary

        all_item[i].click()

        """storing all the texts in dictionary keys"""

        name = context.page.locator(tags["PLACE_NAME"]).text_content()
        rating = context.page.locator(tags["RATINGS"]).text_content()
        review = context.page.locator(tags["REVIEW"]).text_content()
        address = context.page.locator(tags["ADDRESS"]).text_content()

        #  adding the keys to dictionary
        D['Name'] = name
        D['Rating'] = rating
        D['Review'] = review
        D['Address'] = address

        # adding individual details to list
        context.L.append(D)


@then(u'User makes a csv file to save the information')
def saves_company_details_to_csv(context):
    # Specify the CSV file path
    csv_file_path = f'{context.search}'

    # Extract the keys from the first dictionary in the list (assuming all dictionaries have the same keys)
    field_names = context.L[0].keys()

    # Write data to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(context.L)

    print(f"Data has been successfully written to {csv_file_path}")
