import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('user-data-dir=C:\\user_data\\user')

driver = webdriver.Chrome(options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://ticket.melon.com/performance/index.htm?prodId=210962")

#input('로그인 정보를 입력 후, 준비가 되면 아무 버튼 클릭 후 엔터: ')
time.sleep(2)
driver.find_element(by=By.ID, value='global_top_ticketLogin_Button').click()
time.sleep(3)
driver.find_element(by=By.XPATH, value='//*[@id="conts_section"]/div/div/div[1]/button').click()
time.sleep(2)
'''
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[1])
else:
    print('error! 카카오 로그인 창 뜨지 않음')

time.sleep(3)
kko_id = driver.find_element(by=By.ID, value='loginId--1')
kko_pw = driver.find_element(by=By.ID, value='password--2')
kko_id.send_keys(ID)
kko_pw.send_keys(PW)
driver.find_element(by=By.XPATH, value='//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
time.sleep(3)
'''

# ID - box_list_date : 날짜 선택 리스트, item_date: 날짜
date_list = driver.find_element(by=By.ID, value='box_list_date')
dates = date_list.find_elements(by=By.CLASS_NAME, value='item_date')
print('-------box_list_date-------')
for e in dates:
    print(e.text)
print('---------------------------')

# 나중에 클릭할 날짜 선정, 일단 첫 날짜로
dates[0].click()
time.sleep(1)
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
