import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from essentialDef import send_message, wait_element, checkAlert


def checkAvailable(driver):
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "inner-btn")))
        driver.close()
        print('예매창 오류로 대기 (30초)')
        time.sleep(30)
        driver.switch_to.window(driver.window_handles[0])
        return False
    except:
        return True


def settingJS(driver, seatDirection):
    javaBase = """
        const ezCanvas = document.getElementById('ez_canvas');
        const rectElements = ezCanvas.querySelectorAll('rect'); // rect 요소 선택
        const notEmptyElements = [];

        rectElements.forEach(rect => {
            const fillValue = rect.getAttribute('fill');
            if (fillValue && fillValue !== '#DDDDDD' && fillValue !== 'none') {
                notEmptyElements.push(rect);
            }
        });

    """
    javaDirectionH = ''
    javaDirectionV = ''

    if seatDirection == 'l' or seatDirection == 'r':
        javaBase += "notEmptyElements.sort((a, b) => a.getAttribute('y') - b.getAttribute('y'))"
    if 'l' in seatDirection:
        javaDirectionH = """
        notEmptyElements.sort((a, b) => a.getAttribute('x') - b.getAttribute('x'))

        """
    elif 'r' in seatDirection:
        javaDirectionH = """
        notEmptyElements.sort((a, b) => b.getAttribute('x') - a.getAttribute('x'))

        """
    if 'u' in seatDirection:
        javaDirectionV = """
        notEmptyElements.sort((a, b) => a.getAttribute('y') - b.getAttribute('y'))

        """
    elif 'd' in seatDirection:
        javaDirectionV = """
        notEmptyElements.sort((a, b) => b.getAttribute('y') - a.getAttribute('y'))

        """
    
    # JavaScript 코드 실행
    seats = driver.execute_script(
        javaBase+
        javaDirectionH+
        javaDirectionV+
        """

        return notEmptyElements;
        """)
    
    return seats


def find_seat(driver, ticketBtn, seatDirection, asSeatLim, pre_seat = []):
    didAlert = 0

    seats = settingJS(driver, seatDirection)

    # 찾은 요소들을 활용하여 Selenium 작업 수행 (예: 클릭, 텍스트 가져오기 등)
    for seat in seats:
        if len(seats) == len(pre_seat) or int(asSeatLim) <= len(pre_seat):
            # 이선좌 자리로 선택된 것과 남은게 동일하다면 넘기기
            print('이선좌 제한으로 다음 구역 이동')
            return 2 # 넘기기 위해 이선좌 발생
        elif len(seats) > len(pre_seat) and seat.rect in pre_seat:
            # 직전에 시도한 자리랑 같은데 2자리 이상이면 다음거로 시도
            continue
        # 예시: 특정 fill 값을 가진 요소 클릭
        
        pre_seat.append(seat.rect)
        # print('좌석선택: ', seat.rect)
        
        seat.click()
        time.sleep(.5)
        ticketBtn.click()

        print('*'*20)
        print('구역 내 좌석 수:', len(seats))
        if checkAlert(driver):
            didAlert = find_seat(driver, ticketBtn, seatDirection, asSeatLim, pre_seat)
            if didAlert != 1:
                didAlert = 2  # 좌석 찾음, 이선좌로 알람발생
            break
        else:
            return 1  # 좌석 찾음, 알람 없음
    return didAlert  # 0의 경우 좌석 없음


def getSector(driver, presetData, isMultigrade):
    deleteSectorList = []
    seletedSectorList = []
    # print('check21')
    tbody = wait_element(driver, 10, (By.ID, "divGradeSummary"))
    # "list_area listOn" 클래스 아래의 모든 <li> 요소 찾기
    # print('check22')
    list_area = tbody.find_elements(By.CSS_SELECTOR, ".list_area.listOn")
    # print('check23')
    for sectorData in presetData['sectorList']:
        focus_sector = None
        if sectorData['sectorType'] == 'name': #특정 구역을 명명했을 경우
            try:
                if isMultigrade:
                    seat_elements = list_area[int(sectorData['gradeData'])].find_elements(By.TAG_NAME, "li")
                else:
                    
                    seat_elements = list_area[0].find_elements(By.TAG_NAME, "li")
                for e in seat_elements:
                    if sectorData['textData'].strip() in e.text:
                        focus_sector = e
                        print(sectorData['gradeData'], e.text)
                        break
                if focus_sector == None:
                    print('No sector: ', sectorData['textData'])
                    deleteSectorList.append(sectorData)
                else:
                    seletedSectorList.append(focus_sector)
            except Exception as e:
                print('구역 세팅 오류 발생', e)
        else:
            if isMultigrade:
                seat_elements = list_area[int(sectorData['gradeData'])].find_elements(By.TAG_NAME, "li")
            else:
                seat_elements = list_area[0].find_elements(By.TAG_NAME, "li")
            focus_sector = seat_elements[int(sectorData['textData'])]
            if focus_sector == None:
                print('No sector: ', sectorData['textData'])
                deleteSectorList.append(sectorData)
            else:
                print(sectorData['gradeData'], focus_sector.text)
                seletedSectorList.append(focus_sector)

    for deleteSector in deleteSectorList:
            presetData['sectorList'].remove(deleteSector)

    return seletedSectorList

