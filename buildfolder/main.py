import time
import requests
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from recognize_word import recognizing
from preset import getPreset

chrome_options = Options()
user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
chrome_options.add_argument("user-agent="+user_agent)
chrome_options.add_experimental_option("detach", True)
os = platform.system()
if os == 'Windows':
    chrome_options.add_argument('user-data-dir=C:\\user_data\\user')
elif os == 'Darwin': # Mac
    pass
elif os == 'Linux':
    pass
driver = webdriver.Chrome(options=chrome_options)


def send_message(_bot, _id, txt, repeat=1):
    if _bot == '':
        print('텔레그램 없음] ', txt)
    else:
        url = "https://api.telegram.org/bot"
        for i in range(0, repeat):
            r = requests.get(url+_bot+'/sendMessage?chat_id='+_id+"&text="+txt)
            print(r)


def wait_element(t, element, clickable=False):
    target = WebDriverWait(driver, t).until(EC.visibility_of_element_located(element))
    if clickable:
        target.click()
    return target


def checkAlert():
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())  # 알림 창이 나타날 때까지 대기
        alert = driver.switch_to.alert
        print(alert.text)
        alert.accept()
        time.sleep(.4)
        return True
    except Exception as e:
        return False


def login(_platform, _id, _pw):
    try:
        wait_element(10, (By.ID, 'global_top_ticketLogin_Button'), clickable=True)
        if _platform in '카카오멜론티켓KAKAOMELONKakaoMelonkakaomelon':
            if _platform in '카카오KAKAOKakaokakao':
                print('카카오 로그인')
                wait_element(5, (By.XPATH, '//*[@id="conts_section"]/div/div/div[1]/button'), clickable=True)
                time.sleep(2)  # 대기하며 로그인 창이 유지되는지 확인

                if len(driver.window_handles) > 1:  # 로그인 정보가 없을 때
                    driver.switch_to.window(driver.window_handles[1])
                    wait_element(5, (By.ID, 'loginId--1'))
                    wait_element(5, (By.ID, 'label-saveSignedIn'), True)
                    driver.find_element(By.ID, 'loginId--1').send_keys(_id)
                    driver.find_element(By.ID, 'password--2').send_keys(_pw)
                    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
                    time.sleep(3)
                    if len(driver.window_handles) > 1:
                        input('카카오 로그인 인증을 완료 한 후 아무 문자와 함께 엔터: ')
                else:
                    print('기존 로그인 정보로 로그인 완료')
                driver.switch_to.window(driver.window_handles[0])
            else: # 멜론 로그인
                print('멜론 로그인')
                wait_element(5, (By.XPATH, '//*[@id="conts_section"]/div/div/div[2]/button'), clickable=True)
                wait_element(5, (By.ID, 'id'))
                driver.find_element(By.ID, 'id').send_keys(_id)
                driver.find_element(By.ID, 'pwd').send_keys(_pw)
                driver.find_element(By.ID, 'btnLogin').click()
                time.sleep(3)
        else:
            print('idpw.txt 3번째 줄에 카카오,멜론티켓,KAKAO,MELON,Kakao,Melon,kakao,melon 중에 하나를 적어주세요')
    except Exception as e:
        send_message(_T_BOT, _T_ID, '로그인 오류 발생')
        print(f"로그인 오류 발생: {e}")


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
        seat.click()
        driver.find_element(by=By.ID, value='nextTicketSelection').click()
        print('*'*20)
        print('구역 내 좌석 수:', len(seats))
        print('[좌석선택]', seat.get_attribute('x'), seat.get_attribute('y'))
        if checkAlert():
            didAlert = find_seat()
            if didAlert != 1:
                didAlert = 2  # 좌석 찾음, 이선좌로 알람발생
            break
        else:
            return 1  # 좌석 찾음, 알람 없음
    if len(seats) == 0:
        pass
        # print('구역 내 좌석 없음.')
    return didAlert  # 0의 경우 좌석 없음


def checkAvailable():
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "inner-btn")))
        driver.close()
        print('예매창 오류로 대기 (30초)')
        time.sleep(30)
        driver.switch_to.window(driver.window_handles[0])
        return False
    except:
        return True


def checkCaptcha():  # display: none or block에 따라 확인
    try:
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "certification"))
        )
        style = element.get_attribute("style")
        if style:  # style 속성이 존재하는 경우에만 확인
            return not ("display: none" in style)  # display:block 상태
        else:
            return False  # style 속성이 없는 경우
    except:  # element를 찾을 수 없는 경우
        return False  # 보안창이 없으므로 패스
    

