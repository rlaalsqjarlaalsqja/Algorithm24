# 1.맨체스터 시티
# 2.리버풀
# 3.아스널
# 4.애스턴빌라
# 5.토트넘
# 6.첼시
# 7.맨체스터 유나이티드
# 8.에버턴
# 9.뉴캐슬
# 10.울브스

# 랜덤으로 경기(딕셔너리)(1번씩 경기이므로 1번 경기하면 경기 안하게)
# 승패 리스트에 저(리스트?)(랜덤으로)
# 득실차 저장(리스트?)(넣은 골, 먹힌 골, 득실 차)
# 승정 계산하여 저장(승패로 승점 계산)
import random
import os
from datetime import datetime

# 현재 스크립트 파일의 디렉토리 경로
script_dir = os.path.dirname(os.path.abspath(__file__))
league_dir = os.path.join(script_dir, "league")
goal_dir = os.path.join(script_dir, "goal")

index = 0

teams = [
    "맨체스터 시티",
    "리버풀",
    "아스널",
    "애스턴빌라",
    "토트넘",
    "첼시",
    "맨체스터 유나이티드",
    "에버턴",
    "뉴캐슬",
    "울브스"
]

stacks = [[team] for team in teams] # 컴프리헨션으로 스택을 리스트로 만듬
stacks_goal = [0] * len(teams) # 득점 수
stacks_goal_mi = [0] * len(teams) # 실점 수
win = [0] * len(teams) # 승 횟수
lose = [0] * len(teams) # 패 횟수
draw = [0] * len(teams) # 무 횟수
point = [0] * len(teams) # 승점

if not os.path.exists(goal_dir):
    os.makedirs(goal_dir)

def league_start():
    global stacks, stacks_goal, stacks_goal_mi, win, lose, draw, point
    point = [0] * len(teams) # 승점 초기화
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    goal_file_path = os.path.join(goal_dir, f"game_{current_time}.txt")
    
    with open(goal_file_path, 'w', encoding='utf-8') as goal_file:
        for i in range(len(stacks)):
            # 각 팀은 나머지 모든 팀과 한 번씩 경기를 진행
            for j in range(i + 1, len(stacks)):
                goal_i = random.randint(0, 6) # i의 득점 j의 실점
                goal_j = random.randint(0, 6) # j의 득점 i의 실점
                stacks_goal[i] += goal_i # 득점
                stacks_goal[j] += goal_j # 득점
                stacks_goal_mi[i] += goal_j # 실점
                stacks_goal_mi[j] += goal_i # 실점
                
                # 결과를 파일에 기록
                goal_file.write(f"Team {teams[i]} vs Team {teams[j]}\n")
                goal_file.write(f"Team {teams[i]} goals: {goal_i}\n")
                goal_file.write(f"Team {teams[j]} goals: {goal_j}\n")
                goal_file.write("\n")
                
                # 경기 결과에 따라 승/패/무 기록
                if goal_i > goal_j:
                    stacks[i].append(1) # 승리 1 패배 0
                    stacks[j].append(0)
                elif goal_j > goal_i:
                    stacks[j].append(1)
                    stacks[i].append(0)
                else: # goal_i == goal_j
                    stacks[i].append(2) # 무승부 2
                    stacks[j].append(2)

    # 승/패/무 기록을 포인트로 변환
    for i in range(len(stacks)):
        for result in stacks[i][1:]:
            if result == 1:
                win[i] += 1
            elif result == 0:
                lose[i] += 1
            elif result == 2:
                draw[i] += 1
        point[i] = win[i] * 3 + draw[i]

    # 리그 결과를 파일에 쓰기
    if not os.path.exists(league_dir):
        os.makedirs(league_dir)

    # 고유한 파일 이름 생성
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(league_dir, f"league_results_{current_time}.txt")

    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(len(stacks)):
            f.write(f"{teams[i]}의 ")
            f.write(f"승: {win[i]} ")
            f.write(f"패: {lose[i]} ")
            f.write(f"무: {draw[i]} ")
            f.write(f"득점: {stacks_goal[i]} ")
            f.write(f"실점: {stacks_goal_mi[i]} ")
            f.write(f"득실차: {stacks_goal[i] - stacks_goal_mi[i]} ")
            f.write(f"승점: {point[i]}\n")

    
    manage_file_limit(league_dir, 20)
    manage_file_limit(goal_dir, 20)

