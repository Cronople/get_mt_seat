import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from essentialDef import send_message, wait_element, checkAlert


def ticketSelect(driver, presetData):
    # 좌석 정보
    ticket_info_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".txt_ticket_info"))
    )
    seat_info = ticket_info_element.text
    send_message(presetData, seat_info)
    print(seat_info)

    # 티켓 매수 선택
    try:
        # CSS 선택자 '[id^="..."]'를 사용하여 특정 문자열로 시작하는 ID를 가진 요소를 찾습니다.
        ticket_select_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='volume_']")
    except:
        pass
    # ticket_select_elements = driver.find_elements(By.ID, 'volume_10009_10067') # 아이브 id
    # ticket_select_elements = driver.find_elements(By.ID, 'volume_10007_10067')  # 다른 예매 id

    if ticket_select_elements:  # 선택창 확인
        select_element = ticket_select_elements[0]
        select = Select(select_element)
        select.select_by_index(1)
        # 아직 1장만 고르도록 되어있음.

    # 가격 선택 창에서 다음 버튼
    wait_element(driver, 5, (By.ID, 'nextPayment'), True)
    checkAlert(driver, 3)
    time.sleep(3)


def virtualAccountOption(driver, presetData):
    # 무통장입금 버튼 찾기
    cash_payment_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='payMethodCode003']"))
    )
    # 무통장입금 버튼이 활성화되어 있는지 확인
    isClickable = None
    try:
        isClickable_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "payMethodCode003"))
        )
        isClickable = isClickable_element.get_dom_attribute("style")
    except:
        send_message(presetData, '무통장입금 비활성화! 직접 결제 단계를 수행해주세요', 3)
    if isClickable == None:
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
                send_message(presetData,'은행 선택 오류! 직접 결제 단계를 수행해주세요')
                print(f"은행: {presetData['bank']} 를 찾을 수 없습니다.")
                # 은행 못 찾으면 그냥 첫번째 은행으로 고르도록

        except Exception as e:
            send_message(presetData, '은행 선택 오류! 직접 결제 단계를 수행해주세요')
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

        time.sleep(1)
        # 최종 결제
        payment_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btnFinalPayment'))
            )
        payment_button.click()


def kakaoMoneyOption(driver, presetData):
    send_message(presetData, '카카오페이 머니로 결제 진행')
    isClickable = None
    # 카카오페이 머니 클릭
    # kakaopay_money_button = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='payMethod009_money']"))
    # )
    # try:
    #     isClickable_element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "payMethod009_money"))
    #     )
    #     isClickable = isClickable_element.get_dom_attribute("style")
    # except:
    #     send_message(presetData, '카카오페이 비활성화! 직접 결제 단계를 수행해주세요', 3)
    if isClickable == None:
        # kakaopay_money_button.click()
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

        time.sleep(10)

        # 카카오 결제 돌입
        # iframe 'payInitIframe'에 한번 더 접근
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "payInitIframe"))
        )

        time.sleep(2)
        # "카톡결제" 요소 찾기 및 클릭
        wait_element(driver, 10, (By.ID, '카톡결제'), True)

        phone_number_input = driver.find_element(By.CSS_SELECTOR, 'input[name="phoneNumber"]')
        phone_number_input.send_keys(presetData['phonenum'])
        time.sleep(1)
        date_of_birth_input = driver.find_element(By.CSS_SELECTOR, 'input[name="dateOfBirth"]')
        date_of_birth_input.send_keys(presetData['birth'])

        # 결제요청하기
        time.sleep(5)

    try:
        payment_request_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                    'button[type="button"].kp-m-button.large.primary')
        # 버튼 활성화 검사
        if payment_request_buttons and payment_request_buttons[0].is_enabled():  # 버튼리스트가 비어있지않고, 첫번째 요소가 활성화 되어있는지 확인
            payment_request_buttons[0].click()
            time.sleep(1)
            driver.switch_to.default_content()  # iframe에서 빠져나오기
            send_message(presetData, '카카오페이 결제 요청을 전송했습니다.', 4)
        else:
            print("결제요청 버튼이 비활성화되어 있습니다. 결제 조건을 확인하세요.")
            send_message(presetData, '카카오페이 결제 오류! 직접 결제 단계를 수행해주세요')
    except Exception as e:
        send_message(presetData, '카카오페이 결제 오류! 직접 결제 단계를 수행해주세요')
        print(f"결제요청 버튼 클릭 중 오류 발생: {e}")


def paymentProcess(driver, presetData):
    try:
        if presetData['payment'] == 'bank':
            virtualAccountOption(driver, presetData)
        elif presetData['payment'] == 'kakaopay':  # 카카오페이 머니로 실행
            kakaoMoneyOption(driver, presetData)
        else:
            if presetData['headlessCheck'] == '1':
                virtualAccountOption(driver, presetData)
            else:    
                send_message(presetData, '직접 결제 진행!')
                print('직접 결제 진행.')
                while True:
                    time.sleep(100)
    except Exception as e:
        send_message(presetData, '결제 오류! 직접 결제 단계를 수행해주세요')
        print(f"결제 수단 선택 중 오류 발생: {e}")
