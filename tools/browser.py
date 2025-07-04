from playwright.sync_api import sync_playwright
import time

def browse(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # يمكنك تعيين False إذا تعمل مع XServer
        page = browser.new_page()
        page.goto(url)
        print("✅ تم فتح الصفحة:", page.title())
        time.sleep(5)  # لتجنب الإغلاق الفوري
        browser.close()

