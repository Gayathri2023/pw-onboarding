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
    # page.goto("https://localhost:8080/#/",wait_until="domcontentloaded")
    # page.get_by_role("heading", name="Retail Accounts").click()
    # page.get_by_role("heading", name="Minors / ITF Account").click()
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
    # #personal details
    # page.get_by_role("textbox", name="Mobile number without country").click()
    # page.get_by_role("textbox", name="Mobile number without country").fill("117779267")
    # time.sleep(2)
    # page.get_by_role("textbox", name="Email address").click()
    # page.get_by_role("textbox", name="Email address").fill("gayathrima156@gmail.com")
    # time.sleep(2)
    # page.get_by_role("textbox", name="Date of birth").click()
    # page.get_by_placeholder("Date of birth").fill("2002-02-07")
    # time.sleep(2)
    # page.get_by_role("button", name="Get OTP").click()
    # page.pause()
    # # page.get_by_role("textbox").first.click()
    # # # page.get_by_role("textbox").first.fill("2")
    # # # page.get_by_role("textbox").nth(1).fill("9")
    # # # page.get_by_role("textbox").nth(2).fill("5")
    # # # page.get_by_role("textbox").nth(3).fill("0")
    # page.get_by_role("button", name="Submit").click()
    # time.sleep(2)
    
    #document details
    
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
 
 
def upload_salary_slip(page, file_path: str):
    """Upload screen: Salary slip."""
    select_document_type(page, "SLSIP")
    page.get_by_text("Add File").first.click()
    page.locator('input[type="file"]').last.set_input_files(file_path)
    confirm_upload(page)
    
def upload_certificate_guardian(page, file_path: str):
    """Upload screen: certificate / guardian document."""
    select_document_type(page, "CTGND")
    page.get_by_role("img").nth(5).click()
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
def upload_gmap(page, file_path: str):
    """Upload screen: geo/sketch map location."""
    select_document_type(page, "GMAP")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
 
def upload_photo(page, file_path: str):
    """Upload screen: applicant photo."""
    select_document_type(page, "PHOTO")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
 
def upload_birth_certificate(page, file_path: str):
    """Upload screen: minor's birth certificate."""
    select_document_type(page, "BIRTHCER")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
def upload_child_photo(page, file_path: str):
    """Upload screen: minor/child photo."""
    select_document_type(page, "CHPHOTO")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    page.get_by_role("button", name="Done").click()
    confirm_upload(page)
 
def upload_signature(page, file_path: str):
    """Upload screen: signature."""
    page.get_by_role("combobox").select_option("SIGN")
    page.get_by_role("button", name="Add File").set_input_files(file_path)
    confirm_upload(page)
 
 
def upload_screen(page, natid, slsip, certificate_guardian, gmap, photo, birth_cert, child_photo, signature):
    """Runs the full upload screen for all required Minors/ITF documents, in order."""
    upload_national_id(page, natid)
    upload_salary_slip(page, slsip)
    upload_certificate_guardian(page, certificate_guardian)
    upload_gmap(page, gmap)
    upload_photo(page, photo)
    upload_birth_certificate(page, birth_cert)
    upload_child_photo(page, child_photo)
    upload_signature(page, signature)
    page.get_by_role("button", name="Continue").click()    
    
    #aplication details
    
