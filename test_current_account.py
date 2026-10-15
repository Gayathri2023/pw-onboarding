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

def get_malawi_phone() -> str:
    """Generate a fake Malawi phone number without +265 prefix."""
    # Malawi numbers are usually 9 digits after +265
    return str(fake.random_int(min=900000000, max=999999999))


# =========================================================
# PAGE FUNCTIONS
# =========================================================

def otp_page(page):
    """OTP page: enter the 4-digit OTP and submit.

    NOTE: OTP digits are hardcoded here for now - fragile if the test
    environment's OTP changes. Replace with a real OTP retrieval mechanism
    once one is available.
    """
    # page.get_by_role("textbox").first.click()
    # page.get_by_role("textbox").first.fill("7")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(1).fill("1")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(2).fill("2")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(3).fill("9")
    # page.keyboard.press("Tab")
    time.sleep(2)

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

def select_document_type(page, doc_type: str):
    """Select the document type in the upload dropdown
    (CTGND, SLSIP, SKMAP, SIGN, PHOTO)."""
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


def upload_certificate_guardian(page, file_path: str):
    """Upload screen: Certificate / guardian document."""
    select_document_type(page, "CTGND")
    page.locator("div").filter(has_text="Add File").nth(5).click()
    page.locator("div").filter(has_text="Add File").nth(5).set_input_files(file_path)
    confirm_upload(page)

def upload_salary_slip(page, file_path: str):
    """Upload screen: Salary slip."""
    select_document_type(page, "SLSIP")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    page.locator("label").filter(has_text="Add File").first.click()
    confirm_upload(page)

def upload_sketch_map(page, file_path: str):
    """Upload screen: Sketch map / home location."""
    select_document_type(page, "SKMAP")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)

def upload_signature(page, file_path: str):
    """Upload screen: Signature."""
    select_document_type(page, "SIGN")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)

def upload_photo(page, file_path: str):
    """Upload screen: Passport-style photo."""
    page.get_by_role("combobox").select_option("PHOTO")
    page.get_by_role("button", name="Add File").set_input_files(file_path)
    confirm_upload(page)

def upload_screen(page, certificate_guardian, salary_slip, sketch_map, signature, photo):
    """Runs the full upload screen for all required Current Account documents, in order."""
    upload_certificate_guardian(page, certificate_guardian)
    upload_salary_slip(page, salary_slip)
    upload_sketch_map(page, sketch_map)
    upload_signature(page, signature)
    upload_photo(page, photo)
    
    page.get_by_role("button", name="Continue").click()


def application_details_page(page, first_name, middle_name, last_name, marital_status,
                              employment_type, business_activity, net_income, district,
                              traditional_authority, home_village, branch_district, branch,
                              residential_address, landmark, issue_date, expiry_date,
                              security_answer, utility_type, utility_number, name_on_utility_bill,
                              kin_relationship, kin_mobile):
    """Application details page: personal, employment, address, ID, and utility bill details."""

    page.get_by_role("option", name="No").click()
    page.get_by_role("textbox").nth(1).click()
    page.get_by_role("option", name="MISS").click()

    page.get_by_role("textbox", name="First Name *").fill(first_name)
    page.get_by_role("textbox", name="Middle Name").fill(middle_name)
    page.get_by_role("textbox", name="Last Name *").fill(last_name)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=marital_status).click()

    # Employment Status
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_text(employment_type).click()
    page.get_by_role("textbox", name="Business Activity *").fill(business_activity)
    page.get_by_role("textbox", name="Net Monthly Income *").fill(net_income)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=district).click()
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_text(traditional_authority).click()
    page.get_by_role("textbox", name="Home Village").fill(home_village)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=branch_district).click()
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=branch).click()
    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_address)
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_text(landmark).click()

    page.get_by_role("textbox", name="Issue Date *").fill(issue_date)
    page.get_by_role("textbox", name="Expiry Date *").fill(expiry_date)
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name="Last 4 digits of your Nat. ID?").click()
    page.get_by_role("textbox", name="Security Answer *").fill(security_answer)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=utility_type).click()
    page.get_by_role("textbox", name="Utility Number *").fill(utility_number)
    page.get_by_role("textbox", name="Name on Utility Bill *").fill(name_on_utility_bill)

    # NOTE: these element IDs are dynamically generated and may not be
    # stable across sessions - replace with role/label based locators
    # once confirmed with Ezhil.
    page.locator("#acDezgKwh2ptT6jN").fill(name_on_utility_bill)
    page.locator("#ldTj6SxIQ0TKFscK").fill(name_on_utility_bill)

    page.locator("div:nth-child(2) > input").click()
    page.get_by_role("option", name=kin_relationship).click()
    kin_mobile_field = page.locator("ngx-intl-tel-input").filter(
        has_text="Uganda+256India (भारत)+"
    ).get_by_placeholder("Mobile number without country")
    kin_mobile_field.click()
    kin_mobile_field.fill(kin_mobile)

    # Step through the "Next of KIN Details" panel confirmations
    for _ in range(3):
        page.locator("div").filter(
            has_text=re.compile(r"^Next of KIN Details: 1$")
        ).first.click()
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


    mobile_number = get_malawi_phone()
    kin_mobile_number = "+265" + get_malawi_phone()
    email = fake.email()
    dob_adult = fake.date_of_birth(minimum_age=18, maximum_age=80)

    page = context.new_page()

    landing_page(page,product_section="Retail Accounts",product_name="Current Account")
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile=mobile_number, email=email, dob=dob_adult)
    otp_page(page)

    upload_screen(
        page,
        certificate_guardian="WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg",
        salary_slip="WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg",
        sketch_map="WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg",
        signature="WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg",
        photo="WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg",
    )

    application_details_page(
        page,
        first_name="SWETHa",
        middle_name="SRi",
        last_name="d",
        marital_status="Single",
        employment_type="Self Employed",
        business_activity="ABc",
        net_income="60,0000",
        district="Chitipa",
        traditional_authority="Mwenewenya",
        home_village="27SEe",
        branch_district="BLANTYRE URBAN",
        branch="BCA",
        residential_address="XXx",
        landmark="CHICHIRI SHOPPING MALL",
        issue_date="2024-05-13",
        expiry_date="2035-10-24",
        security_answer="7654",
        utility_type="MHC Invoice",
        utility_number="123345",
        name_on_utility_bill="TSe",
        kin_relationship="Cousin",
        kin_mobile=kin_mobile_number,
    )
    recording_page(page)
    preview_page(page)
    finalize_application(page)

    

    time.sleep(2)
    context.close()
    browser.close()


def test_current_account():
    with sync_playwright() as playwright:
        run(playwright)