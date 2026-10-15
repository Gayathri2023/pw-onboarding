import re
import pytest
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker
from pages.landing import landing_page
from pages.consent import consent_page
from pages.eligibility import eligibility_page
from pages.personal_info import personal_info_page
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
    """OTP page: enter the 4-digit OTP and submit."""
    # page.get_by_role("textbox").first.click()
    # page.get_by_role("textbox").first.fill("4")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(1).fill("3")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(2).fill("9")
    # page.keyboard.press("Tab")
    # page.get_by_role("textbox").nth(3).fill("2")
    # page.keyboard.press("Tab")
    
    time.sleep(2)


    submit_btn = page.get_by_role("button", name=re.compile("submit", re.I))
    submit_btn.wait_for(state="visible")
    submit_btn.click()
    time.sleep(2)


# --- Upload screen (per-document functions) ---

def select_document_type(page, doc_type: str):
    """Select the document type in the upload dropdown
    (NATID, SKMAP, CTGND, TOBCOM1, PHOTO, SIGN)."""
    dropdown = page.get_by_role("combobox").first
    dropdown.wait_for(state="visible")
    dropdown.select_option(doc_type)


def confirm_upload(page, ignore_warning: bool = False):
    """Click 'Done' and dismiss the 'Ignore' warning if one appears."""
    page.get_by_role("button", name="Done").click()
    if ignore_warning:
        page.get_by_role("button", name="Ignore").click()


def upload_national_id(page, front_file: str, back_file: str):
    """Upload screen: National ID (front + back images)."""
    select_document_type(page, "NATID")

    # Front image
    page.get_by_role("button", name="Add File").first.set_input_files(front_file)
    confirm_upload(page, ignore_warning=True)
    time.sleep(1)

    # Back image
    page.get_by_role("button", name="Choose File").set_input_files(back_file)
    confirm_upload(page, ignore_warning=True)


def upload_sketch_map(page, file_path: str):
    """Upload screen: Sketch map / home location."""
    select_document_type(page, "SKMAP")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
    time.sleep(1)


def upload_certificate_guardian(page, file_path: str):
    """Upload screen: Certificate / guardian document."""
    select_document_type(page, "CTGND")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
    time.sleep(2)


def upload_business_compliance_cert(page, file_path: str):
    """Upload screen: business/tax compliance certificate (TOBCOM1)."""
    select_document_type(page, "TOBCOM1")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
    time.sleep(2)

def upload_photo(page, file_path: str):
    """Upload screen: Passport-style photo."""
    select_document_type(page, "PHOTO")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
    time.sleep(3)

def upload_signature(page, file_path: str):
    """Upload screen: Signature."""
    select_document_type(page, "SIGN")
    page.get_by_text("Add File").click()
    page.get_by_text("Add File").set_input_files(file_path)
    confirm_upload(page)
    time.sleep(2)


def upload_screen(page, natid_front, natid_back, sketch_map, certificate_guardian,
                   business_compliance_cert, photo, signature):
    """Runs the full upload screen for all required Mlimi Account documents, in order."""
    upload_national_id(page, natid_front, natid_back)
    upload_sketch_map(page, sketch_map)
    upload_certificate_guardian(page, certificate_guardian)
    upload_business_compliance_cert(page, business_compliance_cert)
    upload_photo(page, photo)
    upload_signature(page, signature)
    page.get_by_role("button", name="Continue").click()
    page.locator("span").nth(4).click()


