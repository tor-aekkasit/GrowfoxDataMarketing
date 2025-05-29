from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TikTokPageInfo:
    def __new__(cls, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # เพิ่ม path ไปยัง chromedriver.exe
        driver_path = r"C:\Users\blackbook\Desktop\chromedriver-win64\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=driver_path, options=options)

        driver.get(url)
        time.sleep(5)

        try:
            username_text = driver.find_element(By.XPATH, '//h1[@data-e2e="user-title"]').text
            page_name_text = driver.find_element(By.XPATH, '//h2[@data-e2e="user-subtitle"]').text
            followers = driver.find_element(By.XPATH, '//strong[@data-e2e="followers-count"]').text
            likes = driver.find_element(By.XPATH, '//strong[@data-e2e="likes-count"]').text
            bio = driver.find_element(By.XPATH, '//h2[@data-e2e="user-bio"]').text
            profile_pic = driver.find_element(By.XPATH, '//img[contains(@class, "ImgAvatar")]').get_attribute("src")
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            driver.quit()
            return None

        driver.quit()
        return {
            "username": username_text,
            "page_name": page_name_text,
            "followers": followers,
            "likes": likes,
            "bio": bio,
            "profile_pic": profile_pic,
            "url": url
        }