def league_reload():  # 리그를 다시 시작할 때 변수를 초기화
    global stacks, stacks_goal, stacks_goal_mi, win, lose, draw, point
    stacks = [[team] for team in teams] # 각 팀의 기록을 저장할 리스트 초기화
    stacks_goal = [0] * len(teams) # 득점 수 초기화
    stacks_goal_mi = [0] * len(teams) # 실점 수 초기화
    win = [0] * len(teams) # 승 횟수 초기화
    lose = [0] * len(teams) # 패 횟수 초기화
    draw = [0] * len(teams) # 무 횟수 초기화
    point = [0] * len(teams) # 승점 초기화

def manage_file_limit(directory, limit): # 리그 결과 파일이 20개가 넘으면 가장 오래된 파일 삭제
    files = os.listdir(directory)
    txt_files = [f for f in files if f.endswith('.txt')]
    if len(txt_files) > limit:
        txt_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        while len(txt_files) > limit:
            os.remove(os.path.join(directory, txt_files.pop(0)))

def statistics_search():
    output_dir = os.path.join(script_dir, "league")
    txt_files = index_files()

    if txt_files:
        last_integer = []
        # 가장 최신 파일 읽기
        latest_file = txt_files[index]
        file_path = os.path.join(output_dir, latest_file)

        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 팀별 승점 추출
        for line in lines:
            parts = line.split()  # 각 줄을 공백으로 분할하여 리스트로 만듭니다.
            last_integer.append(int(parts[-1]))  # 리스트의 마지막 요소를 정수로 변환합니다.
        
        sort_index = Sort(last_integer)
        return sort_index

    else:
        print("경기 결과 없음")

def statistics_before() :
    global index
    index += 1
    if index >= file_count() :
            index -= 1
            return 1
    else :
        return 1

def statistics_next() :
    global index
    index -= 1
    if index < 0:
        index += 1
        return 1
    else:
        return 1

def Sort(number) :
    indexed_list = list(enumerate(number))
    sorted_indexed_list = sorted(indexed_list, key=lambda x: x[1], reverse=True)
    sorted_index = [index for index, value in sorted_indexed_list]
    return sorted_index

def index_files():
    # output_dir 변수에는 현재 스크립트가 위치한 디렉토리(script_dir)에 "league"라는 하위 디렉토리를 포함한 경로가 저장됩니다.
    output_dir = os.path.join(script_dir, "league")

    # output_dir 디렉토리에 있는 파일과 디렉토리 목록을 가져옵니다.
    files = os.listdir(output_dir)

    # 파일 목록(files) 중에서 확장자가 '.txt'인 파일들만 필터링하여 txt_file 리스트에 저장합니다.
    txt_file = [f for f in files if f.endswith('.txt')]

    # txt_file 리스트에 있는 파일들을 수정된 시간을 기준으로 내림차순으로 정렬합니다.
    # 정렬 기준은 파일의 수정 시간(os.path.getmtime)을 사용합니다.
    # reverse=True 옵션을 통해 내림차순으로 정렬합니다.
    txt_file.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)

    # 정렬된 파일 리스트를 반환합니다.
    return txt_file

def index_goal_files():
    # output_dir 변수에는 현재 스크립트가 위치한 디렉토리(script_dir)에 "league"라는 하위 디렉토리를 포함한 경로가 저장됩니다.
    output_dir = os.path.join(script_dir, "goal")

    # output_dir 디렉토리에 있는 파일과 디렉토리 목록을 가져옵니다.
    files = os.listdir(output_dir)

    # 파일 목록(files) 중에서 확장자가 '.txt'인 파일들만 필터링하여 txt_file 리스트에 저장합니다.
    txt_file = [f for f in files if f.endswith('.txt')]

    # txt_file 리스트에 있는 파일들을 수정된 시간을 기준으로 내림차순으로 정렬합니다.
    # 정렬 기준은 파일의 수정 시간(os.path.getmtime)을 사용합니다.
    # reverse=True 옵션을 통해 내림차순으로 정렬합니다.
    txt_file.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)

    # 정렬된 파일 리스트를 반환합니다.
    return txt_file

