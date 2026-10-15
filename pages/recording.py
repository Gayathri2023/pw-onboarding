import time

def recording_page(page):
    """Video recording step required before preview/submit."""
    page.get_by_role("button", name="I am Ready").click()
    page.get_by_role("button", name="Start Video Recording").click()
    page.get_by_role("button", name="End Video Recording").click()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)    