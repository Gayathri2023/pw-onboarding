import time 

def preview_page(page):
    """Preview page: confirm the Ok dialog and accept the final declaration checkbox."""
    page.goto("https://digidobuat.ndayesa.co.mw/#/preview",wait_until="domcontentloaded")
 
    page.get_by_role("checkbox").nth(1).check()
    page.locator("canvas").click(position={"x": 306, "y": 141})
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Submit").click()
    time.sleep(2)
