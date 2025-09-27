import time
from selenium.webdriver.common.by import By
from essentialDef import send_message, wait_element


def login(driver, presetData):
    _platform = presetData['loginMethod']
    _id = presetData['id']
    _pw = presetData['pw']
    try:
        wait_element(driver, 10, (By.ID, 'global_top_ticketLogin_Button'), clickable=True)
        if _platform in '카카오멜론티켓KAKAOMELONKakaoMelonkakaomelon':
            if _platform in '카카오KAKAOKakaokakao':
                print('카카오 로그인')
                wait_element(driver, 5, (By.XPATH, '//*[@id="conts_section"]/div/div/div[1]/button'), clickable=True)
                time.sleep(2)  # 대기하며 로그인 창이 유지되는지 확인

                if len(driver.window_handles) > 1:  # 로그인 정보가 없을 때
                    driver.switch_to.window(driver.window_handles[1])
                    wait_element(driver, 5, (By.ID, 'loginId--1'))
                    wait_element(driver, 5, (By.ID, 'label-saveSignedIn'), True)
                    driver.find_element(By.ID, 'loginId--1').send_keys(_id)
                    driver.find_element(By.ID, 'password--2').send_keys(_pw)
                    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
                    time.sleep(2)
                    time_stack = 0
                    while len(driver.window_handles) > 1:
                        if time_stack > 10:
                            print('카카오 로그인 인증 대기 중...')
                            send_message(presetData, '카카오 로그인 인증 요구!')
                            time_stack = 0
                        time_stack += 1
                        time.sleep(1)
                    print('로그인 인증 완료.')
                else:
                    print('기존 로그인 정보로 로그인 완료')
                driver.switch_to.window(driver.window_handles[0])
            else: # 멜론 로그인
                print('멜론 로그인')
                wait_element(driver, 5, (By.XPATH, '//*[@id="conts_section"]/div/div/div[2]/button'), clickable=True)
                wait_element(driver, 5, (By.ID, 'id'))
                driver.find_element(By.ID, 'id').send_keys(_id)
                driver.find_element(By.ID, 'pwd').send_keys(_pw)
                driver.find_element(By.ID, 'btnLogin').click()
                time.sleep(3)
        else:
            print('idpw.txt 3번째 줄에 카카오,멜론티켓,KAKAO,MELON,Kakao,Melon,kakao,melon 중에 하나를 적어주세요')
    except Exception as e:
        send_message(presetData, '로그인 오류 발생')
        print(f"로그인 오류 발생: {e}")


def checkDateSector(driver):
    try:
        driver.find_element(by=By.ID, value='ticketReservation_Btn')
        return False
    except:
        return True


def checkTimeSector(driver, seletedTime):
    # box_type_list가 나타날 때까지 기다림
    try:
        list_box = wait_element(driver, 1, (By.CSS_SELECTOR, "#section_time .box_type_list"))
        
        if seletedTime == 0:
            return 0
        else:
            # 시간 목록을 포함하는 ul 요소를 찾음
            time_list_ul = list_box.find_element(By.ID, "list_time")
            
            # 모든 li.item_time 요소를 찾음
            time_items = time_list_ul.find_elements(By.CSS_SELECTOR, "li.item_time")
            
            timeList = []
            for item in time_items:
                # 각 항목의 텍스트에서 시간 정보를 추출 (trim을 위해 strip() 사용)
                button_element = item.find_element(By.TAG_NAME, "button")
                timeList.append(button_element)
            
            return timeList
    except Exception:
        return None


def selectDate(driver, seleted_date):
    # ID - box_list_date : 날짜 선택 리스트, item_date: 날짜
    wait_element(driver, 5, (By.ID, 'box_list_date'))
    date_list = driver.find_element(by=By.ID, value='box_list_date')
    dates = date_list.find_elements(by=By.CLASS_NAME, value='item_date')
    print('날짜: ', seleted_date)

    if len(dates) > 1:
        if seleted_date == '':
            for i, e in enumerate(dates):
                print(i,'] ', e.text)
            print('---------------------------')
            date = input('날짜 선택 (숫자로): ')
            seleted_date = date
        else:
            date = seleted_date
        dates[int(date)].click()
    else:
        dates[0].click()
