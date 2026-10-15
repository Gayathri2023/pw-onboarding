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



    # #landing page
    # page.goto("https://localhost:8080/#/")
    # page.get_by_role("heading", name="Retail Accounts").click()
    # page.get_by_role("heading", name="Savings Special Saver").click()
    # page.get_by_text("Signature DocumentDocument").click()
    # page.get_by_role("button", name="Continue").click()
    # time.sleep(2)
    # page.get_by_role("checkbox").check()
    # page.get_by_role("button", name="Continue").click()
    # time.sleep(2)
    # page.get_by_role("radio").first.check()
    # page.get_by_role("radio").nth(2).check()
    # page.get_by_role("radio").nth(4).check()
    # page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    # page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    # page.locator(".ng-untouched.ng-pristine.ng-invalid").check()
    # page.get_by_role("button", name="Continue").click()
    # time.sleep(2)
    #  #personal details 
    # page.get_by_role("textbox", name="Mobile number without country").click()
    # page.get_by_role("textbox", name="Mobile number without country").fill("117779836")
    # time.sleep(2)
    # page.get_by_role("textbox", name="Email address").click()
    # page.get_by_role("textbox", name="Email address").fill("gayathrima156@gmail.com")
    # time.sleep(2)
    # page.get_by_role("textbox", name="Date of birth").click()
    # page.get_by_placeholder("Date of birth").fill("2001-02-14")
    # time.sleep(2)
    # page.get_by_role("button", name="Get OTP").click()
    # page.pause()
    # # page.locator("#otp_0_rx9arhwzapqmrki9sjh").click()
    # # page.locator("#otp_0_rx9arhwzapqmrki9sjh").fill("3")
    # # page.locator("#otp_1_rx9arhwzapqmrki9sjh").fill("3")
    # # page.locator("#otp_2_rx9arhwzapqmrki9sjh").fill("9")
    # # page.locator("#otp_3_rx9arhwzapqmrki9sjh").fill("7")
    # page.get_by_role("button", name="Submit").click()
    # time.sleep(2)
    #document page
def select_document_type(page, doc_type: str):
    """Select the document type in the upload dropdown."""
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
 
 
def upload_certificate_guardian(page, file_path: str):
    """Upload screen: certificate / guardian document."""
    select_document_type(page, "CTGND")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
 
def upload_sketch_map(page, file_path: str):
    """Upload screen: sketch map / home location."""
    select_document_type(page, "SKMAP")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)

def upload_salary_slip(page, file_path: str):
    """Upload screen: salary slip."""
    select_document_type(page, "SLSIP")
    page.locator(".deskViewShow").first.click()
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
def upload_photo(page, file_path: str):
    """Upload screen: applicant photo."""
    select_document_type(page, "PHOTO")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
def upload_signature(page, file_path: str):
    """Upload screen: signature."""
    page.get_by_role("combobox").select_option("SIGN")
    page.get_by_role("button", name="Add File").set_input_files(file_path)
    confirm_upload(page)
 
def upload_screen(page, natid_front, natid_back, certificate_guardian, sketch_map, salary_slip, photo, signature):
    """Runs the full upload screen for all required Savings Special Saver documents."""
    upload_national_id(page, natid_front, natid_back)
    upload_certificate_guardian(page, certificate_guardian)
    upload_sketch_map(page, sketch_map)
    upload_salary_slip(page, salary_slip)
    upload_photo(page, photo)
    upload_signature(page, signature)
    page.get_by_role("button", name="Continue").click()
 

    #application details
def application_details_page(page, first_name, last_name, employers_name, employers_address,
                              employers_business, employment_start_date, gross_salary, net_salary,
                              home_village, residential_address, issue_date, expiry_date,
                              security_answer, utility_number, name_on_utility_bill,
                              kin_first_name, kin_last_name, kin_mobile):
    """Application details page: personal, employment, ID, utility, and kin details."""
    page.goto("https://localhost:8080/#/applicationdetail")
    expect(page).to_have_url(re.compile(r".*/applicationdetail"))
 
    page.get_by_role("textbox", name="First Name *").fill(first_name)
    page.get_by_role("textbox", name="Last Name *").fill(last_name)
    page.get_by_role("textbox", name="Employers Name *").fill(employers_name)
    page.get_by_role("textbox", name="Employers Address").fill(employers_address)
    page.get_by_role("textbox", name="Employers Business").fill(employers_business)
    page.get_by_role("textbox", name="Employment Start Date").fill(employment_start_date)
    page.get_by_role("textbox", name="Gross Salary *").fill(gross_salary)
    page.get_by_role("textbox", name="Net Salary *").fill(net_salary)
    page.get_by_role("textbox", name="Home Village *").fill(home_village)
    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_address)
    page.get_by_role("textbox", name="Issue Date *").fill(issue_date)
    page.get_by_role("textbox", name="Expiry Date *").fill(expiry_date)
    page.get_by_role("textbox", name="Security Answer *").fill(security_answer)
    page.get_by_role("textbox", name="Utility Number *").fill(utility_number)
    page.get_by_role("textbox", name="Name on Utility Bill *").fill(name_on_utility_bill)
 
    # Kin details 
    page.locator("#acDezgKwh2ptT6jN").fill(kin_first_name)
    page.locator("#ldTj6SxIQ0TKFscK").fill(kin_last_name)
    page.get_by_role("textbox", name="Mobile number without country").nth(2).fill(kin_mobile)
    page.get_by_role("button", name="Continue").click()

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        permissions=["camera", "microphone", "geolocation"],  # grant permissions
        geolocation={"latitude": 12.9716, "longitude": 77.5946},  # example: Bangalore
        locale="en-US"
    )
 
    mobile_number = get_malawi_phone()
    kin_mobile_number = "+265" + get_malawi_phone()
    email = fake.user_email()
    dob_adult = fake.date_of_birth(minimum_age=18, maximum_age=80)
    page = context.new_page()
 
    landing_page(page, product_section="Retail Accounts", product_name="Savings Special Saver")
    # NOTE: same extra pre-continue click seen in the Minors/ITF flow - see
    # that file's note about possibly adding this as a landing_page() param.
    page.get_by_text("Signature Document").click()
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile=mobile_number, email=email, dob=dob_adult)
    otp_page(page)
    
 
    upload_screen(
        page,
        natid_front="front_image.jpeg",
        natid_back="backside_image.jpeg",
        certificate_guardian="front_image.jpeg",
        sketch_map="front_image.jpeg",
        salary_slip="front_image.jpeg",
        photo="front_image.jpeg",
        signature="front_image.jpeg",
    )
 
    application_details_page(
        page,
        first_name=fake.first_name().upper(),
        last_name=fake.last_name().upper(),
        employers_name=fake.company().upper(),
        employers_address=f"STREET{fake.random_int(min=1, max=99)}",
        employers_business="SALES",
        employment_start_date="2024-06-13",
        gross_salary="70,0000",
        net_salary="50,0000",
        home_village="BLANTYRE NEAR",
        residential_address=f"HOUSE {fake.random_int(min=1, max=99)}",
        issue_date="2025-02-18",
        expiry_date="2030-10-24",
        security_answer=str(fake.random_int(min=1000, max=9999)),
        utility_number=str(fake.random_int(min=10000, max=99999)),
        name_on_utility_bill="TEST",
        kin_first_name=fake.first_name().upper(),
        kin_last_name=fake.last_name().upper(),
        kin_mobile=kin_mobile_number,
    )
    recording_page(page)
    preview_page(page)
    finalize_application(page)
 
    
 
    time.sleep(2)
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
