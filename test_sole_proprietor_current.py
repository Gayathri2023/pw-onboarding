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
    # page.get_by_role("heading", name="SME Accounts").click()
    # page.get_by_role("heading", name="Sole Proprietor Current").click()
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
    # page.get_by_role("textbox", name="Mobile number without country").click()
    # page.get_by_role("textbox", name="Mobile number without country").fill("117709346")
    # time.sleep(2)
    # page.get_by_role("textbox", name="Email address").click()
    # page.get_by_role("textbox", name="Email address").fill("gayathrima156@gmail.com")
    # time.sleep(2)
    # page.get_by_role("textbox", name="Date of incorporation").click()
    # page.get_by_placeholder("Date of incorporation").fill("2002-02-14")
    # time.sleep(2)
    # page.get_by_role("button", name="Get OTP").click()
    # page.pause()
    # # page.get_by_role("textbox").first.click()
    # # page.get_by_role("textbox").first.fill("4")
    # # page.get_by_role("textbox").nth(1).fill("8")
    # # page.get_by_role("textbox").nth(2).fill("9")
    # # page.get_by_role("textbox").nth(3).fill("4")
    # page.get_by_role("button", name="Submit").click()
    # time.sleep(2)
    
    #document page       
def select_document_type(page, doc_type: str):
    """Select the document type in the upload dropdown
    (NATID, PHOTO, SIGN, GMAP, CTGND, REG.CERTIFICATE)."""
    dropdown = page.get_by_role("combobox").first
    dropdown.wait_for(state="visible")
    dropdown.select_option(doc_type)
 
 
def confirm_upload(page, ignore_warning: bool = False):
    """Click 'Done' and dismiss the 'Ignore' warning if one appears."""
    page.get_by_role("button", name="Done").click()
    if ignore_warning:
        page.get_by_role("button", name="Ignore").click()
 
 
def upload_national_id(page, front_file: str, back_file: str):
    """Upload screen: National ID (front + back)."""
    select_document_type(page, "NATID")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(front_file)
    confirm_upload(page, ignore_warning=True)
 
    page.get_by_role("button", name="Choose File").set_input_files(back_file)
    confirm_upload(page, ignore_warning=True)
 
 
