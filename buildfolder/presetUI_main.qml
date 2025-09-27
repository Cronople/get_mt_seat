import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 480
    height: 600
    title: "예매 프로그램"

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true
        padding: 16
        bottomPadding: 50
    
        ColumnLayout {
            // 여기에 UI 컴포넌트들을 추가합니다.
            spacing: 15

            CheckBox {
                id: headlessCheckBox
                text: qsTr("headless option")
            }

            ColumnLayout {
                Label { text: "크롬 프로필 선택"; font.bold: true; font.pointSize: 12 }
                TextField {
                    id: profileText
                    placeholderText: "프로필명 입력"
                }
            }

            ColumnLayout {
                
                id: loginMethodSector
                Label { text: "로그인 방식 선택"; font.bold: true; font.pointSize: 12}
                RowLayout {
                    RadioButton { id: melonSector; text: "멜론"}
                    RadioButton { id: kakaoSector; text: "카카오"}
                }
                RowLayout {
                    TextField {
                        id: idText
                        placeholderText: "ID"
                        Layout.preferredWidth: 100
                    }
                    TextField {
                        id: pwText
                        placeholderText: "Password"
                        Layout.preferredWidth: 120
                    }
                }
            }

            ColumnLayout {
                Label { text: "예매사이트"; font.bold: true; font.pointSize: 12 }
                TextField {
                    id: bookingSiteText
                    placeholderText: "URL 입력"
                    Layout.preferredWidth: 400
                }
            }

            ColumnLayout {
                id: dateSector
                Label { text: "날짜 선택"; font.bold: true; font.pointSize: 12}
                RowLayout {
                    RadioButton { id: day1; text: "첫날"; ButtonGroup.group: dateGroup }
                    RadioButton { id: day2; text: "둘째날"; ButtonGroup.group: dateGroup }
                    RadioButton { id: day3; text: "셋째날"; ButtonGroup.group: dateGroup }
                    RadioButton {
                        id: otherDateRadio
                        text: "기타: "
                        ButtonGroup.group: dateGroup
                    }
                    TextField {
                        id: otherDateText
                        placeholderText: "숫자"
                        validator: RegularExpressionValidator { regularExpression: /^[0-9]*$/}
                        enabled: otherDateRadio.checked
                        Layout.preferredWidth: 30
                    }
                    ButtonGroup { id: dateGroup; exclusive: true }
                    // 라디오 버튼들을 그룹에 추가
                    Component.onCompleted: {
                        dateGroup.addButton(day1)
                        dateGroup.addButton(day2)
                        dateGroup.addButton(day3)
                        dateGroup.addButton(otherDateRadio)
                    }
                }
            }

            ColumnLayout {
                Label { text: "반복 간격 (초단위)"; font.bold: true; font.pointSize: 12 }
                TextField {
                    id: repeatIntervalText
                    placeholderText: "최소 0.2"
                    Layout.preferredWidth: 50
                }
            }

            ColumnLayout {
                Label { text: "구역 당 이선좌 제한"; font.bold: true; font.pointSize: 12 }
                TextField {
                    id: asSeatLimitText
                    placeholderText: "무제한은 0"
                    Layout.preferredWidth: 70
                }
            }

            ColumnLayout {
                id: deviceSector
                Label { text: "보안 문자 통과 방식 선택"; font.bold: true; font.pointSize: 12 }
                RowLayout {
                    RadioButton { id: cpuRadio; text: "cpu" }
                    RadioButton { id: gpuRadio; text: "gpu(cuda:0)" }
                    RadioButton { id: handRadio; text: "hand(직접)" }
                    RadioButton {
                        id: otherDeviceRadio
                        text: "기타: "
                    }
                    TextField {
                        id: otherDeviceText
                        placeholderText: "텍스트 입력"
                        enabled: otherDeviceRadio.checked
                    }
                    ButtonGroup { id: deviceGroup; exclusive: true }
                    Component.onCompleted: {
                        deviceGroup.addButton(cpuRadio)
                        deviceGroup.addButton(gpuRadio)
                        deviceGroup.addButton(handRadio)
                        deviceGroup.addButton(otherDeviceRadio)
                    }
                }
            }

            ColumnLayout {
                id: paymentSector
                Label { text: "결제 방식 선택"; font.bold: true; font.pointSize: 12 }
                RowLayout {
                    RadioButton { id: manualRadio; text: "직접(manual)" }
                    RadioButton { id: bankSendRadio; text: "무통장" }
                    RadioButton { id: kakaoPayRadio; text: "카카오결제" }
                    ButtonGroup { id: paymentGroup; exclusive: true }
                    Component.onCompleted: {
                        paymentGroup.addButton(manualRadio)
                        paymentGroup.addButton(bankSendRadio)
                        paymentGroup.addButton(kakaoPayRadio)
                    }
                }
            }
            
            ColumnLayout {
                Layout.leftMargin: 20
                id: bankSector
                Label { text: "↳ 은행명(무통장 옵션)"; font.bold: true; font.pointSize: 10 }
                ComboBox {
                    id: bankComboBox
                    enabled: bankSendRadio.checked
                    model: ["기업은행", "국민은행", "농협은행", "하나은행", "우리은행", "신한은행", "경남은행", "우체국", "부산은행", "iM뱅크"]
                }
            }
            ColumnLayout {
                Layout.leftMargin: 20
                Label { text: "↳ 전화번호 (카카오결제 옵션)"; font.bold: true; font.pointSize: 10 }
                TextField {
                    id: phoneNumText
                    placeholderText: "- 없이 숫자만 입력"
                    enabled: kakaoPayRadio.checked
                    validator: RegularExpressionValidator { regularExpression: /^[0-9]{0,11}$/ }
                }
            }

            ColumnLayout {
                Layout.leftMargin: 20
                Label { text: "↳ 생년월일 (카카오결제 옵션)"; font.bold: true; font.pointSize: 10 }
                TextField {
                    id: birthDateText
                    placeholderText: "6자리 생년월일"
                    enabled: kakaoPayRadio.checked
                    validator: RegularExpressionValidator { regularExpression: /^[0-9]{0,6}$/ }
                }
            }

            ColumnLayout {
                Label { text: "텔레그램 알림 (선택사항)"; font.bold: true; font.pointSize: 12 }
                TextField {
                    id: telegramBotText
                    placeholderText: "봇 토큰 Bot token"
                    Layout.preferredWidth: 400
                }
                TextField {
                    id: telegramChannelText
                    placeholderText: "채널 아이디 Channel ID"
                    Layout.preferredWidth: 200
                }
            }
        }
    }
    Rectangle {
        id: buttonBackground
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 50
        color: "#ff00d4ff"
        z: 0
    }
    RowLayout {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 15
        spacing: 10
        
        Button {
            id: loadButton
            text: "데이터 불러오기"

            onClicked: {
                fileDialog.open()
            }
        }

        Button {
            id: saveButton
            text: "데이터 저장"
            
            onClicked: {
                // date 선택 데이터 추출
                var headlessCheck = "0";
                if (headlessCheckBox.checked) headlessCheck = "1";

                var selectedDate = "";
                if (day1.checked) { selectedDate = 0; }
                else if (day2.checked) { selectedDate = 1; }
                else if (day3.checked) { selectedDate = 2; }
                else if (otherDateRadio.checked) { selectedDate = otherDateText.text; }
                
                // 나머지 입력 필드 값 추출
                var bankName = bankComboBox.currentText;
                var phoneNumber = phoneNumText.text;
                var birthDate = birthDateText.text;
                var repeatInterval = repeatIntervalText.text;
                var bookingSite = bookingSiteText.text;
                var profileName = profileText.text;
                
                var selectedDevice = "";
                if (cpuRadio.checked) { selectedDevice = "cpu"; }
                else if (gpuRadio.checked) { selectedDevice = "cuda:0"; }
                else if (handRadio.checked) { selectedDevice = "hand"; }
                else if (otherDeviceRadio.checked) { selectedDevice = otherDeviceRadio.text; }

                //if (phoneNumber.length < 10 || phoneNumber.length > 11) {
                //    errorDialog.text = "전화번호는 10~11자리 숫자여야 합니다.";
                //    errorDialog.open();
                //    return;
                //}
                //if (birthDate.length !== 6) {
                //    errorDialog.text = "생년월일은 6자리 숫자로 입력해야 합니다.";
                //    errorDialog.open();
                //    return;
                //}

                var loginMethodType = "";
                if (melonSector.checked) { loginMethodType = melonSector.text; }
                else if (kakaoSector.checked) { loginMethodType = kakaoSector.text; }
                var idData = idText.text;
                var pwData = pwText.text;
                var telegramBotData = telegramBotText.text;
                var telegramChannelData = telegramChannelText.text;
                var asSeatLimitTextData = asSeatLimitText.text;

                var selectedPayment = "";
                if (manualRadio.checked) { selectedPayment = "manual"; }
                else if (bankSendRadio.checked) { selectedPayment = "bank"; }
                else if (kakaoPayRadio.checked) { selectedPayment = "kakaopay"; }

                // Python 함수 호출
                dataHandler.saveData(
                    headlessCheck,
                    selectedDate,
                    bankName,
                    phoneNumber,
                    birthDate,
                    repeatInterval,
                    bookingSite,
                    profileName,
                    selectedDevice,
                    loginMethodType,
                    idData,
                    pwData,
                    telegramBotData,
                    telegramChannelData,
                    asSeatLimitTextData,
                    selectedPayment
                );
                successDialog.text = profileName+"_data.txt로 저장 완료되었습니다."
                successDialog.open()
            }
            MessageDialog {
                id: errorDialog
                title: "입력 오류"
                buttons: MessageDialog.Ok
            }
            MessageDialog {
                id: successDialog
                title: "알림"
                buttons: MessageDialog.Ok
            }
        }

        FileDialog {
            id: fileDialog
            nameFilters: ["Text files (*_data.txt)"]
            // currentFolder: StandardPaths.standardLocations(StandardPaths.displayName)[0]
            onAccepted: {
                console.log("선택된 파일:", selectedFile.toString().replace("file:///", ""))
                dataHandler.loadData(selectedFile.toString().replace("file:///", ""))
            }
        }

        // 데이터가 Python에서 불려왔을 때 UI에 채워넣기
        Connections {
            target: dataHandler
            function onDataLoaded(headlessCheck, date, bank, phonenum, birth, repeat, site, profile, device,
                                    loginMethod, idData, pwData, telegramBot, telegramChannel, asSeatLimit, payment
                                ) {
                
                if (headlessCheck === "0") {
                    headlessCheckBox.checked = false
                } else if (headlessCheck === "1") {
                    headlessCheckBox.checked = true
                }

                if (loginMethod === melonSector.text) {
                    melonSector.checked = true
                } else if (loginMethod === kakaoSector.text) {
                    kakaoSector.checked = true
                }
                idText.text = idData
                pwText.text = pwData
                telegramBotText.text = telegramBot
                telegramChannelText.text = telegramChannel
                asSeatLimitText.text = asSeatLimit

                // date 선택 라디오 버튼 및 텍스트 필드 업데이트
                if (date === "0") {
                    day1.checked = true
                } else if (date === "1") {
                    day2.checked = true
                } else if (date === "2") {
                    day3.checked = true
                } else {
                    otherDateRadio.checked = true
                    otherDateText.text = date // 기본값으로 텍스트필드에 값 넣기
                }
            
                // ComboBox 및 일반 텍스트 필드 업데이트
                var bankIndex = -1
                    for (var i = 0; i < bankComboBox.model.length; i++) {
                        if (bankComboBox.model[i] === bank) {
                            bankIndex = i
                            break
                        }
                    }
                    // 찾은 인덱스로 콤보박스 항목 변경
                    if (bankIndex !== -1) {
                        bankComboBox.currentIndex = bankIndex
                    }
                phoneNumText.text = phonenum
                birthDateText.text = birth
                repeatIntervalText.text = repeat
                bookingSiteText.text = site
                profileText.text = profile

                if (device.startsWith("기타:")) {
                    otherDeviceRadio.checked = true
                    otherDeviceRadio.text = device.substring(device.indexOf(":") + 2)
                } else if (device === 'cpu') {
                    cpuRadio.checked = true
                } else if (device === 'cuda:0') {
                    gpuRadio.checked = true
                } else if (device === 'hand') {
                    handRadio.checked = true
                } else {
                    otherDateRadio.checked = false
                    cpuRadio.checked = false
                    gpuRadio.checked = false
                    handRadio.checked = false
                    otherDeviceRadio.text = device // 기본값으로 텍스트필드에 값 넣기
                }

                if (payment === 'bank') {
                    bankSendRadio.checked = true
                } else if (payment === 'kakaopay') {
                    kakaoPayRadio.checked = true
                } else {
                    manualRadio.checked = true
                }
                
            }
        }
    }
}