def file_count():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    league_dir = os.path.join(current_dir, 'league')
    
    if not os.path.exists(league_dir):
        return 0
    
    txt_files = [f for f in os.listdir(league_dir) if f.endswith('.txt')]
    num_txt_files = len(txt_files) # 저장된 파일의 개수
    return num_txt_files

def file_search(index):
    search_file = index_files()  # search_file[0]은 가장 최신의 파일 데이터
    file_name = search_file[index]
    file_path = os.path.join(script_dir, "league", file_name)
    
    data = []  # 이중 리스트를 저장할 리스트
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()  # 각 줄을 공백으로 분할하여 리스트로 만듭니다.
            int_parts = []
            for part in parts:
                try:
                    int_parts.append(int(part))  # 정수로 변환하여 리스트에 추가합니다.
                except ValueError:
                    # 정수로 변환할 수 없는 경우 무시합니다.
                    continue
            data.append(int_parts)  # 변환된 데이터를 data 리스트에 추가합니다.
            
    return data

def goal_file_search(index, team_name):
    # 최신 파일들을 리스트로 가져옵니다. goal_files[0]이 가장 최신의 파일 데이터입니다.
    goal_files = index_goal_files()
    
    # index에 해당하는 파일 이름을 가져옵니다.
    goal_file_name = goal_files[index]
    
    # goal 파일의 경로를 만듭니다.
    goal_file_path = os.path.join(script_dir, "goal", goal_file_name)
    
    # 결과를 저장할 리스트입니다.
    team_results = []

    # goal 파일을 읽기 모드로 엽니다.
    with open(goal_file_path, 'r', encoding='utf-8') as file:
        # 파일의 각 줄을 반복합니다.
        for line in file:
            # 줄 양쪽의 공백 문자를 제거합니다.
            line = line.strip()
            
            # 'Team'으로 시작하는 줄을 찾습니다.
            if line.startswith('Team'):
                # 팀 이름을 ' vs '로 분할합니다.
                teams = line.split(' vs ')
                
                # 팀이 두 개 있는지 확인합니다.
                if len(teams) == 2:
                    # 각 팀의 이름을 추출합니다.
                    team1, team2 = teams[0].replace('Team ', ''), teams[1].replace('Team ', '')
                    
                    # 다음 줄을 읽어서 팀1의 골 수를 추출합니다.
                    goals1 = int(file.readline().strip().split(': ')[1])
                    
                    # 그 다음 줄을 읽어서 팀2의 골 수를 추출합니다.
                    goals2 = int(file.readline().strip().split(': ')[1])
                    
                    # 팀 이름이 원하는 팀 이름과 일치하는지 확인합니다.
                    if team1 == team_name or team2 == team_name:
                        # 결과 리스트에 경기 결과를 추가합니다.
                        team_results.append({'team1': team1, 'team2': team2, 'goals1': goals1, 'goals2': goals2})
    
    # 결과를 형식화합니다.
    formatted_results = format_match_results(team_results)
    
    # 형식화된 결과를 반환합니다.
    return formatted_results

# 경기 결과를 형식화하는 함수
def format_match_results(results):
    formatted_results = []
    # 각 경기 결과를 반복합니다.
    for match in results:
        # 팀 이름과 골 수를 가져옵니다. 키가 없을 경우 기본값을 사용합니다.
        team1 = match.get('team1', 'Unknown Team 1')
        team2 = match.get('team2', 'Unknown Team 2')
        goals1 = match.get('goals1', 0)
        goals2 = match.get('goals2', 0)
        
        # 형식화된 문자열을 만들어 리스트에 추가합니다.
        formatted_results.append(f"{team1} {goals1} : {goals2} {team2}")
    
    # 형식화된 결과 리스트를 반환합니다.
    return formatted_results






