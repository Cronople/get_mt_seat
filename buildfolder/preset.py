def getPreset():
    convert = {'날짜선택': 'date',
               '좌석등급': 'grade', 
               '구역선택': 'sector', 
               '은행명': 'bank', 
               '전화번호(-없이)': 'phonenumber', 
               '생년월일(6자리)': 'birthdate',
               '반복 간격': 'repeat',
               '예매 사이트': 'page'}

    with open('preset.txt', 'r', encoding='utf-8') as idpwFile:
        preset_data = {}

        data = idpwFile.readlines()
        for i in data:
            tempdata = i.split(':')
            value = tempdata[1].strip()
            if value == '':
                preset_data[convert[tempdata[0]]] = ''
            else:
                preset_data[convert[tempdata[0]]] = value
        idpwFile.close()
    
    
    print('-' * 20)
    print(preset_data)
    print('-' * 20)

    return preset_data

getPreset()