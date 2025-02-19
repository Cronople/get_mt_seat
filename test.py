import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from recognize_word import recognizing

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('user-data-dir=C:\\user_data\\user')
driver = webdriver.Chrome(options=chrome_options)




def wait_element(t, element, clickable = False):
    WebDriverWait(driver, t).until(EC.visibility_of_element_located(element))
    if clickable:
        driver.find_element(element[0], element[1]).click()


def checkAlert():
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())  # 알림 창이 나타날 때까지 대기
        alert = driver.switch_to.alert
        print(alert.text)
        alert.accept()
        time.sleep(.2)
        return True
    except Exception as e:
        return False


def find_seat():
    didAlert = 0
    # JavaScript 코드 실행
    seats = driver.execute_script("""
        const ezCanvas = document.getElementById('ez_canvas');
        const rectElements = ezCanvas.querySelectorAll('rect'); // rect 요소 선택
        const notDdddElements = [];

        rectElements.forEach(rect => {
            const fillValue = rect.getAttribute('fill');
            if (fillValue && fillValue !== '#DDDDDD' && fillValue !== 'none') {
                notDdddElements.push(rect);
            }
        });

        return notDdddElements;
    """)
    
    # 찾은 요소들을 활용하여 Selenium 작업 수행 (예: 클릭, 텍스트 가져오기 등)
    for seat in seats:
        # 예시: 특정 fill 값을 가진 요소 클릭
        print('구역 내 좌석 수:', len(seats))
        print('[좌석선택]', seat.get_attribute('x'), seat.get_attribute('y'))
        seat.click()
        driver.find_element(by=By.ID, value='nextTicketSelection').click()
        if checkAlert():
            find_seat()
            didAlert = 2 # 좌석 찾음, 이선좌로 알람발생
            break
        else:
            return 1 # 좌석 찾음, 알람 없음
    if len(seats) == 0:
        print('구역 내 좌석 없음.')
    return didAlert # 0의 경우 좌석 없음


idpwFile = open('idpw.txt', 'r')
_ID = idpwFile.readline()
_PW = idpwFile.readline()
idpwFile.close()

# 웹페이지 해당 주소 이동
# driver.get("https://ticket.melon.com/performance/index.htm?prodId=210962")210876
driver.get("https://ticket.melon.com/performance/index.htm?prodId=210876")

wait_element(5, (By.ID, 'global_top_ticketLogin_Button'), clickable=True)
wait_element(5, (By.XPATH, '//*[@id="conts_section"]/div/div/div[1]/button'), clickable=True)
time.sleep(2) # 대기하며 로그인 창이 유지되는지 확인

if len(driver.window_handles) > 1: #로그인 정보가 없을 때
    driver.switch_to.window(driver.window_handles[1])
    wait_element(5, (By.ID, 'loginId--1'))
    driver.find_element(By.ID, 'loginId--1').send_keys(_ID)
    driver.find_element(By.ID, 'password--2').send_keys(_PW)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
    #input('카카오 로그인 인증을 완료 한 후 아무 문자와 함께 엔터: ')
else:
    print('기존 로그인 정보로 로그인 완료')

print(driver.window_handles)
driver.switch_to.window(driver.window_handles[0])

# ID - box_list_date : 날짜 선택 리스트, item_date: 날짜
time.sleep(3)
wait_element(5, (By.ID, 'box_list_date'))
date_list = driver.find_element(by=By.ID, value='box_list_date')
dates = date_list.find_elements(by=By.CLASS_NAME, value='item_date')
print('-------box_list_date-------')
for i, e in enumerate(dates):
    print(i,'] ', e.text)
print('---------------------------')

# 나중에 클릭할 날짜 선정, 일단 첫 날짜로
dates[0].click()
time.sleep(.5) # 너무 빠르면 시간 선택 오류 발생
# ID - ticketReservation_Btn : 예매하기 버튼
driver.find_element(by=By.ID, value='ticketReservation_Btn').click()


time.sleep(1)
print(driver.window_handles)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[1])

# 보안코드 입력 성공했는지 체크하는 네트워크 판단 기능
time.sleep(1)
#ID - label-for-captcha : 캡챠 적는 란

captcha_word = ''
#captchaImg = driver.find_element(By.ID, 'captchaImg')
#captcha_word = recognizing(captchaImg.get_attribute('src'))
driver.find_element(By.ID, 'label-for-captcha').send_keys(captcha_word)
driver.find_element(by=By.XPATH, value='//*[@id="btnComplete"]').click()
input('보안문자 입력 완료: ')

try:
    # iframe으로 전환 (반드시 필요)
    iframe = WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "oneStopFrame"))
    )
    print('iframe 전환 완료')
    
    # 좌석 등급 펼치기
    sector_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#divGradeSummary")) # CSS Selector 사용
    )
    print('구역 요소 찾음')
    if len(sector_elements) == 1:
        sector_element = sector_elements[0]
    else:
        for i, e in enumerate(sector_elements):
            print(i, '] ', e)
        grade = input('원하는 등급에 해당하는 숫자를 적고 엔터: ')
        sector_element = sector_elements[grade]
    print(sector_element.text, ' 구역 요소 확장')
    sector_element.click()
    time.sleep(.5)

    # "list_area listOn" 클래스 아래의 모든 <li> 요소 찾기
    seat_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list_area.listOn li"))
    )
    for i, e in enumerate(seat_elements):
        print(i, '] ', e.text)
    
    focus_sector = input('조사 구역을 번호로 적어주세요: ')
    if ',' in focus_sector:
        focus_sector = focus_sector.split(',')
    else:
        focus_sector = focus_sector.split()
    focus_sector_list = list(map(int, focus_sector))
    print('조사할 구역')
    for e in focus_sector_list:
        print(seat_elements[e].text)
    
    for i in focus_sector_list:
        seat_elements[i].click()
        didAlert = find_seat()
        if didAlert == 1: # 좌석 잡음
            break
        elif didAlert == 2: # 이선좌로 알람 발생
            sector_element.click()
            seat_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list_area.listOn li"))
                )
        time.sleep(.5)

    # 좌석 정보
    ticket_info_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".txt_ticket_info"))
    )
    seat_info = ticket_info_element.text

    # 티켓 매수 선택
    select_elements = driver.find_elements(By.ID, 'volume_10009_10067')

    if select_elements:  # 선택창 확인
        select_element = select_elements[0]
        select = Select(select_element)
        select.select_by_index(1)




    print(seat_info)
    # 가격 선택 창에서 다음 버튼
    wait_element(5, (By.ID, 'nextPayment'), True)
    driver.switch_to.default_content() # iframe에서 빠져나오기

except Exception as e:
    print(f"3오류 발생: {e}")