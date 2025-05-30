import config
from playwright.sync_api import TimeoutError 
from time import sleep


# Login Checker ---------------------------------------------------------------------------------------------

def is_logged_in(page):
    try:
        page.wait_for_selector('xpath=/html/body/div[1]/div/div/div/div/nav/div/div/div/button/div')
        return True
    except TimeoutError:
        return page.locator("xpath=/html/body/div[1]/div/div/div/div/nav/div/div/div/button/div").is_visible()

# Login Automation ------------------------------------------------------------------------------------------

def do_login(page):
    page.goto(config.LOGIN_URL,wait_until='load')
    page.wait_for_selector('//*[@id="user_email"]') 

    email_input_box = page.locator('//*[@id="user_email"]')
    email_input_box.fill(config.EMAIL)
    
    sleep(0.5)
    pass_input_box = page.locator('//*[@id="user_password"]')
    pass_input_box.fill(config.PASS)
    
    sleep(0.5)
    sign_in_btn = page.locator('//*[@id="new-signin-button"]')
    sign_in_btn.click()
    sleep(0.5)