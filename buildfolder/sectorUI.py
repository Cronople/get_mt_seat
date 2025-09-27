import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtSlot

GRADE_MAP = {"1등급": "0", "2등급": "1", "3등급": "2"}
AREA_MAP = {"구역명": "name", "순서": "order"}
DIRECTION_MAP = {
    "↖": "ul", "↑": "u", "↗": "ur",
    "←": "l", "⨂": "m", "→": "r",
    "↙": "dl", "↓": "d", "↘": "dr"
}

INV_GRADE_MAP = {v: k for k, v in GRADE_MAP.items()}
INV_AREA_MAP = {v: k for k, v in AREA_MAP.items()}
INV_DIRECTION_MAP = {v: k for k, v in DIRECTION_MAP.items()}

class Backend(QObject):
    @pyqtSlot(str, str, result=bool)
    def save_to_file(self, profile_name, list_json):
        if not profile_name:
            return False
        try:
            data_list = json.loads(list_json)
            with open(f"data/{profile_name}_sector.txt", "w", encoding="utf-8") as f:
                for item in data_list:
                    grade = GRADE_MAP.get(item["gradeData"], item["gradeData"])
                    if int(grade) > 2: grade = str(int(grade)-1)
                    area = AREA_MAP.get(item["areaData"], item["areaData"])
                    direction = DIRECTION_MAP.get(item["directionData"], item["directionData"])
                    line = f"{grade}|{area}|{direction}|{item['textData']}\n"
                    f.write(line)
            return True
        except Exception as e:
            print("Error saving file:", e)
            return False

    @pyqtSlot(result=str)
    def load_from_file(self):
        path, _ = QFileDialog.getOpenFileName(None, "sector라고 적힌 데이터 파일들 중 선택", './data', "Text Files (*_sector.txt)")
        if not path:
            return ""
        try:
            filename = os.path.basename(path)
            profile_name = ""
            if filename.endswith("_sector.txt"):
                profile_name = filename[:-11]  # "_sector.txt" 제거

            items = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    grade, area, direction, text = line.strip().split("|")
                    grade = INV_GRADE_MAP.get(grade, grade)
                    area = INV_AREA_MAP.get(area, area)
                    direction = INV_DIRECTION_MAP.get(direction, direction)
                    items.append({
                        "gradeData": grade,
                        "areaData": area,
                        "directionData": direction,
                        "textData": text
                    })
            result = {
                "profileName": profile_name,
                "items": items
            }
            return json.dumps(result, ensure_ascii=False)
        
        except Exception as e:
            print("Error loading file:", e)
            return ""
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.load("buildfolder/sectorUI_main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    root = engine.rootObjects()[0]
    list_model = root.findChild(QObject, "listModel")

    backend = Backend(list_model)
    engine.rootContext().setContextProperty("backend", backend)

    sys.exit(app.exec())
