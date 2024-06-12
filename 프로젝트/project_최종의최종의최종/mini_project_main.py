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
index = 0

def league_start():
    global stacks, stacks_goal, stacks_goal_mi, win, lose, draw, point
    point = [0] * len(teams) # 승점 초기화
    for i in range(len(stacks)):
        # 각 팀은 나머지 모든 팀과 한 번씩 경기를 진행
        for j in range(i + 1, len(stacks)):
            goal_i = random.randint(0, 6) # i의 득점 j의 실점
            goal_j = random.randint(0, 6) # j의 득점 i의 실점
            stacks_goal[i] += goal_i # 득점
            stacks_goal[j] += goal_j # 득점
            stacks_goal_mi[i] += goal_j # 실점
            stacks_goal_mi[j] += goal_i # 실점
            if goal_i > goal_j:
                stacks[i].append(1) # 승리 1 패배 0
                stacks[j].append(0)
            elif goal_j > goal_i:
                stacks[j].append(1)
                stacks[i].append(0)
            elif goal_i == goal_j:
                stacks[i].append(2) # 무승부 2
                stacks[j].append(2)

    for i in range(len(stacks)):
        for result in stacks[i][1:]:
            if result == 1:
                win[i] += 1
            elif result == 0:
                lose[i] += 1
            elif result == 2:
                draw[i] += 1
        point[i] = win[i] * 3 + draw[i]

    # 결과를 파일에 쓰기
    output_dir = os.path.join(script_dir, "league")  # 디렉토리 경로
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 고유한 파일 이름 생성
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"league_results_{current_time}.txt")

    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(len(stacks)):
            f.write("%s의 " % teams[i] + ": ")
            f.write("경기수: 9 ")
            f.write("승: %d " % win[i])
            f.write("패: %d " % lose[i])
            f.write("무: %d " % draw[i])
            f.write("득점: %d " % stacks_goal[i])
            f.write("실점: %d " % stacks_goal_mi[i])
            f.write("득실차: %d " % (stacks_goal[i] - stacks_goal_mi[i]))
            f.write("승점: %d" % point[i])
            f.write("\n") # 줄 바꿈

    # 파일이 20개가 넘으면 가장 오래된 파일 삭제
    files = os.listdir(output_dir)
    txt_files = [f for f in files if f.endswith('.txt')]
    if len(txt_files) > 20:
        txt_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))
        os.remove(os.path.join(output_dir, txt_files[0]))

def league_reload():  # 리그를 다시 시작할 때 변수를 초기화
    global stacks, stacks_goal, stacks_goal_mi, win, lose, draw, point
    stacks = [[team] for team in teams] # 각 팀의 기록을 저장할 리스트 초기화
    stacks_goal = [0] * len(teams) # 득점 수 초기화
    stacks_goal_mi = [0] * len(teams) # 실점 수 초기화
    win = [0] * len(teams) # 승 횟수 초기화
    lose = [0] * len(teams) # 패 횟수 초기화
    draw = [0] * len(teams) # 무 횟수 초기화
    point = [0] * len(teams) # 승점 초기화

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
    output_dir = os.path.join(script_dir, "league")
    files = os.listdir(output_dir)
    txt_file = [f for f in files if f.endswith('.txt')]
    txt_file.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
    return txt_file

def file_count():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    league_dir = os.path.join(current_dir, 'league')
    
    if not os.path.exists(league_dir):
        return 0
    
    txt_files = [f for f in os.listdir(league_dir) if f.endswith('.txt')]
    num_txt_files = len(txt_files) # 저장된 파일의 개수
    return num_txt_files