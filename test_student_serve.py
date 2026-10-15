import re
import pytest
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker
from pages.eligibility import eligibility_page
from pages.landing import landing_page
from pages.consent import consent_page
from pages.personal_info import personal_info_page
from pages.recording import recording_page
from pages.preview import preview_page
from pages.finalize_application import finalize_application
fake = Faker()


def get_malawi_phone() -> str:
    """Generate a fake Malawi phone number without +265 prefix."""
    return str(fake.random_int(min=900000000, max=999999999))


# =========================================================
# PAGE FUNCTIONS
# =========================================================


def otp_page(page):
    """OTP page: enter the 4-digit OTP and submit."""
    # page.get_by_role("textbox").first.click()
    # page.get_by_role("textbox").first.fill("7")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(1).fill("6")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(2).fill("3")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(3).fill("7")
    # page.keyboard.press("Tab")

    submit_btn = page.get_by_role("button", name=re.compile("submit", re.I))
    submit_btn.wait_for(state="visible")
    submit_btn.click()


# --- Upload screen (per-document functions) ---
#
# Cheatsheet reference (File Upload and Download section):
#   el = page.locator('input[type="file"]')
#   el.set_input_files('photos/mountain.png')
#
# set_input_files() must target the actual <input type="file"> element.
# The original script called it on get_by_text("Add File") and
# get_by_role("img"), neither of which is a file input per the
# cheatsheet's own documented usage, so every upload below is rewritten
# to locate 'input[type="file"]' directly.

def select_document_type(page, doc_type: str):
    """Select the document type in the upload dropdown (NATID, ADM_LTR, SKMAP, PHOTO, SIGN)."""
    page.get_by_role("combobox").first.select_option(doc_type)


def confirm_upload(page, double_click: bool = False, ignore_warning: bool = False):
    """Click 'Done' (or double-click it) and dismiss the 'Ignore' warning if one appears."""
    done_btn = page.get_by_role("button", name="Done")
    if double_click:
        done_btn.dblclick()
    else:
        done_btn.click()
    if ignore_warning:
        page.get_by_role("button", name="Ignore").click()


def upload_national_id(page, front_file: str, back_file: str):
    """Upload screen: National ID (front + back images)."""
    select_document_type(page, "NATID")

    # Front image
    page.get_by_text("Add File").first.click()
    page.locator('input[type="file"]').last.set_input_files(front_file)
    confirm_upload(page, double_click=True, ignore_warning=True)

    # Back image
    page.get_by_role("button", name="Choose File").click()
    page.locator('input[type="file"]').last.set_input_files(back_file)
    confirm_upload(page, double_click=True, ignore_warning=True)


def upload_admission_letter(page, file_path: str):
    """Upload screen: Admission letter."""
    select_document_type(page, "ADM_LTR")
    page.get_by_text("Add File").first.click()
    page.locator('input[type="file"]').last.set_input_files(file_path)
    confirm_upload(page)


def upload_sketch_map(page, file_path: str):
    """Upload screen: Sketch map / home location."""
    select_document_type(page, "SKMAP")
    page.get_by_text("Add File").first.click()
    page.locator('input[type="file"]').last.set_input_files(file_path)
    confirm_upload(page)


def upload_photo(page, file_path: str):
    """Upload screen: Passport-style photo."""
    select_document_type(page, "PHOTO")
    page.locator(".deskViewShow").first.click()
    page.get_by_role("button", name="Add File").first.click()
    page.locator('input[type="file"]').last.set_input_files(file_path)
    confirm_upload(page)


def upload_signature(page, file_path: str):
    """Upload screen: Signature."""
    page.get_by_role("combobox").select_option("SIGN")
    page.get_by_role("button", name="Add File").click()
    page.locator('input[type="file"]').last.set_input_files(file_path)
    confirm_upload(page)

def upload_screen(page, natid_front, natid_back, adm_letter, sketch_map, photo, signature):
    """Runs the full upload screen for all 5 required documents, in order."""
    upload_national_id(page, natid_front, natid_back)
    upload_admission_letter(page, adm_letter)
    upload_sketch_map(page, sketch_map)
    upload_photo(page, photo)
    upload_signature(page, signature)
    page.get_by_role("button", name="Continue").click()


def application_details_page(page, middle_name, last_name, university, university_address,
                              admission_date, net_income, home_village, residential_address,
                              issue_date, expiry_date, security_answer):
    """Application details page: student + ID details."""
    page.goto("https://localhost:8080/#/applicationdetail")

    # Page Assertions (cheatsheet): confirm navigation landed correctly
    # before filling the form.
    expect(page).to_have_url(re.compile(r".*/applicationdetail"))

    page.get_by_role("textbox", name="Middle Name").fill(middle_name)
    page.get_by_role("textbox", name="Last Name *").fill(last_name)
    page.get_by_role("textbox", name="University College Name *").fill(university)
    page.get_by_role("textbox", name="University or College Address").fill(university_address)
    page.get_by_role("textbox", name="Admission Date *").fill(admission_date)
    page.get_by_role("textbox", name="Net Monthly Income *").fill(net_income)
    page.get_by_role("textbox", name="Home Village").fill(home_village)
    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_address)
    page.get_by_role("textbox", name="Issue Date *").fill(issue_date)
    page.get_by_role("textbox", name="Expiry Date *").fill(expiry_date)
    page.get_by_role("textbox", name="Security Answer *").fill(security_answer)


def kin_details_page(page, kin_first_name, kin_last_name, kin_mobile):
    """Next of kin page: kin name and mobile number."""
    page.locator("#acDezgKwh2ptT6jN").fill(kin_first_name)
    page.locator("#ldTj6SxIQ0TKFscK").fill(kin_last_name)
    page.get_by_role("textbox", name="Mobile number without country").nth(1).fill(kin_mobile)




# =========================================================
# MAIN FLOW
# =========================================================

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        permissions=["camera", "microphone", "geolocation"],  # grant permissions
        geolocation={"latitude": 12.9716, "longitude": 77.5946},  # example: Bangalore
        locale="en-US"
    )


    mobile_number = get_malawi_phone()
    kin_mobile_number = "+265" + get_malawi_phone()
    email = fake.email()

    page = context.new_page()

    landing_page(page,product_section="Students Account",product_name="Student Serve")
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile=mobile_number, email=email, dob="2003-11-15")
    otp_page(page)

    upload_screen(
        page,
        natid_front="front_image.jpeg",
        natid_back="backside_image.jpegg",
        adm_letter="front_image.jpegg",
        sketch_map="front_image.jpeg",
        photo="front_image.jpeg",
        signature="front_image.jpeg"
    )

    application_details_page(
        page,
        middle_name=fake.first_name(),
        last_name=fake.last_name(),
        university="MAKRERe",
        university_address="KAMPALa",
        admission_date="2025-01-31",
        net_income="500,000",
        home_village="HHj",
        residential_address="HHJJJi",
        issue_date="2025-01-31",
        expiry_date="2032-06-10",
        security_answer="ABc"
    )

    kin_details_page(
        page,
        kin_first_name=fake.first_name(),
        kin_last_name=fake.last_name(),
        kin_mobile=kin_mobile_number
    )
    recording_page(page)
    preview_page(page)
    finalize_application(page)

    time.sleep(2)
    context.close()
    browser.close()

def test_savings_ordinary():
    with sync_playwright() as playwright:
        run(playwright) 