def application_details_page(page, account_number, id_number, otp_value, title,
                               first_name, last_name, marital_status, employment_status,
                               guardian_first_name, guardian_last_name, guardian_dob,
                               business_activity, net_income, region, village_area,
                               home_village, district, bank_code, residential_address,
                               street, issue_date, expiry_date, security_question,
                               security_answer, utility_type, utility_number,
                               name_on_utility_bill, kin_first_name, kin_last_name,
                               kin_relationship, kin_mobile):
    """Minors/ITF application details page: account, applicant, guardian,
    address, security, utility, and kin/relationship details."""
    page.get_by_role("spinbutton", name="Account Number *").click()
    page.get_by_role("spinbutton", name="Account Number *").fill(account_number)
    page.get_by_role("textbox", name="ID Number *").first.click()
    page.get_by_role("textbox", name="ID Number *").first.fill(id_number)
    page.get_by_role("button", name="Ok").click()
    page.get_by_role("spinbutton", name="OTP *").fill("12345")
    page.get_by_role("textbox").nth(2).click()
    page.get_by_role("button", name="Ok").click()
 
    page.get_by_role("textbox").nth(2).click()
    page.get_by_role("option", name=title).click()
 
    page.get_by_role("textbox", name="First Name *").first.click()
    page.get_by_role("textbox", name="First Name *").first.fill(first_name)
    page.get_by_role("textbox", name="Last Name *").first.click()
    page.get_by_role("textbox", name="Last Name *").first.fill(last_name)
 
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=marital_status).click()
 
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_text(employment_status).click()
 
    # Guardian details
    page.get_by_role("textbox", name="First Name *").nth(1).click()
    page.get_by_role("textbox", name="First Name *").nth(1).fill(guardian_first_name)
    page.get_by_role("textbox", name="Last Name *").nth(1).click()
    page.get_by_role("textbox", name="Last Name *").nth(1).fill(guardian_last_name)
    page.get_by_role("textbox", name="Date of Birth *", exact=True).fill(guardian_dob)
 
    page.get_by_role("textbox", name="Business Activity *").click()
    page.get_by_role("textbox", name="Business Activity *").fill(business_activity)
    page.get_by_role("textbox", name="Net Monthly Income *").click()
    page.get_by_role("textbox", name="Net Monthly Income *").fill(net_income)
 
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=region).click()
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=village_area).click()
 
    page.get_by_role("textbox", name="Home Village *").click()
    page.get_by_role("textbox", name="Home Village *").fill(home_village)
 
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_text(district).click()
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_role("option", name=bank_code).click()
 
    page.get_by_role("textbox", name="Residential Physical Address").click()
    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_address)
    page.locator("div:nth-child(2) > input").first.click()
    page.get_by_text(street).click()
 
    page.get_by_role("textbox", name="Issue Date *").fill(issue_date)
    page.get_by_role("textbox", name="Expiry Date *").fill(expiry_date)
 
    security_question_dropdown = page.locator(
        ".application_select.ng-select-searchable.ng-select-clearable.ng-select.ng-select-single.ng-untouched.ng-pristine.ng-invalid"
    ).first
    security_question_dropdown.click()
    page.get_by_role("option", name=security_question).click()
    page.get_by_role("textbox", name="Security Answer *").click()
    page.get_by_role("textbox", name="Security Answer *").fill(security_answer)
 
    utility_type_dropdown = page.locator(
        ".application_select.ng-select-searchable.ng-select-clearable.ng-select.ng-select-single.ng-untouched.ng-pristine.ng-invalid > .ng-select-container > .ng-arrow-wrapper"
    ).first
    utility_type_dropdown.click()
    page.get_by_role("option", name=utility_type).click()
    page.get_by_role("textbox", name="Utility Number *").click()
    page.get_by_role("textbox", name="Utility Number *").fill(utility_number)
    page.get_by_role("textbox", name="Name on Utility Bill *").click()
    page.get_by_role("textbox", name="Name on Utility Bill *").fill(name_on_utility_bill)
 
    # Kin details - dynamic IDs, same caveat as other flows (confirm stability with Ezhil)
    page.locator("#acDezgKwh2ptT6jN").click()
    page.locator("#acDezgKwh2ptT6jN").fill(kin_first_name)
    page.locator("#ldTj6SxIQ0TKFscK").click()
    page.locator("#ldTj6SxIQ0TKFscK").fill(kin_last_name)
    page.locator("#OeCBgdtTtWsJamXv > .ng-select-container > .ng-arrow-wrapper").click()
    page.get_by_role("option", name=kin_relationship).click()
    page.get_by_role("textbox", name="Mobile number without country").nth(2).click()
    page.get_by_role("textbox", name="Mobile number without country").nth(2).fill(kin_mobile)
 
    page.get_by_role("button", name="Continue").click()    
   
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
 
    mobile_number = get_malawi_phone()
    kin_mobile_number = "+265" + get_malawi_phone()
    email = fake.email() 
    dob_adult = fake.date_of_birth(minimum_age=18, maximum_age=80)
    
 
    landing_page(page, product_section="Retail Accounts", product_name="Minors / ITF Account")
    page.get_by_text("Signature Document").click()
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile=mobile_number, email=email, dob=dob_adult)
    otp_page(page)

    page.get_by_text("Signature Document").click()
    
 
    
 
    upload_screen(
        page,
        natid_front="front_image.jpeg",
        natid_back="backside_image.jpeg",
        certificate_guardian="front_image.jpeg",
        gmap="front_image.jpeg",
        photo="front_image.jpeg",
        birth_cert="front_image.jpeg",
        child_photo="front_image.jpeg",
        signature="front_image.jpeg",
    )
 
    application_details_page(
        page,
        account_number="1004567289",
        id_number="12354w",
        otp_value="12345",
        title="MISS",
        first_name=fake.first_name().upper(),
        last_name=fake.last_name().upper(),
        marital_status="Single",
        employment_status="Self Employed",
        guardian_first_name=fake.first_name().upper(),
        guardian_last_name=fake.last_name().upper(),
        guardian_dob="2024-02-14",
        business_activity="ACCOUNTER",
        net_income="90,0000",
        region="Blantyre",
        village_area="Kunthembwe",
        home_village="27KUNTHEMBWE",
        district="BLANTYRE URBAN",
        bank_code="BCA",
        residential_address="HOUSE20",
        street="CUSTOMS ROAD",
        issue_date="2025-01-07",
        expiry_date="2035-10-25",
        security_question="Last 4 digits of your Nat. ID?",
        security_answer="8765",
        utility_type="City/Ground Rates",
        utility_number="5432",
        name_on_utility_bill="TEST",
        kin_first_name=fake.first_name().upper(),
        kin_last_name=fake.last_name().upper(),
        kin_relationship="Sibling",
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
