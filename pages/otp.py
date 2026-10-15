from pydoc import pager
import re
import time
from utils.test_db_connection import test_get_otp

def otp_page(page,email,mobile_number):
    print("inside_otp_page")
    """OTP page: Enter the 4-digit OTP and submit."""
    otp = test_get_otp(email=email,mobile=mobile_number)
    otp_boxes = page.get_by_role("textbox")
    otp_boxes.first.click()

    for i in range(4):
        otp_boxes.nth(i).clear()
        otp_boxes.nth(i).fill(otp[i])
        page.keyboard.press("Tab")
    time.sleep(2)
    page.pause()
    
    submit_btn = page.get_by_role("button", name=re.compile("submit", re.I))
    submit_btn.wait_for(state="visible")
    submit_btn.click()
    
