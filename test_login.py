import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


from selenium.common.exceptions import TimeoutException
import time 


LOGIN_URL = "http://localhost:3002/login"  


GECERLI_KULLANICI_ADI = "Judge"  
GECERLI_SIFRE = "Salih123."  
GECERSIZ_SIFRE = "salih1"


KULLANICI_ADI_INPUT = (By.ID, "username")  
SIFRE_INPUT = (By.ID, "password")  
GIRIS_YAP_BUTONU = (By.ID, "submitb")  


HATA_MESAJI_ALANI = (By.ID, "errorb")  




@pytest.fixture
def driver_wait_setup():
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    
    wait = WebDriverWait(driver, 10)

    
    driver.maximize_window()

    
    driver.get(LOGIN_URL)

   
    yield driver, wait

    
    driver.quit()




def test_basarili_giris(driver_wait_setup):
    """Geçerli kullanıcı adı ve şifre ile başarılı giriş testi."""
    
    
    driver, wait = driver_wait_setup

    try:
       
        username_input = wait.until(EC.visibility_of_element_located(KULLANICI_ADI_INPUT))
        username_input.send_keys(GECERLI_KULLANICI_ADI)

       
        password_input = driver.find_element(*SIFRE_INPUT) 
        password_input.send_keys(GECERLI_SIFRE)

       
        login_button = driver.find_element(*GIRIS_YAP_BUTONU)
        login_button.click()




        
        assert "/dashboard" in driver.current_url, "Giriş başarılı, ancak beklenen URL'e yönlenmedi."

    except TimeoutException:
       
        pytest.fail("Test zaman aşımına uğradı. Beklenen element bulunamadı.")


def test_hatali_sifre_ile_giris(driver_wait_setup):
    """Geçerli kullanıcı adı ve geçersiz şifre ile hatalı giriş testi."""
    
    driver, wait = driver_wait_setup

    try:
      
        username_input = wait.until(EC.visibility_of_element_located(KULLANICI_ADI_INPUT))
        username_input.send_keys(GECERLI_KULLANICI_ADI)

       
        password_input = driver.find_element(*SIFRE_INPUT)
        password_input.send_keys(GECERSIZ_SIFRE)

      
        login_button = driver.find_element(*GIRIS_YAP_BUTONU)
        login_button.click()

       
        error_message = wait.until(EC.visibility_of_element_located(HATA_MESAJI_ALANI))

       
        assert error_message.is_displayed(), "Hata mesajı görüntülenmedi."

       
        beklenen_hata_mesaji = "Hatalı Kullanıcı Adı veya Şifre."  
        assert error_message.text == beklenen_hata_mesaji, "Görüntülenen hata mesajı metni beklenenle aynı değil."

    except TimeoutException:
        pytest.fail("Test zaman aşımına uğradı. Hata mesajı elementi bulunamadı.")