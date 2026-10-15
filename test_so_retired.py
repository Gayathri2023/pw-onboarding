import re
import pytest
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
   #landingpage
    page.goto("https://localhost:8080/#/",wait_until="domcontentloaded")
    page.get_by_role("heading", name="Retail Accounts").click()
    page.get_by_role("heading", name="Savings Ordinary").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("radio").first.check()
    page.get_by_role("radio").nth(2).check()
    page.get_by_role("radio").nth(4).check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").check()
    page.get_by_role("button", name="Continue").click()
    #personal information detials(mobilenumber,email)
    page.get_by_role("textbox", name="Mobile number without country").click()
    page.get_by_role("textbox", name="Mobile number without country").fill("111337775")
    page.get_by_role("textbox", name="Email address").click()
    page.get_by_role("textbox", name="Email address").fill("gayathrima156@gmail.com")
    page.get_by_role("textbox", name="Date of birth").click()
    page.get_by_placeholder("Date of birth").fill("2003-06-12")
    #onetimepassword details
    page.get_by_role("button", name="Get OTP").click()
    # page.locator("#otp_0_ifocnb19umkmrixztcv").fill("7")
    # page.locator("#otp_1_ifocnb19umkmrixztcv").fill("1")
    # page.locator("#otp_2_ifocnb19umkmrixztcv").fill("9")
    # page.locator("#otp_3_ifocnb19umkmrixztcv").fill("5")
    page.get_by_role("button", name="Submit").click()
    #document form details
    page.locator("div").filter(has_text="Applying For - Savings").click()
   
    page.get_by_role("combobox").first.select_option("NATID")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("button", name="Choose File").set_input_files("backside_image.jpeg")
    page.get_by_role("combobox").first.select_option("SLSIP")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("combobox").first.select_option("CTGND")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("combobox").first.select_option("SKMAP")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("combobox").first.select_option("PHOTO")
    page.get_by_role("button", name="Add File").first.set_input_files("front_image.jpeg")
    page.get_by_role("combobox").select_option("SIGN")
    page.get_by_role("button", name="Add File").set_input_files("front_image.jpeg")
   #aplication details
    page.goto("https://localhost:8080/#/applicationdetail")
    page.get_by_role("textbox", name="First Name *").fill("SYRIVIA,s")
    page.get_by_role("textbox", name="Middle Name").fill("SWe")
    page.get_by_role("textbox", name="Last Name *").fill("Dd")
    page.get_by_role("textbox", name="Net Monthly Income *").fill("70,0000")
    page.get_by_role("textbox", name="Home Village *").fill("FFFGo")
    page.get_by_role("textbox", name="Residential Physical Address").fill("HHJo")
    page.get_by_role("textbox", name="Issue Date *").fill("2025-01-21")
    page.get_by_role("textbox", name="Expiry Date *").fill("2035-10-20")
    page.get_by_role("textbox", name="Security Answer *").fill("5432")
    page.get_by_role("textbox", name="Utility Number *").fill("12345")
    page.get_by_role("textbox", name="Name on Utility Bill *").fill("TEST4")
    page.locator("#acDezgKwh2ptT6jN").fill("SWe")
    page.locator("#ldTj6SxIQ0TKFscK").fill("NMe")
    page.get_by_role("textbox", name="Mobile number without country").nth(2).fill("+265115577543")
    page.goto("https://localhost:8080/#/integration")

    # ---------------------
    context.close()
    browser.close()


def test_so_retired():
    with sync_playwright() as playwright:
        run(playwright)