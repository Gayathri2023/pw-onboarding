import re
import pytest
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker
from pages.eligibility import eligibility_page
from pages.landing import landing_page
from pages.consent import consent_page
from pages.personal_info import personal_info_page
from pages.otp import otp_page
from pages.recording import recording_page
from pages.preview import preview_page
from pages.finalize_application import finalize_application

fake = Faker()
Employment_Status_Types = ["Employed","Not Employed","Retired","Self Employed","Student"]
select_product="savingsordinary"

def get_malawi_phone() -> str:
    """Generate a fake Malawi phone number without +265 prefix."""
    # Malawi numbers are usually 9 digits after +265
    return str(fake.random_int(min=900000000, max=999999999))

# =========================================================
# PAGE FUNCTIONS
# =========================================================
# --- Upload screen (per-document functions) ---
#
# Cheatsheet reference (File Upload and Download section):
#   el = page.locator('input[type="file"]')
#   el.set_input_files('photos/mountain.png')
#
# set_input_files() must target the actual <input type="file"> element.

def select_document_type(page, doc_type: str):
    """Select the document type in the upload dropdown
    (NATID, SLSIP, CTGND, SKMAP, PHOTO, SIGN)."""
    dropdown = page.get_by_role("combobox").first
    dropdown.wait_for(state="visible")
    dropdown.select_option(doc_type)


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


def upload_salary_slip(page, file_path: str):
    """Upload screen: Salary slip."""
    select_document_type(page, "SLSIP")
    page.get_by_text("Add File").first.click()
    page.locator('input[type="file"]').last.set_input_files(file_path)
    confirm_upload(page)


def upload_certificate_guardian(page, file_path: str):
    """Upload screen: Certificate / guardian document."""
    select_document_type(page, "CTGND")
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

def upload_screen(page, natid_front, natid_back, salary_slip, certificate_guardian,
                   sketch_map, photo, signature):
    """Runs the full upload screen for all required Savings Ordinary documents, in order."""
    upload_national_id(page, natid_front, natid_back)
    upload_salary_slip(page, salary_slip)
    upload_certificate_guardian(page, certificate_guardian)
    upload_sketch_map(page, sketch_map)
    upload_photo(page, photo)
    upload_signature(page, signature)
    page.get_by_role("button", name="Continue").click()


def application_details_page(page, first_name, middle_name, last_name, net_income,
                              home_village, residential_address, issue_date, expiry_date,
                              security_answer, utility_number, name_on_utility_bill,
                              kin_first_name, kin_last_name, kin_mobile):
    """Application details page: personal, ID, and utility bill details."""
    page.goto("https://localhost:8080/#/applicationdetail")

    # Page Assertions (cheatsheet): confirm navigation landed correctly
    # before filling the form.
    expect(page).to_have_url(re.compile(r".*/applicationdetail"))
    page.get_by_role("option", name="No").click()
    page.get_by_role("textbox").nth(1).click()
    page.get_by_role("option", name="MISS").click()

    page.get_by_role("textbox", name="First Name *").fill(first_name)
    page.get_by_role("textbox", name="Middle Name").fill(middle_name)
    page.get_by_role("textbox", name="Last Name *").fill(last_name)
    page.get_by_role("textbox", name="Net Monthly Income *").fill(net_income)
    page.get_by_role("textbox", name="Home Village *").fill(home_village)
    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_address)
    page.get_by_role("textbox", name="Issue Date *").fill(issue_date)
    page.get_by_role("textbox", name="Expiry Date *").fill(expiry_date)
    page.get_by_role("textbox", name="Security Answer *").fill(security_answer)
    page.get_by_role("textbox", name="Utility Number *").fill(utility_number)
    page.locator("#acDezgKwh2ptT6jN").fill(kin_first_name)
    page.locator("#ldTj6SxIQ0TKFscK").fill(kin_last_name)
    page.get_by_role("textbox", name="Mobile number without country").nth(2).fill(kin_mobile)
    page.get_by_role("textbox", name="Name on Utility Bill *").fill(name_on_utility_bill)
    page.get_by_role("button", name="Continue").click()



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

    mobile_number ='117743564'#get_malawi_phone()
    kin_mobile_number = "+265" + get_malawi_phone()
    email ='simbu@gmail.com' # fake.email()
    dob_adult = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")

    page = context.new_page()

    landing_page(page,product_section="Savings",product_name="Savings Ordinary")
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile=mobile_number, email=email, dob=dob_adult)
    otp_page(page,email,mobile_number)

    upload_screen(
        page,
        natid_front="front_image.jpeg",
        natid_back="backside_imagejpeg",
        salary_slip="front_image.jpeg",
        certificate_guardian="front_image.jpeg",
        sketch_map="front_image.jpeg",
        photo="front_image.jpeg",
        signature="front_image.jpeg"
    )

    application_details_page(
        page,
        first_name="SWe",
        middle_name="SRi",
        last_name="d",
        net_income="20,0000",
        home_village="HHHj",
        residential_address="HOMe",
        issue_date="2026-02-04",
        expiry_date="2027-02-10",
        security_answer="XXXYy",
        utility_number="54321",
        name_on_utility_bill="SWe",
        kin_first_name="SRi",
        kin_last_name="NAMe",
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