def searchSeats():
    get_seat = False
    # iframe으로 전환 (반드시 필요)
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "oneStopFrame"))
    )
    # print('iframe 전환 완료')

    # 좌석 등급 펼치기
    tbody = wait_element(10, (By.ID, "divGradeSummary"))
    # tbody 안의 모든 tr 요소 찾기 (좌석 정보 tr만 해당)
    sector_elements = tbody.find_elements(By.TAG_NAME, "tr")
    if len(sector_elements) <= 2:
        sector_element = sector_elements[0]
    else:
        for i, row in enumerate(sector_elements):
            # 좌석 정보를 가진 tr 요소인지 확인 (class="box_list_area" 제외)
            if "box_list_area" not in row.get_attribute("class"):
                # 좌석 이름 td 요소 찾기
                sector_name = row.find_element(By.CLASS_NAME, "seat_name").text
                print(int(i / 2), '] ', sector_name)
        if presetData['grade'] == '':
            grade = input('원하는 등급에 해당하는 숫자를 적고 엔터: ')
            presetData['grade'] = grade
        else:
            grade = presetData['grade']
        sector_element = sector_elements[int(int(grade) * 2)]
    print(sector_element.text, ' 구역 요소 확장')
    sector_element.click()
    time.sleep(.2)

    # "list_area listOn" 클래스 아래의 모든 <li> 요소 찾기
    seat_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list_area.listOn li"))
    )

    if presetData['sector'] == '':
        for i, e in enumerate(seat_elements):
            print(i, '] ', e.text)
        focus_sector = input('조사 구역을 번호로 적어주세요: ')
        presetData['sector'] = focus_sector
    else:
        focus_sector = presetData['sector']
    if ',' in focus_sector:
        focus_sector = focus_sector.split(',')
    else:
        focus_sector = focus_sector.split()
    focus_sector_list = list(map(int, focus_sector))
    print('조사할 구역')
    for e in focus_sector_list:
        print(seat_elements[e].text)

    if presetData['repeat'] == '':
        repeat_time = 1
    else:
        repeat_time= float(presetData['repeat'])

    start_time = time.time()
    while time.time() - start_time < 2400: # 40분에 한번씩 초기화
        for i in focus_sector_list:
            seat_elements[i].click()

            didAlert = find_seat()

            if didAlert == 1:  # 좌석 잡음
                break
            elif didAlert == 2:  # 이선좌로 알람 발생
                sector_element.click()
                time.sleep(0.2)
                seat_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list_area.listOn li"))
                )
            time.sleep(repeat_time) # 구역 전환 시간텀
        if didAlert == 1:
            get_seat = True
            send_message(_T_BOT, _T_ID, 'WE Got Ticket!', 5)
            break
    if get_seat == False:
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])

    return get_seat


#############################
#프리셋 데이터 로드
presetData = getPreset()

with open('idpw.txt', 'r', encoding='utf-8') as idpwFile:
    _ID = idpwFile.readline().strip()
    _PW = idpwFile.readline().strip()
    _PLATFORM = idpwFile.readline().strip()
    _T_BOT = idpwFile.readline().strip()
    _T_ID = idpwFile.readline().strip()
    idpwFile.close()

# 웹페이지 해당 주소 이동
if presetData['page'] == '':
    driver.get("https://ticket.melon.com/performance/index.htm?prodId=210962") # 210876
else:
    driver.get(presetData['page'])
# driver.get("https://ticket.melon.com/performance/index.htm?prodId=210711")

login(_PLATFORM, _ID, _PW)

get_seat = False
while (not get_seat):
    # ID - box_list_date : 날짜 선택 리스트, item_date: 날짜
    wait_element(5, (By.ID, 'box_list_date'))
    date_list = driver.find_element(by=By.ID, value='box_list_date')
    dates = date_list.find_elements(by=By.CLASS_NAME, value='item_date')

    if len(dates) > 1:
        if presetData['date'] == '':
            for i, e in enumerate(dates):
                print(i,'] ', e.text)
            print('---------------------------')
            date = input('날짜 선택 (숫자로): ')
            presetData['date'] = date
        else:
            date = presetData['date']
        dates[int(date)].click()
    else:
        dates[0].click()

    time.sleep(.5)  # 너무 빠르면 시간 선택 오류 발생
    # ID - ticketReservation_Btn : 예매하기 버튼
    driver.find_element(by=By.ID, value='ticketReservation_Btn').click()

    time.sleep(1)
    # print(driver.window_handles)
    wait_stack = 0
    while True: # 대기열로 예매창이 열리지 않을 시
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            break
        else:
            wait_stack += 1
            if wait_stack > 10:
                print('예매창 열리길 기다리는 중...')
                wait_stack = 0
            time.sleep(2)
    print('시작 시간:', time.ctime())

    if checkAvailable():
        pass # 오류 발생시 하단 진행 사항 넘기기

    if checkCaptcha():  # 보안코드 있는지 체크
        captcha_text = driver.find_element(By.ID, 'label-for-captcha')
        captcha_count = 0
        while checkCaptcha():
            wait_element(5, (By.ID, 'btnReload'), True)
            time.sleep(1)
            captcha_text.clear()
            # ID - label-for-captcha : 캡챠 적는 란
            captchaImg = driver.find_element(By.ID, 'captchaImg')
            captcha_word = recognizing(captchaImg.get_attribute('src'))
            captcha_text.send_keys(captcha_word)
            if captcha_count > 5:
                send_message(_T_BOT, _T_ID, '캡챠 5회 이상 오류, 직접 진행해주세요')
                time.sleep(10)
            driver.find_element(By.XPATH, '//*[@id="btnComplete"]').click()
            time.sleep(.7)
            captcha_count += 1
        print('보안 문자 통과')
    else:
        print('보안 문자 없음')

    try:
        get_seat = searchSeats()
    except Exception as e:
        send_message(_T_BOT, _T_ID, '오류발생! 확인 요망')
        print(f"오류 발생: {e}")
    
