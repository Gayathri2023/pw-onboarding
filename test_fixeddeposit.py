import re
import pytest
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker

fake = Faker()


def get_malawi_phone() -> str:
    
    """Generate a fake Malawi phone number without +265 prefix."""
    # Malawi numbers are usually 9 digits after +265
    return str(fake.random_int(min=900000000, max=999999999))



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
   #landing page 
    page.goto("https://localhost:8080",wait_until="domcontentloaded")
    page.get_by_role("heading", name="Investment Accounts").click()
    page.get_by_role("heading", name="Fixed Deposit").click()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)
    page.get_by_role("radio").first.check()
    page.get_by_role("radio").nth(2).check()
    page.get_by_role("radio").nth(4).check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").check()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)
    #personal details
    page.get_by_role("textbox", name="Mobile number without country").click()
    page.get_by_role("textbox", name="Mobile number without country").fill("119973852")
    time.sleep(2)
    page.get_by_role("textbox", name="Email address").click()
    page.get_by_role("textbox", name="Email address").fill("gayathrima156@gmail.com")
    time.sleep(2)
    page.get_by_role("textbox", name="Date of birth").click()
    page.get_by_placeholder("Date of birth").fill("2003-03-14")
    time.sleep(2)
    page.get_by_role("button", name="Get OTP").click()
    page.pause()
    # page.locator("#otp_0_7ujh9kvdjkpmrkbbmzj").click()
    # page.locator("#otp_0_7ujh9kvdjkpmrkbbmzj").fill("8")
    # page.locator("#otp_1_7ujh9kvdjkpmrkbbmzj").fill("6")
    # page.locator("#otp_2_7ujh9kvdjkpmrkbbmzj").fill("2")
    # page.locator("#otp_3_7ujh9kvdjkpmrkbbmzj").fill("3")
    page.get_by_role("button", name="Submit").click()
    time.sleep(2)
    #application details
    page.get_by_role("combobox").first.select_option("NATID")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("button", name="Done").click()
    page.get_by_role("button", name="Ignore").click()
    page.get_by_role("button", name="Choose File").set_input_files("backside_image.jpeg")
    page.get_by_role("button", name="Done").click()
    page.get_by_role("button", name="Ignore").click()
    page.get_by_role("combobox").first.select_option("PHOTO")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("button", name="Done").click()
    page.get_by_role("combobox").select_option("SIGN")
    page.get_by_text("Add File").click()
    page.get_by_text("Add File").set_input_files("front_image.jpeg")
    page.get_by_role("button", name="Done").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("spinbutton", name="Account Number *").click()
    page.get_by_role("spinbutton", name="Account Number *").fill("1010834585")
    page.get_by_role("textbox", name="ID Number *").click()
    page.get_by_role("textbox", name="ID Number *").fill("12543")
    page.get_by_role("spinbutton", name="OTP *").click()
    page.get_by_role("spinbutton", name="OTP *").fill("23456")
    page.get_by_role("textbox", name="First Name *").click()
    page.get_by_role("button", name="Ok").click()
    page.get_by_role("textbox", name="First Name *").fill("SYESh")
    page.get_by_role("textbox", name="Last Name *").click()
    page.get_by_role("textbox", name="Last Name *").fill("a")
    page.locator("ng-select").filter(has_text="Choose NBM Branch").locator("input[type=\"text\"]").click()
    page.get_by_role("option", name="CHICHIRI SHOPPING MALL").click()
    page.locator("input[type=\"text\"]").nth(4).click()
    page.get_by_role("option", name="3 MONTHS").click()
    page.locator("input[type=\"text\"]").nth(5).click()
    page.get_by_text("MALAWIAN KWACHA - MWK").click()
    page.get_by_role("textbox", name="Amount *").click()
    page.get_by_role("textbox", name="Amount *").fill("126,7000")
    page.locator(".application_select.ng-select-searchable.ng-select-clearable.ng-select.ng-select-single.ng-untouched > .ng-select-container > .ng-arrow-wrapper").click()
    page.get_by_text("Reinvest (rollover) both").click()
    page.get_by_role("button", name="Continue").click()
    #recording page
    page.get_by_role("button", name="I am Ready").click()
    page.get_by_role("button", name="Start Video Recording").click()
    page.get_by_role("button", name="End Video Recording").click()
    page.get_by_role("button", name="Continue").click()
    #preview and submit page
    page.goto("https://localhost:8080/#/preview")
    page.get_by_role("checkbox").nth(1).check()
    page.locator("canvas").click(position={"x":324,"y":139})
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Submit").click()
    page.goto("https://localhost:8080/#/integration")
    page.get_by_role("button", name="Ok").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
