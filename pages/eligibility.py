import time

def eligibility_page(page):
    """Eligibility page: select the required radio options and confirmation checkboxes."""
    page.get_by_role("radio").first.check()
    page.get_by_role("radio").nth(2).check()
    page.get_by_role("radio").nth(4).check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").first.check()
    page.locator(".ng-untouched.ng-pristine.ng-invalid").check()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)