def upload_photo(page, file_path: str):
    """Upload screen: passport-style photo."""
    select_document_type(page, "PHOTO")
    page.get_by_text("Add File").first.click()
    page.get_by_text("Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
 
def upload_signature(page, file_path: str):
    """Upload screen: signature."""
    select_document_type(page, "SIGN")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
 
def upload_gmap(page, file_path: str):
    """Upload screen: geo/sketch map location."""
    select_document_type(page, "GMAP")
    page.locator(".deskViewShow").first.click()
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
def upload_certificate_guardian(page, file_path: str):
    """Upload screen: certificate / guardian document."""
    select_document_type(page, "CTGND")
    page.get_by_role("button", name="Add File").first.set_input_files(file_path)
    confirm_upload(page)
 
def upload_registration_certificate(page, file_path: str):
    """Upload screen: business registration certificate."""
    select_document_type(page, "REG.CERTIFICATE")
    page.get_by_role("button", name="Add File").set_input_files(file_path)
    confirm_upload(page)
 
def upload_screen(page, natid_front, natid_back, photo, signature, gmap, certificate_guardian,
                   registration_certificate):
    """Runs the full upload screen for all required Sole Proprietor Current documents, in order."""
    upload_national_id(page, natid_front, natid_back)
    upload_photo(page, photo)
    upload_signature(page, signature)
    upload_gmap(page, gmap)
    upload_certificate_guardian(page, certificate_guardian)
    upload_registration_certificate(page, registration_certificate)
    page.get_by_role("button", name="Continue").click()
  
    # page.get_by_role("combobox").first.select_option("NATID")
    # page.get_by_text("Add File").first.click()
    # page.get_by_text("Add File").first.set_input_files("WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg")
    # page.get_by_role("button", name="Done").click()
    # page.get_by_role("button", name="Ignore").click()
    # page.get_by_role("button", name="Choose File").set_input_files("WhatsApp Image 2025-07-30 at 11.29.00 AM (1).jpeg")
    # page.get_by_role("button", name="Done").click()
    # page.get_by_role("button", name="Ignore").click()
    # page.get_by_role("combobox").first.select_option("PHOTO")
    # page.get_by_text("Add File").first.click()
    # page.get_by_text("Add File").first.set_input_files("WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg")
    # page.get_by_role("button", name="Done").click()
    # page.get_by_role("combobox").first.select_option("SIGN")
    # page.get_by_role("button", name="Add File").first.set_input_files("WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg")
    # page.get_by_role("button", name="Done").click()
    # page.get_by_role("combobox").first.select_option("GMAP")
    # page.locator(".deskViewShow").first.click()
    # page.get_by_role("button", name="Add File").first.set_input_files("WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg")
    # page.get_by_role("combobox").first.select_option("CTGND")
    # page.get_by_role("button", name="Add File").first.set_input_files("WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg")
    # page.get_by_role("combobox").select_option("REG.CERTIFICATE")
    # page.get_by_role("button", name="Add File").set_input_files("WhatsApp Image 2025-07-30 at 11.28.59 AM (2).jpeg")
    # page.get_by_role("button", name="Continue").click()
    
    #application page
def business_details_page(page, residence_location, registration_number, postal_address,
                           physical_address, mobile_business, residential_physical_address,
                           business_type, source_of_capital, num_employees, annual_turnover,
                           contact_name, contact_designation, mobile_contact, contact_dob,
                           id_number, start_date, expiry_date, postal_code):
    """Application details page: business, registration, and contact-person details."""
    page.goto("https://localhost:8080/#/applicationdetail")
 
    # Page assertion: confirm navigation landed correctly before filling the form.
    expect(page).to_have_url(re.compile(r".*/applicationdetail"))
 
    page.get_by_role("textbox", name="Residence/Business Location *").fill(residence_location)
    page.get_by_role("textbox", name="Registration Number *").fill(registration_number)
    page.get_by_role("textbox", name="Postal Address *").fill(postal_address)
    page.get_by_role("textbox", name="Physical Address *").fill(physical_address)
 
    mobile_fields = page.get_by_role("textbox", name="Mobile number without country")
    mobile_fields.first.fill(mobile_business)
 
    page.get_by_role("textbox", name="Residential Physical Address").fill(residential_physical_address)
    page.get_by_role("textbox", name="Type of Business / Business").fill(business_type)
    page.get_by_role("textbox", name="Source of Capital *").fill(source_of_capital)
    page.get_by_role("spinbutton", name="Number of Employees *").fill(num_employees)
    page.get_by_role("textbox", name="Expected Annual Turnover *").fill(annual_turnover)
 
    
    page.locator("#lIAtgZ0zwCN4smCh").fill(contact_name)
    page.locator("#T9PTuER0zqwstqAZ").fill(contact_designation)
 
    mobile_fields.nth(4).fill(mobile_contact)
 
    page.locator("#nzovlwLggNEiHEJp").fill(contact_dob)
    page.locator("#g7xz9QeKlzn0uez1").fill(id_number)
 
    date_fields = page.locator("input[type=\"date\"]")
    date_fields.nth(2).fill(start_date)
    date_fields.nth(3).fill(expiry_date)
 
    page.locator("#Nbl4tVZIafAsQI1S").fill(postal_code)
    page.get_by_role("button", name="Continue").click()
    
    # page.goto("https://localhost:8080/#/applicationdetail")
    # page.get_by_role("textbox", name="Residence/Business Location *").fill("MALAWI")
    # page.get_by_role("textbox", name="Registration Number *").fill("54321")
    # page.get_by_role("textbox", name="Postal Address *").fill("BOX10")
    # page.get_by_role("textbox", name="Physical Address *").fill("BANWE")
    # page.get_by_role("textbox", name="Mobile number without country").first.fill("+265117793456")
    # page.get_by_role("textbox", name="Residential Physical Address").fill("CHIRADZULU NEAR")
    # page.get_by_role("textbox", name="Type of Business / Business").fill("SALES OF BIKES")
    # page.get_by_role("textbox", name="Source of Capital *").fill("LOAN")
    # page.get_by_role("spinbutton", name="Number of Employees *").fill("30")
    # page.get_by_role("textbox", name="Expected Annual Turnover *").fill("70,0000")
    # page.locator("#lIAtgZ0zwCN4smCh").fill("USHA")
    # page.locator("#T9PTuER0zqwstqAZ").fill("CEO")
    # page.get_by_role("textbox", name="Mobile number without country").nth(4).fill("+265117229834")
    # page.locator("#nzovlwLggNEiHEJp").fill("1996-02-14")
    # page.locator("#g7xz9QeKlzn0uez1").fill("TEST1234")
    # page.locator("input[type=\"date\"]").nth(2).fill("2019-01-08")
    # page.locator("input[type=\"date\"]").nth(3).fill("2030-06-14")
    # page.locator("#Nbl4tVZIafAsQI1S").fill("12345")
    # page.goto("https://localhost:8080/#/integration")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        permissions=["camera", "microphone", "geolocation"],
        geolocation={"latitude": 12.9716, "longitude": 77.5946},
        locale="en-US",
    )
 
    mobile_number = get_malawi_phone()
    mobile_business = "+265" + get_malawi_phone()
    mobile_contact = "+265" + get_malawi_phone()
    email = fake.email() 
    dob_adult = fake.date_of_birth(minimum_age=18, maximum_age=80)
 
    page = context.new_page()
 
    landing_page(page, product_section="SME Accounts", product_name="Sole Proprietor Current")
    consent_page(page)
    eligibility_page(page)
    personal_info_page(page, mobile=mobile_number, email=email, dob=dob_adult)
    otp_page(page)
 
    upload_screen(
        page,
        natid_front="front_image.jpeg",
        natid_back="backside_image.jpeg",
        photo="front_image.jpeg",
        signature="front_image.jpegg",
        gmap="front_image.jpeg",
        certificate_guardian="front_image.jpeg",
        registration_certificate="front_image.jpeg",
    )
 
    business_details_page(
        page,
        residence_location="MALAWI",
        registration_number=str(fake.random_int(min=10000, max=99999)),
        postal_address=f"BOX{fake.random_int(min=1, max=999)}",
        physical_address=fake.city().upper(),
        mobile_business=mobile_business,
        residential_physical_address=fake.street_address().upper(),
        business_type="SALES OF BIKES",
        source_of_capital="LOAN",
        num_employees=str(fake.random_int(min=1, max=100)),
        annual_turnover="70,0000",
        contact_name=fake.first_name().upper(),
        contact_designation="CEO",
        mobile_contact=mobile_contact,
        contact_dob="1996-02-14",
        id_number="TEST" + str(fake.random_int(min=1000, max=9999)),
        start_date="2019-01-08",
        expiry_date="2030-06-14",
        postal_code=str(fake.random_int(min=10000, max=99999)),
    )
 
    recording_page(page)
    preview_page(page)
    finalize_application(page)
 
    time.sleep(2)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
