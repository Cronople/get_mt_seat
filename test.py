import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('user-data-dir=C:\\user_data\\user')
driver = webdriver.Chrome(options=chrome_options)

def wait_element(t, element, clickable = False):
    WebDriverWait(driver, t).until(EC.visibility_of_element_located(element))
    if clickable:
        driver.find_element(element[0], element[1]).click()

idpwFile = open('idpw.txt', 'r')
_ID = idpwFile.readline()
_PW = idpwFile.readline()
idpwFile.close()

# 웹페이지 해당 주소 이동
driver.get("https://ticket.melon.com/performance/index.htm?prodId=210962")


wait_element(5, (By.ID, 'global_top_ticketLogin_Button'), clickable=True)
wait_element(5, (By.XPATH, '//*[@id="conts_section"]/div/div/div[1]/button'), clickable=True)
time.sleep(3) # 대기하며 로그인 창이 유지되는지 확인

if len(driver.window_handles) > 1: #로그인 정보가 없을 때
    driver.switch_to.window(driver.window_handles[1])
    wait_element(5, (By.ID, 'loginId--1'))
    driver.find_element(By.ID, 'loginId--1').send_keys(_ID)
    driver.find_element(By.ID, 'password--2').send_keys(_PW)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
    input('카카오 로그인 인증을 완료 한 후 아무 문자와 함께 엔터: ')
else:
    print('기존 로그인 정보로 로그인 완료')

# ID - box_list_date : 날짜 선택 리스트, item_date: 날짜
date_list = driver.find_element(by=By.ID, value='box_list_date')
dates = date_list.find_elements(by=By.CLASS_NAME, value='item_date')
print('-------box_list_date-------')
for i, e in enumerate(dates):
    print(i,'] ', e.text)
print('---------------------------')

# 나중에 클릭할 날짜 선정, 일단 첫 날짜로
dates[0].click()
time.sleep(1) # 너무 빠르면 시간 선택 오류 발생
# ID - ticketReservation_Btn : 예매하기 버튼
driver.find_element(by=By.ID, value='ticketReservation_Btn').click()


time.sleep(1)
print(driver.window_handles)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[1])

# 보안코드 입력 성공했는지 체크하는 네트워크 판단 기능
time.sleep(1)
input('보안코드 입력 완료: ')
#driver.find_element(by=By.XPATH, value='//*[@id="btnComplete"]').click()

#ID - iez_canvas: 좌석도 우상단 표시
#ID - ez_canvas : 좌석 표시
#li10009FLOORF1, li10009FLOORF2
#li10009FLOORF3, li10009FLOORF4, li10009FLOORF5
#time.sleep(3)
#driver.find_element(by=By.XPATH, value='//*[@id="gd10009"]/td[4]').click()

###########################################################################################
iframe = driver.find_element(by=By.XPATH, value='//*[@id="oneStopFrame"]')
driver.switch_to.frame(iframe)

time.sleep(3)
F_third = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/div[1]/div/div[1]/div[1]/div/svg/path[74]')
F_fourth = driver.find_element(by=By.XPATH, value='//*[@id="iez_canvas"]/svg/path[75]')
F_fifth = driver.find_element(by=By.XPATH, value='//*[@id="iez_canvas"]/svg/path[76]')
print('가능??')
time.sleep(3)
F_third.click()
time.sleep(3)
F_fourth.click()
time.sleep(3)
F_fifth.click()