### 결제 프로세스 ###
# 좌석 정보
ticket_info_element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".txt_ticket_info"))
)
seat_info = ticket_info_element.text
print(seat_info)

# 티켓 매수 선택
select_elements = driver.find_elements(By.ID, 'volume_10009_10067') # 아이브 id
# select_elements = driver.find_elements(By.ID, 'volume_10007_10067')  # 다른 예매 id

if select_elements:  # 선택창 확인
    select_element = select_elements[0]
    select = Select(select_element)
    select.select_by_index(1)

# 가격 선택 창에서 다음 버튼
wait_element(5, (By.ID, 'nextPayment'), True)

try:
    # 무통장입금 버튼 찾기
    cash_payment_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[title="무통장입금"]'))
    )

    # 무통장입금 버튼이 활성화되어 있는지 확인
    if not cash_payment_button.get_attribute("disabled"):
        cash_payment_button.click()
        try:
            # select box에서 원하는 은행 찾기
            bank_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'bankCode'))
            )
            select = Select(bank_select)

            # 은행명과 일치하는 option 찾아서 선택
            bank_found = False  # 은행을 찾았는지 여부를 저장하는 변수
            if presetData['bank'] == '':
                presetData['bank'] = '우리은행'
            for option in select.options:
                if option.text == presetData['bank']:
                    select.select_by_visible_text(presetData['bank'])
                    bank_found = True  # 은행을 찾았음을 표시
                    break  # 은행을 찾았으면 반복문 종료

            if not bank_found:  # 은행을 찾지 못했다면
                send_message(_T_BOT, _T_ID,'은행 선택 오류! 직접 결제 단계를 수행해주세요')
                print(f"은행: {presetData['bank']} 를 찾을 수 없습니다.")
                # 은행 못 찾으면 그냥 첫번째 은행으로 고르도록

        except Exception as e:
            send_message(_T_BOT, _T_ID, '은행 선택 오류! 직접 결제 단계를 수행해주세요')
            print(f"은행 선택 중 오류 발생: {e}")

        # 현금영수증 미발행 라디오 버튼 찾기 및 클릭
        no_issue_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[title="미발행"]'))  # title 속성으로 찾기
        )
        no_issue_radio.click()

        # 전체동의
        agree_all_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'chkAgreeAll'))
        )
        agree_all_checkbox.click()

        # 최종 결제
        payment_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btnFinalPayment'))
            )
        payment_button.click()
        send_message(_T_BOT, _T_ID, '결제 단계 수행 완료! 확인 요망', 2)

    else:  # 무통이 없으면 카카오페이 머니로 변경
        send_message(_T_BOT, _T_ID, '카카오페이 머니로 결제 진행')
        # 카카오페이 머니 클릭
        kakaopay_money_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[title="카카오페이 머니"]'))
        )
        kakaopay_money_button.click()

        # 전체동의
        agree_all_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'chkAgreeAll'))
        )
        agree_all_checkbox.click()

        time.sleep(2)
        # iframe 'payInitIframe'에 한번 더 접근
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "payInitIframe"))
        )

        # 카카오 결제 돌입
        time.sleep(2)
        payment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnFinalPayment'))
        )
        payment_button.click()

        # "카톡결제" 요소 찾기 및 클릭
        wait_element(10, (By.ID, '카톡결제'), True)

        # 휴대폰번호 입력
        phone_number_input = wait_element(10, (By.NAME, 'phoneNumber'))
        phone_number_input.send_keys(presetData['phonenumber'])

        # 생년월일 입력
        date_of_birth_input = driver.find_elements(By.NAME, 'dateOfBirth')
        date_of_birth_input.send_keys(presetData['birthdate'])
        
        # 결제요청하기
        time.sleep(1)

        try:
            payment_request_button = driver.find_elements(By.CSS_SELECTOR, 'button[type="button"].kp-m-button.large.primary')
            # 버튼 활성화 검사
            if not payment_request_button.get_attribute("disabled"):
                payment_request_button.click()
                send_message(_T_BOT, _T_ID, '카카오페이 결제 요청을 전송했습니다.', 4)
            else:
                print("결제요청 버튼이 비활성화되어 있습니다. 결제 조건을 확인하세요.")
                send_message(_T_BOT, _T_ID, '카카오페이 결제 오류! 직접 결제 단계를 수행해주세요')
        except Exception as e:
            send_message(_T_BOT, _T_ID, '카카오페이 결제 오류! 직접 결제 단계를 수행해주세요')
            print(f"결제요청 버튼 클릭 중 오류 발생: {e}")
except Exception as e:
    send_message(_T_BOT, _T_ID, '결제 오류! 직접 결제 단계를 수행해주세요')
    print(f"결제 수단 선택 중 오류 발생: {e}")