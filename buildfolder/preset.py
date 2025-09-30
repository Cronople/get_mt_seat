def getPreset(profile):

    config = {}
    with open(f'./data/{profile}_data.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                config[key] = value
    print('Preset data loading complete')
    
    items = []
    with open(f'./data/{profile}_sector.txt', "r", encoding="utf-8") as f:
        for line in f:
            grade, area, direction, text = line.strip().split("|")
            items.append({
                "gradeData": grade, # 등급(VIP, 일반석 등)
                "sectorType": area, # 구역명으로 할지, 순서로 유형 선택
                "directionData": direction, # 구역 우선 조사 방향
                "textData": text # 구역명
            })
        config['sectorList'] = items
    print('Sector data loading complete')
    
    print(f"프로필: {config['profile']}\n보안문자처리 방식: {config['device']}\n사용 아이디: {config['id']}\n선택 날짜: {config['date']}")

    return config