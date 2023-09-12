from playwright.sync_api import Playwright, sync_playwright, expect

tags = {

    'USER NAME': "xpath=//*[@id='user-name']",
    'PASSWORD':  "xpath=//*[@id='password']",
    'LOGIN': "xpath=//*[@id='login-button']",
    "HEADER": "xpath=//*[@class='title']",
    "BURGER": "xpath=//*[@id='react-burger-menu-btn']",
    "LOGOUT": "xpath=//*[@id='logout_sidebar_link']"

}
def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False, slow_mo=3000)  #slow_mo is used for slowing down the process
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 521})      #viewpoint is for setting windows to maximum width and height as playwright have no inbuilt methods for maximizing

    page.goto("https://www.saucedemo.com/")    #containing url


    #for login credential
    page.locator(tags["USER NAME"]).type("standard_user", delay=1000)
    page.locator(tags["PASSWORD"]).fill("secret_sauce")
    page.locator(tags["LOGIN"]).click()

    #for knowing if the user correctly logged in or not
    assert page.locator(tags["HEADER"]).is_visible(),'login failed'
    print("valid login")

    #for navigating back
    page.go_back()

    #for navigatin forward
    page.go_forward()

    print(page.url)  #for printing current url
    #for log out
    page.locator(tags["BURGER"]).click()
    page.locator(tags["LOGOUT"]).click()

    # for knowing if the user correctly logged out or not
    assert page.locator(tags["LOGIN"]).is_visible(),'logout failed'
    print("user logged out")



    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="HP Laptop 15s, AMD Ryzen 7 5700U, 15.6-inch (39.6 cm), FHD, 16GB DDR4, 512GB SSD, AMD Radeon Graphics, Backlit KB, Thin & Light, Dual Speakers (Win 11, MSO 2021, Silver, 1.69 kg), ey2001AU").click()
    page1 = page1_info.value
    page1.get_by_title("Add to Shopping Cart").click()
    page1.close()