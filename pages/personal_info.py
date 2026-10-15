import time

def personal_info_page(page, mobile, email, dob):
    """Personal info page: mobile number, email, date of birth, then trigger OTP."""
    page.get_by_role("textbox", name="Mobile number without country").click()
    page.get_by_role("textbox", name="Mobile number without country").fill(mobile)
    time.sleep(2)
    page.get_by_role("textbox", name="Email address").click()
    page.get_by_role("textbox", name="Email address").fill(email)#email
    time.sleep(2)
    page.get_by_placeholder("Date of birth").click()
    page.get_by_placeholder("Date of birth").fill(dob)#dob
    time.sleep(2)
    page.get_by_role("button", name="Get OTP").click()
    time.sleep(5)