from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Browser:
    """
    Browser class for scraping using a Chrome test browser
    """

    driver = None

    def __init__(self, email: str):
        """
        Starts browser and logs in to MercadoLibre
        """

        # Browser config
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
        options.add_argument("start-maximized")  # ensure window is full-screen

        # Init browser
        driver = webdriver.Chrome(options=options)
        self.driver = driver
        print("Browser inited")

        # Log in
        driver.get("https://www.mercadolibre.com/jms/mlv/lgz/msl/login/")
        input_box = driver.find_element(By.CSS_SELECTOR, 'input[name="user_id"]')
        input_box.send_keys(email)
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].login-form__submit')
        login_button.click()

        # Wait for recaptcha
        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))
        )
        print("Resuelva el Captcha en pantalla")
        time.sleep(100)

        # Wait for challenges section
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.challenge-options__container'))
        )

        # Select Google authenticator challenge
        gauth_button = driver.find_element(By.CSS_SELECTOR, 'li#totp > button.andes-list__item-action')
        gauth_button.click()

        # Wait for OTP input
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
        )

        # Input value received from terminal
        otp_code = input("Ingrese el código OTP de Google Authenticator: ")
        otp_inputs = driver.find_elements(By.CSS_SELECTOR, 'input.andes-form-control__field')
        for code_val, input_field in list(zip(otp_code, otp_inputs)):
            input_field.send_keys(code_val)
        confirm_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        confirm_button.click()

        # Wait for login success
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dynamic-access-card-item__item-description'))
        )


    def get_response_text(self, url: str):
        """
        Returns text content of a page from its URL
        """
        
        self.driver.get(url)
        return self.driver.page_source        
