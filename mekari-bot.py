import config
from custom_parser import parser
from datetime import datetime

import login
import os
from playwright.sync_api import sync_playwright, TimeoutError 

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

import sys
from time import sleep

# Command Prompt Configuration -----------------------------------------------------------------------------

install()
console = Console()
args = parser()

# Command Prompt Validation --------------------------------------------------------------------------------

if args.number > config.limit: # Automation limit validation
    console.print(Panel.fit(
        f"[bold red]LimitExceededError :[/]\nThe 'number' value is too large.\nMaximum allowed: {config.limit}. Found: {args.number}",
        title="🚫 Error",
        border_style="red"
    ))
    sys.exit(1)

if args.ib <= 0 : # Automation limit validation
    console.print(Panel.fit(
        f"[bold red]ValueError :[/]\nInitial balance cannot less or equal than 0. \nFound: {args.ib}",
        title="🚫 Error",
        border_style="red"
    ))
    sys.exit(1)

# Playwright Automation -------------------------------------------------------------------------------------

with sync_playwright() as p:

    # Lunch Browser -----------------------------------------------------------------------------------------

    browser = p.chromium.launch(headless=False, channel="chrome")

    # Load and Create Authentication Token ------------------------------------------------------------------

    if os.path.exists(config.AUTH):
        context = browser.new_context(storage_state=config.AUTH)
    else:
        context = browser.new_context()

    # Go To Dashboard ---------------------------------------------------------------------------------------

    page = context.new_page()

    page.goto(config.DASHBOARD_URL, wait_until='load')

    # Check Session -----------------------------------------------------------------------------------------

    if not login.is_logged_in(page):
        console.print("❌ [bold red]Session expired or not logged in. Logging in again...[/]")
        
        with console.status("[bold green]Login ...") as status:
            login.do_login(page)
        
        context.storage_state(path=config.AUTH)
    else:
        console.print("✅ [bold green]Already logged in with saved session.")

    console.print(f"[bold green]Automating[/] [yellow]{args.number}[/] [bold green]Task[/]")

    # Go To Card Menu ---------------------------------------------------------------------------------------

    page.goto(config.CARD_URL)
    
    # Add Card Automation -----------------------------------------------------------------------------------
    
    with console.status("[bold green]Working on tasks...") as status:
        for i in range(args.number):

            # Add Card --------------------------------------------------------------------------------------

            xpath_add_card_btn = "/html/body/div[1]/div/div/div/main/section/div/div[1]/div[2]/div/button"
            page.wait_for_selector("xpath=" + xpath_add_card_btn)
            page.locator("xpath=" + xpath_add_card_btn).click()
            
            # Input Card Name -------------------------------------------------------------------------------

            sleep(0.5)
            x_path_card_name_input = '//*[@id="card-name"]'
            page.wait_for_selector("xpath=" + x_path_card_name_input)
            page.locator("xpath=" + x_path_card_name_input).fill(args.cardname)
            
            # Input Card Purpose ----------------------------------------------------------------------------

            sleep(0.5)
            x_path_card_purpose_input = '//*[@id="card-purpose"]'
            page.locator("xpath=" + x_path_card_purpose_input).fill(str(i+1))
            
            # Input Card Holder -----------------------------------------------------------------------------
            
            sleep(0.5) 
            x_path_card_holder_dropdown = '//*[@id="input-general-filter"]'
            page.locator("xpath=" + x_path_card_holder_dropdown).click() # Click Dropdown
                        
            sleep(0.5)
            x_path_card_holder_teta_input = '//*[@id="card-holder"]'
            page.locator("xpath=" + x_path_card_holder_teta_input).fill(config.card_holder_name) # Search Card Holder
            
            sleep(5)
            x_path_card_holder_teta_btn = "/html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[3]/div[2]/div/section/div[2]/button"
            page.locator("xpath=" + x_path_card_holder_teta_btn).click() # Select Card Holder
            
            # Pick Active Date -----------------------------------------------------------------------------
            
            sleep(0.5)
            x_path_active_date_input = '//*[@id="trip-start-date-input"]'
            page.locator("xpath=" + x_path_active_date_input).click() # Click Date Picker
            
            sleep(0.5)             
            page.query_selector('//html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[1]/section/div/div/div/div[1]/div/button[2]').click() # Click Year Menu
            
            sleep(0.5)
            first_block = int(page.query_selector('//html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[1]/section/div/div/div/div[2]/table/tr[1]/td[1]/div').inner_text())
            last_block = int(page.query_selector('//html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[1]/section/div/div/div/div[2]/table/tr[3]/td[2]/div').inner_text())
            curr_date = datetime.strptime(config.today_date,"%Y-%m-%d")

            while True:
                if first_block <= curr_date.year <= last_block:
                    page.click("table td div:has-text('%s')" % (curr_date.year)) # Select Year
                    break
                elif curr_date.year < first_block:
                    page.click('/html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[1]/section/div/div/div/div[1]/button[1]') # Select Previous Year
                elif curr_date.year > last_block:
                    page.click('/html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[1]/section/div/div/div/div[1]/button[2]') # Select Next Year
                sleep(1)

            page.click("table td div:has-text('%s')" % (curr_date.strftime("%b") )) # Select Month

            sleep(2)
            page.click('table tbody td[title="%s"]' % (curr_date.strftime("%Y-%m-%d"))) # Select Date

            # Pick Valid Thru Date -------------------------------------------------------------------------
            
            sleep(0.5)
            x_path_valid_thru_input = '//*[@id="trip-end-date-input"]'
            page.locator("xpath=" + x_path_valid_thru_input).click() # Click Date Picker
            
            sleep(0.5)
            page.query_selector('//html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[2]/section/div/div/div/div[1]/div/button[2]').click() # Click Year Menu
            
            sleep(0.5)
            first_block = int(page.query_selector('//html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[2]/section/div/div/div/div[2]/table/tr[1]/td[1]/div').inner_text())
            last_block = int(page.query_selector('//html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[2]/section/div/div/div/div[2]/table/tr[3]/td[2]/div').inner_text())
            valid_thru_date = datetime.strptime(config.valid_thru,"%Y-%m-%d")

            while True:
                if  first_block <= valid_thru_date.year <= last_block:
                    page.click("table td div:has-text('%s')" % (valid_thru_date.year)) # Select Year
                    break
                elif valid_thru_date.year < first_block:
                    page.click('/html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[2]/section/div/div/div/div[1]/button[1]') # Select Previous Year
                elif valid_thru_date.year > last_block:
                    page.click('/html/body/div[1]/div/div/div/main/section/div/section/div[1]/div[4]/div[2]/section/div/div/div/div[1]/button[2]') # Select Next Year
                sleep(1)

            page.click("table td div:has-text('%s')" % (valid_thru_date.strftime("%b") )) # Select Month

            sleep(2)
            page.click('table tbody td[title="%s"]' % (valid_thru_date.strftime("%Y-%m-%d"))) # Select Date

            # Select Account -----------------------------------------------------------------------------------------

            sleep(0.5)
            x_path_account_input = '//*[@id="account"]'
            page.locator("xpath=" + x_path_account_input).fill(config.account)

            # Set Initial Balance ------------------------------------------------------------------------------------
            
            sleep(0.5)
            x_path_initial_balance_input = '//*[@id="spending-limit"]'
            page.locator("xpath=" + x_path_initial_balance_input).fill(str(args.ib))
            
            # Click Check Read & Aggreement --------------------------------------------------------------------------
            
            sleep(0.5)
            x_path_check_read_aggreement = '/html/body/div[1]/div/div/div/main/section/div/section/div[3]/div/div[1]/label/span'
            page.locator("xpath=" + x_path_check_read_aggreement).click()

            # Click Save Button -------------------------------------------------------------------------------------

            sleep(0.5)
            x_path_save_btn = '/html/body/div[1]/div/div/div/main/section/div/section/div[3]/div/div[2]/button[2]'
            page.locator("xpath=" + x_path_save_btn).click()

            console.log(f"Task {i+1}/{args.number} complete")
            sleep(config.delay)

    # Close Browser -------------------------------------------------------------------------------------------------

    sleep(2)    
    context.close()
    browser.close()
