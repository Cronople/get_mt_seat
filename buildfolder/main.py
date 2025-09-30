import argparse
import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from preset import getPreset
from essentialDef import send_message, wait_element, printL
from ticketPage import login, checkDateSector, selectDate, checkTimeSector
from ticketSearch import checkAvailable, checkCaptcha, solvingCaptcha, settingSearch, searchSeats
from ticketPay import paymentProcess, ticketSelect


def create_parser():
    parser = argparse.ArgumentParser(description='Select preset profile')
    
    parser.add_argument('profile', type=str, help='write profile. usually this [yourprofile]_data.txt')
    # '--site' 인자 추가: 선택적 인자
    parser.add_argument('-s', '--site', type=str, default='', help='ticket reservation page')
    parser.add_argument('-l', '--log', type=int, default=2, help='log level. 1: every step 2: main act info. 3: nessesary info. 4: fatal error')
    
    return parser


#############################
def main():
    parser = create_parser()
    args = parser.parse_args()

    #프리셋 데이터 로드
    user_profile = args.profile
    presetData = getPreset(user_profile)
    presetData['logLevel'] = args.log

    printL(args.log, f"\n시작 시간: {time.ctime()}\n", 4)

    if presetData['device'] != 'hand':
        from mmocr_fixed.inference_word import preload_inferencer

    chrome_options = Options()
    user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    chrome_options.add_argument("user-agent="+user_agent)
    if presetData['headlessCheck'] == "1":
        chrome_options.add_argument('headless')
    else:
        chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--log-level=3")
    os = platform.system()
    if os == 'Windows':
        if presetData["profile"] == '':
            pass
        else:
            chrome_options.add_argument(f'user-data-dir=C:\\user_data\\{presetData["profile"]}')
    elif os == 'Darwin': # Mac
        pass
    elif os == 'Linux':
        pass
    driver = webdriver.Chrome(options=chrome_options)

    # 웹페이지 해당 주소 이동
    if args.site != '':
        driver.get(args.site)
    elif presetData['site'] == '':
        driver.get("https://ticket.melon.com/main/index.htm")
        input('예매 사이트로 이동 후 아무 키나 누르고 엔터: ')
    else:
        driver.get(presetData['site'])

    #check Notice Popup
    try:
        wait_element(driver, 3, (By.ID, 'noticeAlert_layerpopup_cookie'), True)
    except:
        pass

    # Site Login 
    login(driver, presetData)

    ## text recog model load
    if presetData['device'] == '':
        presetData['device'] = 'cpu'
        printL(args.log, '보안 문자 해제 방식 미선택. CPU로 진행', 3)
    if presetData['device'] != 'hand':
        recog_model = preload_inferencer(presetData['device'], args.log)
        printL(args.log, '*model load finished*', 2)

    ## check date sector is opened
    wait_stack = 600
    while(checkDateSector(driver)):
        wait_stack += 1
        if wait_stack > 600:
            printL(args.log, '[대기] 예매창 열리길 기다리는 중...', 2)
            wait_stack = 0
        time.sleep(.1)
    printL(args.log, '날짜창 열림', 2)

    if presetData['alreadySeletedSeatLimit'] == '' or presetData['alreadySeletedSeatLimit'] == '0':
        # alreadySeletedSeatLimit를 무제한으로 변경
        presetData['alreadySeletedSeatLimit'] = 5000

    get_seat = False
    timeList = None

    while (not get_seat):
        try:
            selectDate(driver, presetData['date'])
            printL(args.log, f"Date: {presetData['date']}", 2)

            while timeList == None:
                timeList = checkTimeSector(driver, 0)
            if timeList != 0:
                pass # 나중에 시간 리스트 선택해야할 경우 추가
            # ID - ticketReservation_Btn : 예매하기 버튼
            driver.find_element(by=By.ID, value='ticketReservation_Btn').click()
        except:
            pass

        try:
            # print(driver.window_handles)
            wait_stack = 301
            while len(driver.window_handles) == 1: # 대기열로 예매창이 열리지 않을 시
                wait_stack += 1
                if wait_stack > 300:
                    printL(args.log, '[대기] 예매창 열리길 기다리는 중...', 2)
                    wait_stack = 0
                time.sleep(.2)
            driver.switch_to.window(driver.window_handles[1])
            if presetData['headlessCheck'] == "1":
                driver.set_window_size(1024, 768)
            printL(args.log, f'시작 시간: {time.ctime()}', 3)

            if not checkAvailable(driver):
                continue # 오류 발생시 하단 진행 사항 넘기기

            if checkCaptcha(driver):  # 보안코드 있는지 체크
                solvingCaptcha(driver, presetData, recog_model)
                printL(args.log, '보안 문자 통과', 2)
            else:
                printL(args.log, '보안 문자 없음', 2)

            seletedSectorList = settingSearch(driver, presetData)
            if seletedSectorList != []:
                get_seat = searchSeats(driver, presetData, seletedSectorList)
            else:
                printL(args.log, 'ERROR! 선택 구역 존재하지 않음', 4)
                
        except Exception as e:
            if len(driver.window_handles) > 1 and get_seat == False:
                printL(args.log, f'오류 발생. 예매창 닫고 다시 시도. {e}', 4)
                send_message(presetData, '오류 발생. 예매창 닫고 다시 시도.')
                driver.close()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[0])
            else:
                printL(args.log, f"오류 발생: {e}", 4)
                driver.switch_to.window(driver.window_handles[0])

        
    ### 결제 프로세스 ###
    ticketSelect(driver, presetData)
    paymentProcess(driver, presetData)
    try:
        driver.switch_to.default_content()  # iframe에서 빠져나오기
    except:
        printL(args.log, 'iframe 벗어나기 오류 발생', 4)
    try:
        # "결제가 정상적으로 완료되었습니다." 요소 찾기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tit_gr")))
        send_message(presetData, '결제 단계 수행 완료! 확인 요망')
    except Exception as e:
        send_message(presetData, '결제 오류! 직접 결제 단계를 수행해주세요', 3)


if __name__ == '__main__':
    main()