import time

from playwright.sync_api import *


tags = {
"INPUT_AREA" : "xpath=//*[@jslog='11886']",
"SEARCH_BTN" : "xpath=//*[@jslog='11887']",
"SEARCH ITEMS" :"xpath=//*[@class='Nv2PK THOPZb CpccDe ']/a",
"NAME" : "xpath=(//div[@class='qBF1Pd fontHeadlineSmall '])[1]",
"RATING" : "xpath=(//*[@class='MW4etd'])[1]",
"REVIEW" : "xpath=(//*[@class='UY7F9'])[1]",
"ADDRESS" :"xpath=(//*[@class='W4Efsd']/span[2])[1]"
}

details={}



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=5000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/maps")
    page.locator(tags["INPUT_AREA"]).fill("resturants")
    page.locator(tags["SEARCH_BTN"]).click()

    while True:
        all_item = page.query_selector_all(tags["SEARCH ITEMS"])
        all_item[0].click()
        page.keyboard.press("End")
        if len(all_item)>5:
            break
    L=[]
    for i in range(5):
        D={}
        all_item[i].click()
        time.sleep(5)
        name=page.locator("//h1[@class='DUwDvf lfPIob']").text_content()
        rating=page.locator(("(//span[@class='ceNzKf']//preceding-sibling::span)[1]")).text_content()
        review=page.locator(("(//div[@class='F7nice ']//span)[9]")).text_content()
        address=page.locator("(//div[@class='rogA2c ']//div)[1]").text_content()
        print(name)
        print(rating)
        print(review)
        print(address)
        D['Name']=name
        D['Rating']=rating
        D['Review']=review
        D['Address']=address
        L.append(D)
    print(L)









    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)