def getGrade(driver, sectorData):
    # 좌석 등급 펼치기
    tbody = wait_element(driver, 10, (By.ID, "divGradeSummary"))
    # tbody 안의 모든 tr 요소 찾기 (좌석 정보 tr만 해당)
    sector_elements = tbody.find_elements(By.TAG_NAME, "tr")
    if len(sector_elements) <= 2:
        sector_element = sector_elements[0]
    else:
        grade = sectorData['gradeData']
        sector_element = sector_elements[int(int(grade) * 2)]
    # print(sector_element.text, ' 구역 요소 확장')
    return sector_element


def openGrade(driver, presetData):
    # print('check10')
    tbody = wait_element(driver, 10, (By.ID, "divGradeSummary"))
    present_grade = presetData['sectorList'][0]['gradeData']
    multi_grade = False
    for sectorData in presetData['sectorList']:
        if sectorData['gradeData'] != present_grade:
            multi_grade = True
            break
    # print('check11')
    sector_elements = tbody.find_elements(By.TAG_NAME, "tr")
    if multi_grade:
        # 다중 등급이라 모든 등급 열기
        for sector_element in sector_elements:
            try:
                sector_element.find_element(By.CSS_SELECTOR, ".open")
            except:
                sector_element.click()
    else:
        # 단일 등급 설정일 경우
        print('단일 등급')
        sector_element = sector_elements[int(int(present_grade) * 2)]
        try:
            sector_element.find_element(By.CSS_SELECTOR, ".open")
        except:
            sector_element.click()

    time.sleep(.1)
    return multi_grade


def searchSetting(driver, presetData):
    # iframe으로 전환 (반드시 필요)
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "oneStopFrame"))
    )
    # print('iframe 전환 완료')

    # 좌석 등급 설정
    isMultigrade = openGrade(driver, presetData)
    time.sleep(0.1)
    # 좌석 설정
    seletedSectorList = getSector(driver, presetData, isMultigrade)

    return seletedSectorList


def searchSeats(driver, presetData, seletedSectorList):
    get_seat = False
    start_time = time.time()

    if presetData['repeat'] == '':
        repeat_time = .5
    else:
        repeat_time= float(presetData['repeat'])

    ticketBtn = driver.find_element(by=By.ID, value='nextTicketSelection')

    while time.time() - start_time < 600: # 10분에 한번씩 초기화
        for i, focus_sector in enumerate(seletedSectorList):
            sectorName = focus_sector.text
            # print('check50')
            focus_sector.click()
            # print('check51')
            seatDirection = presetData['sectorList'][i]['directionData']
            didAlert = find_seat(driver, ticketBtn, seatDirection, presetData['alreadySeletedSeatLimit'], [])
            if didAlert == 1:  # 좌석 잡음
                break
            elif didAlert == 2:  # 이선좌로 알람 발생
                # print('check0')
                print(f'{time.ctime()}\n 이선좌 구역: {sectorName}')
                # print('check1')
                ticketBtn = driver.find_element(by=By.ID, value='nextTicketSelection')
                # print('check2')
                isMultigrade = openGrade(driver, presetData)
                # print('check3')
                seletedSectorList = getSector(driver, presetData, isMultigrade)
                break
            time.sleep(repeat_time) # 구역 전환 시간텀
        if didAlert == 1:
            get_seat = True
            send_message(presetData, 'WE Got Ticket!', 3)
            break
    if get_seat == False:
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])

    return get_seat


def checkCaptcha(driver):  # display: none or block에 따라 확인
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "certification"))
        )
        style = element.get_dom_attribute("style")
        if style:  # style 속성이 존재하는 경우에만 확인
            return not ("display: none" in style)  # display:block 상태
        else:
            return False  # style 속성이 없는 경우
    except:  # element를 찾을 수 없는 경우
        return False  # 보안창이 없으므로 패스
    

def solvingCaptcha(driver, presetData, recog_model):
    if presetData['device'] != 'hand':
        from recognize_word import recognizing

    if presetData['device'] == 'hand':
        wait_stack = 31
        while checkCaptcha(driver):
            time.sleep(.1)
            if wait_stack > 30:
                print('캡챠 직접 인증 기다리는 중...you are using hand option')
                wait_stack = 0
            wait_stack += 1
    else:
        captcha_text = driver.find_element(By.ID, 'label-for-captcha')
        captcha_reload = driver.find_element(By.ID, 'btnReload')
        captcha_count = 0
        while checkCaptcha(driver):
            if captcha_count > 10:
                send_message(presetData, '캡챠 10회 이상 오류, 직접 진행해주세요')
                while checkCaptcha(driver):
                    time.sleep(1)
                break
            elif captcha_count > 0:
                captcha_reload.click()
                time.sleep(.3)
            try:
                captcha_text.clear()
                # ID - label-for-captcha : 캡챠 적는 란
                captchaImg = driver.find_element(By.ID, 'captchaImg')
                captcha_word = recognizing(captchaImg.get_attribute('src'), recog_model)
                captcha_text.send_keys(captcha_word)
                # print(captcha_word)
                driver.find_element(By.XPATH, '//*[@id="btnComplete"]').click()
            except:
                pass
            time.sleep(.3)
            captcha_count += 1