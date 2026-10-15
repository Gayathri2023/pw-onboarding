def finalize_application(page):
    """Final page: pause for manual checks, then navigate to the integration step."""
    print("⚡ Please input manually if required...")
    page.pause()
    print("⚡ Automation continuing...")

    page.goto("https://digidobuat.ndayesa.co.mw/#/integration",wait_until="domcontentloaded")
    page.get_by_role("button", name="Ok").click()
    print("✅ Script completed successfully!")