def application_details_page(page, title, first_name, last_name, marital_status,
                               business_activity, net_income, home_district, home_ta,
                               home_village, district_of_origin, ta_of_origin,
                               residential_address, residential_district,
                               issue_date, expiry_date, security_answer,
                               utility_provider, utility_number, name_on_utility_bill,
                               kin_first_name, kin_last_name,
                               kin_relationship, kin_mobile):
    """Application details page: personal, ID, address, security, and next-of-kin details."""

    page.get_by_role("option", name="No").click()
    
    page.get_by_role("textbox").nth(1).click()
    page.get_by_role("option", name=title).click()
    page.get_by_role("option", name="MISS").click()
    

    page.get_by_role("textbox", name="First Name *").fill(first_name)
    page.get_by_role("textbox", name="Last Name *").fill(last_name)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=marital_status).click()

    page.get_by_role("textbox", name="Business Activity *").fill(business_activity)
    page.get_by_role("textbox", name="Net Monthly Income *").fill(net_income)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=home_district).click()

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=home_ta).click()

    page.get_by_role("textbox", name="Home Village").fill(home_village)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=district_of_origin).click()

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=ta_of_origin).click()

    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_address)

    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_label("Options list").get_by_text(residential_district).click()

    page.get_by_role("textbox", name="Issue Date *").fill(issue_date)
    page.get_by_role("textbox", name="Expiry Date *").fill(expiry_date)

    # NOTE: fragile - long generated Angular selector chain.
    page.locator(
        ".application_select.ng-select-searchable.ng-select-clearable"
        ".ng-select.ng-select-single.ng-untouched.ng-pristine.ng-invalid "
        "> .ng-select-container > .ng-arrow-wrapper"
    ).first.click()
    page.get_by_role("option", name="Name of your primary head").click()

    page.get_by_role("textbox", name="Security Answer *").fill(security_answer)

    page.locator(
        ".row.border-div-bottom.pb-4.mt-3.ng-untouched.ng-invalid > div "
        "> .form-group > .application_select > .ng-select-container > .ng-arrow-wrapper"
    ).click()
    page.get_by_role("option", name=utility_provider).click()

    page.get_by_role("textbox", name="Utility Number").fill(utility_number)
    page.get_by_role("textbox", name="Name on Utility Bill *").fill(name_on_utility_bill)

    page.locator("#acDezgKwh2ptT6jN").fill(kin_first_name)
    page.locator("#ldTj6SxIQ0TKFscK").fill(kin_last_name)

    page.locator("div:nth-child(2) > input").click()
    page.get_by_role("option", name=kin_relationship).click()

    page.get_by_role("textbox", name="Mobile number without country").nth(2).fill(kin_mobile)

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
    email = fake.company_email()
    dob_adult = fake.date_of_birth(minimum_age=18, maximum_age=80)
    first_name = fake.first_name_female()
    last_name = fake.last_name()

    page = context.new_page()

    landing_page(page,product_section="Savings",product_name="Mlimi Account")
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile="117773995", email="gayathrima156@gmail.com", dob="2003-09-16")
    otp_page(page)

    upload_screen(
        page,
        natid_front="front_image.jpeg",
        natid_back="backside_image.jpeg",
        sketch_map="front_image.jpeg",
        certificate_guardian="front_image.jpeg",
        business_compliance_cert="front_image.jpeg",
        photo="front_image.jpeg",
        signature="front_image.jpeg",
    )

    application_details_page(
        page,
        title="MISS",
        first_name=first_name,
        last_name=last_name,
        marital_status="Single",
        business_activity=fake.job()[:20],
        net_income="700000",
        home_district="Blantyre",
        home_ta="Kapeni",
        home_village=fake.street_name()[:15],
        district_of_origin="CHITIPA",
        ta_of_origin="STA Nthengatenga",
        residential_address=fake.street_address()[:15],
        residential_district="CHITIPA",
        issue_date="2025-01-21",
        expiry_date="2036-11-09",
        security_answer=fake.word()[:10],
        utility_provider="ESCOM",
        utility_number="12345",
        name_on_utility_bill=f"{first_name} {last_name}",
        kin_first_name=fake.first_name(),
        kin_last_name=fake.last_name(),
        kin_relationship="Sibling",
        kin_mobile=kin_mobile_number,
    )
    recording_page(page)
    preview_page(page)
    finalize_application(page)

    time.sleep(2)
    context.close()
    browser.close()


def test_mlimi_account():
    with sync_playwright() as playwright:
        run(playwright)