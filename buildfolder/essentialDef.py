
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_element(driver, t, element, clickable=False):
    target = WebDriverWait(driver, t).until(EC.visibility_of_element_located(element))
    if clickable:
        target.click()
    return target


def send_message(presetData, txt, repeat=1):
    _bot = presetData['telegramBot']
    _id = presetData['telegramChannel']
    if _bot == '':
        print('텔레그램 없음] ', txt)
    else:
        url = "https://api.telegram.org/bot"
        for _ in range(0, repeat):
            r = requests.get(url+_bot+'/sendMessage?chat_id='+_id+"&text="+txt)
            print(r)


def checkAlert(driver, delay_t=.4):
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())  # 알림 창이 나타날 때까지 대기
        alert = driver.switch_to.alert
        alertText = alert.text
        print(alertText)
        
        alert.accept()
        time.sleep(delay_t)
        if ("확인해주세요" in alertText):
            # 단일 등급이 아닌 곳에서 뜨는 알림 선택하신 좌석등급과 가격이 맞는지 확인해주세요.
            return False
        else:
            return True
    except Exception as e:
        return False
