import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

ApplicationWindow {
    visible: true
    width: 480
    height: 650
    title: "구역 및 좌석 선택기"
    property string selectedDirection: ""

    ColumnLayout {
        anchors.fill: parent
        spacing: 10
        Layout.margins: 10

        // --- 최상단: 프로필 입력 ---
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 10
            Text { text: "프로필:"; font.pixelSize: 24}
            TextField { id: profileInput; placeholderText: "프로필 이름 입력"
                font.pixelSize: 18
                implicitHeight: 30
                Layout.preferredWidth: 160
                }
        }

        // --- 좌우 RowLayout ---
        RowLayout {
            Layout.fillWidth: true
            spacing: 20

            // --- 좌측: 등급/구역 선택 ---
            ColumnLayout {
                spacing: 10
                Layout.fillWidth: true

                // 등급 선택
                GroupBox {
                    title: "등급 선택"
                    Layout.fillWidth: true
                    RowLayout {
                        spacing: 10
                        RadioButton { id: grade1; text: "1등급"; checked: true }
                        RadioButton { id: grade2; text: "2등급" }
                        RadioButton { id: grade3; text: "3등급" }
                        RadioButton { id: gradeOther; text: "기타" }

                        TextField {
                            id: gradeOtherInput
                            placeholderText: "숫자"
                            enabled: gradeOther.checked
                            Layout.preferredWidth: 40
                        }
                    }
                }

                // 구역/순서 선택
                GroupBox {
                    title: "구역/순서 선택"
                    Layout.fillWidth: true
                    RowLayout {
                        spacing: 10
                        RadioButton { id: areaRadio; text: "구역명"; checked: true }
                        RadioButton { id: orderRadio; text: "순서" }
                    }
                }
            }

            // --- 우측: 방향 선택 8방향 버튼 ---
            GroupBox {
                title: "방향 선택"
                Layout.fillWidth: true
                GridLayout {
                    columns: 3
                    rowSpacing: 5
                    columnSpacing: 5
                    anchors.horizontalCenter: parent.horizontalCenter

                    // 위쪽
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "↖" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "↖"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="↖"; cursorShape: Qt.PointingHandCursor }
                    }
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "↑" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "↑"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="↑"; cursorShape: Qt.PointingHandCursor }
                    }
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "↗" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "↗"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="↗"; cursorShape: Qt.PointingHandCursor }
                    }

                    // 중간
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "←" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "←"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="←"; cursorShape: Qt.PointingHandCursor }
                    }
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "⨂" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "⨂"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="⨂"; cursorShape: Qt.PointingHandCursor }
                    }
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "→" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "→"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="→"; cursorShape: Qt.PointingHandCursor }
                    }

                    // 아래쪽
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "↙" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "↙"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="↙"; cursorShape: Qt.PointingHandCursor }
                    }
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "↓" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "↓"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="↓"; cursorShape: Qt.PointingHandCursor }
                    }
                    Rectangle {
                        width: 40; height: 40; radius: 5
                        color: selectedDirection === "↘" ? "lightblue" : "lightgray"
                        border.color: "black"
                        Text { anchors.centerIn: parent; text: "↘"; font.pixelSize: 16 }
                        MouseArea { anchors.fill: parent; onClicked: selectedDirection="↘"; cursorShape: Qt.PointingHandCursor }
                    }
                }
            }
        }

        // --- 텍스트 입력 + 추가 버튼 ---
        RowLayout {
            spacing: 5
            TextField {
                id: inputField
                Layout.fillWidth: true
                placeholderText: "텍스트 입력..."
                font.pixelSize: 18
                implicitHeight: 30
            }

            Button {
                text: "추가"
                font.pixelSize: 18
                implicitWidth: 80
                implicitHeight: 30
                onClicked: {
                    var gradeText = grade1.checked ? "1등급" :
                                    grade2.checked ? "2등급" :
                                    grade3.checked ? "3등급" :
                                    gradeOtherInput.text
                    var areaText = areaRadio.checked ? "구역명" : "순서"

                    if (inputField.text !== "" && gradeText !== "" && selectedDirection !== "") {
                        listModel.append({
                            "gradeData": gradeText,
                            "areaData": areaText,
                            "directionData": selectedDirection,
                            "textData": inputField.text
                        })
                        inputField.text = ""
                        gradeOtherInput.text = ""
                        selectedDirection = ""
                    }
                }
            }
        }

        // --- 리스트 ---
        ListView {
            id: listView
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ListModel { id: listModel }
            spacing: 5

            delegate: Row {
                width: listView.width
                spacing: 10

                Button { text: "삭제"; onClicked: listModel.remove(index) }
                Button { text: "↑"; enabled: index>0; onClicked: listModel.move(index,index-1,1) }
                Button { text: "↓"; enabled: index<listModel.count-1; onClicked: listModel.move(index,index+1,1) }

                Text {
                    text: gradeData + " / " + areaData + " / " + directionData + " / " + textData
                    font.pixelSize: 16
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 20

            Button {
                text: "불러오기"
                onClicked: {
                    var jsonStr = backend.load_from_file()
                    if (jsonStr === "") return

                    var data = JSON.parse(jsonStr)

                    // 크롬 프로필 텍스트 자동 채우기
                    if (data.profileName !== undefined)
                        profileInput.text = data.profileName

                    // 리스트 채우기
                    listModel.clear()
                    for (var i=0; i<data.items.length; i++) {
                        listModel.append(data.items[i])
                    }
                }
            }

            Button {
                text: "저장하기"
                onClicked: {
                    var items = []
                    for (var i = 0; i < listModel.count; i++) {
                        items.push(listModel.get(i))
                    }
                    var success = backend.save_to_file(profileInput.text, JSON.stringify(items))
                    if (success) {
                        console.log("저장 완료")
                        successDialog.text = profileInput.text+"_sector.txt로 저장 완료되었습니다."
                        successDialog.open()
                    }
                }
                MessageDialog {
                    id: successDialog
                    title: "알림"
                    buttons: MessageDialog.Ok
                }
            }
        }

    }
}
