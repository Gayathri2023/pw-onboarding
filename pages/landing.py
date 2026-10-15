import time

def landing_page(page,product_section,product_name):
    """Landing page: select product section, product name, and confirm document type."""
    page.goto("https://digidobuat.ndayesa.co.mw/#/",wait_until="domcontentloaded")
    page.get_by_role("button", name=product_section).click()
    page.get_by_role("heading", name=product_name).click()
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)