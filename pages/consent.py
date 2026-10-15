import time

def consent_page(page):
    """Consent page: accept terms checkbox and continue."""
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)