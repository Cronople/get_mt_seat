import sys
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from pathlib import Path

class DataHandler(QObject):
    """QML과 Python 간 데이터 통신을 위한 클래스"""
    dataLoaded = pyqtSignal(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
    
    @pyqtSlot(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    def saveData(self, headlessCheck, date, bank, phonenum, birth, repeat, site, profile, device,
                 loginMethod, idData, pwData, telegramBot, telegramChannel, asSeatLimit, payment):
        """QML에서 받은 데이터를 텍스트 파일에 저장하는 메서드"""
        data = f"""profile: {profile}
headlessCheck: {headlessCheck}
loginMethod: {loginMethod}
id: {idData}
pw: {pwData}
site: {site}
date: {date}
repeat: {repeat}
alreadySeletedSeatLimit: {asSeatLimit}
device: {device}
payment: {payment}
bank: {bank}
phonenum: {phonenum}
birth: {birth}
telegramBot: {telegramBot}
telegramChannel: {telegramChannel}
"""
        
        try:
            file_path = f"./data/{profile}_data.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"데이터가 '{file_path}' 파일에 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 오류가 발생했습니다: {e}")

        if device == 'cpu':
            conda_env = 'mt_seat_cpu'
        elif device == 'hand':
            conda_env = 'mt_seat_hand'
        else:
            conda_env = 'mt_seat_gpu'

        bat = f"""call conda activate {conda_env}
call python buildfolder\main.py "{profile}"
pause"""

        try:
            file_path = f"{profile}_run.bat"
            with open(file_path, "w") as f:
                f.write(bat)
            print(f"데이터가 '{file_path}' 파일에 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 오류가 발생했습니다: {e}")


    @pyqtSlot(str)
    def loadData(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # 단순 파싱 (형식 맞춘 경우)
            def extract(prefix):
                for line in lines:
                    if line.strip().startswith(prefix):
                        return line.split(":", 1)[1].strip()
                return ""
            headlessCheck = extract("headlessCheck")
            date = extract("date")
            bank = extract("bank")
            phonenum = extract("phonenum")
            birth = extract("birth")
            repeat = extract("repeat")
            site = extract("site")
            profile = extract("profile")
            device = extract("device")
            loginMethod = extract("loginMethod")
            idData = extract("id")
            pwData = extract("pw")
            telegramBot = extract("telegramBot")
            telegramChannel = extract("telegramChannel")
            asSeatLimit = extract("alreadySeletedSeatLimit")
            payment = extract("payment")

            # QML로 데이터 전달
            self.dataLoaded.emit(headlessCheck, date, bank, phonenum, birth, repeat, site, profile, device,
                                 loginMethod, idData, pwData, telegramBot, telegramChannel, asSeatLimit, payment)
            print("데이터를 성공적으로 불러왔습니다.")
        except Exception as e:
            print(f"파일 불러오기 중 오류 발생: {e}")


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Python 클래스 인스턴스 생성
    handler = DataHandler()
    # QML 컨텍스트에 클래스 인스턴스를 노출시킵니다.
    # QML에서 `dataHandler`라는 이름으로 접근할 수 있습니다.
    engine.rootContext().setContextProperty("dataHandler", handler)
    
    qml_file = Path(__file__).parent / "presetUI_main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))

    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()