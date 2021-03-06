import pygame
import random
from time import sleep

# 배경색과 창크기 설정
BGcolor = (255,255,255)
width = 512
height = 700
BG_height = 700
unit_width= 86
unit_height= 79
enemy_width= 67
enemy_height= 89
fireball1_width = 61
fireball1_height = 140
fireball2_width = 59
fireball2_height = 86

# 킬 점수 카운트하는 변수입니다.
enemy_kill = 0

#게임오버 카운트 표시
def Score(count):
    global gamepad
    font=pygame.font.SysFont(None,25)
    text=font.render("pass : "+str(count),True,BGcolor)
    gamepad.blit(text,(0,15))

#킬점수 표시입니다.
def killScore(count):
    global gamepad
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score : " + str(count), True, BGcolor)
    gamepad.blit(text, (0, 0))

# 텍스트의 폰트와 크기등을 결정하고 2초 슬립시킵니다
def dispMessage(text):
    waiting = True
    global gamepad
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((width / 2), (height / 2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()

# 게임 오버 표시
def gameOver():
    global gamepad
    dispMessage('GAME OVER')

def crash():
    global gamepad
    dispMessage('Crashed!')
    
# 텍스트를 출력하는 함수입니다.
def textObj(text, font):
    textSurface = font.render(text,True,[255,0,0])
    return textSurface, textSurface.get_rect()

# 게임에 집어넣을 객체를 만드는 함수
def into_Game(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def runGame():
    global gamepad,clock,unit,BG,BG1
    global enemy,fires,bullet,boom,effect
    global enemy_kill

    is_enemy_dead=False
    enemy_kill = 0
    boom_count=0
    effect_count = 0
    # 적이 파괴되지 않고 지나간 횟수 카운트하는 변수
    enemy_passed=0
    bullet_xy=[]
    # 비행기 좌표설정
    x = width*0.37
    y = height*0.8
    # 비행기 좌표를 변경할 변수 선언
    changeX = 0
    changeY = 0
    # 비행기 이동을 위한 변수 선언
    x_switch = 0  # 0이면 정지, 1이면 좌측, 2면 우측으로 이동하도록 하기위한 변수입니다.
    y_switch = 0  # 0이면 정지, 1이면 위, 2면 아래로 이동하도록 하기위한 변수입니다.
    x_save = 0  # 좌,우키 2개가 눌렸을시 먼저 누른 키를 기억하기 위한 변수입니다.
    y_save = 0  # 상,하키 2개가 눌렸을시 먼저 누른 키를 기억하기 위한 변수입니다.
    x_doublekey = 0  # X축 이동시 2개이상의 키가 눌렸는지 확인하기 위한 변수입니다.
    y_doublekey = 0  # Y축 이동시 2개이상의 키가 눌렸는지 확인하기 위한 변수입니다.
    # 총알 발사를 위한 변수 선언
    attack = 0  # 1이면 총알을 발사하고 0이면 멈춥니다.
    attack_count = 5  # 총알이 나가는 주기를 설정합니다.
    # 적 hp를 생성하기 위한 변수입니다.
    enemy_hp = 2
    enemy_hpc = 0

    # 배경화면 설정
    BG_X = 0
    BG_X2 = -BG_height
    # 적, 방해물 위치 지정
    enemy_x = random.randrange(0,width-67)
    enemy_y = -67
    fire_x = random.randrange(0,width)
    fire_y = -140
    random.shuffle(fires)
    fire = fires[0]
    PrintScore = False # 적 파괴시 점수 출력
    y_change = 0
    x_change = 0

    #플래그 설정
    crashe=False
    while not crashe:
        # event.get()은 게임에서 발생하는 이벤트 반환하는 함수입니다.
        for event in pygame.event.get():
            # 마우스로 창을 닫을경우 플래그를 설정하여 while문을 빠져나옵니다.
            if event.type == pygame.QUIT:
                quit()
            # 키입력시 x좌표를 업데이트함
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    if x_switch == 2:  # 현재 우측으로 움직이고 있을때 왼쪽 키를 누른다면
                        x_doublekey = 1  # 좌, 우키 2개 누른거고
                        x_save = x_switch  # 우측으로 먼저 움직이고 있었음을 기억한 후
                        x_switch = 1  # 좌측으로 움직이도록 합니다.
                    else:
                        x_switch = 1  # 아니면 그냥 왼쪽으로 움직이면 됩니다.
                elif(event.key == pygame.K_RIGHT):
                    if x_switch == 1:
                        x_doublekey = 1
                        x_save = x_switch
                        x_switch = 2
                    else:
                        x_switch = 2
                elif event.key == pygame.K_DOWN:
                    if y_switch == 1:  # 위로 움직이고 있을때 아래키를 누른다면
                        y_doublekey = 1  # 위, 아래키 2개 누른거고
                        y_save = y_switch  # 위쪽으로 먼저 움직이고 있었음을 기억한 후
                        y_switch = 2  # 아래로 움직이도록 합니다.
                    else:
                        y_switch = 2
                elif event.key == pygame.K_UP:
                    if y_switch == 2:
                        y_doublekey = 1
                        y_save = y_switch
                        y_switch = 1
                    else:
                        y_switch = 1
                # Z키를 누르면 총알 발사
                elif event.key == pygame.K_z:
                    attack = 1
                # 일시 정지 5초
                elif(event.key==pygame.K_SPACE):
                    sleep(5)
            # 방향키를 동시에 눌렀을때 버벅임을 없애느라 코드가 길어졌습니다
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if y_doublekey == 1:  # 아래, 위키 2개 눌려있는상황에서 위 키를 뗐을때
                        if y_save == 2:  # 먼저 눌린 키가 아래방향이면
                            y_switch = 2  # 아래로 움직이게 만듭니다.
                            y_doublekey = 0  # 그리고 키가 2개 눌리지 않았음을 표시합니다.
                        elif y_save == 1:  # 먼저 눌린키가 위 키면
                            y_switch = 2  # 아래키는 눌린 상태이니 아래로 움직이게 만들고
                            y_doublekey = 0  # 키가 2개 눌리지 않았았음을 표시합니다.
                    else:
                        y_switch = 0  # 키가 2개 눌린게 아닌경우 그냥 멈추면 됩니다.
                if event.key == pygame.K_DOWN:
                    if y_doublekey == 1:
                        if y_save == 2:
                            y_switch = 1
                            y_doublekey = 0
                        elif y_save == 1:
                            y_switch = 1
                            y_doublekey = 0
                    else:
                        y_switch = 0
                if event.key == pygame.K_LEFT:
                    if x_doublekey == 1:  # 좌, 우키 2개 눌렸을때
                        if x_save == 2:  # 먼저 눌린 키가 우측 키라면
                            x_switch = 2  # 우측으로 움직이게 만들고
                            x_doublekey = 0  # 더블키를 초기화
                        elif x_save == 1:  # 먼저 눌린 키가 좌측 키라면
                            x_switch = 2  # 우측으로 움직이게 만들고
                            x_doublekey = 0  # 더블키를 초기화
                    else:
                        x_switch = 0  # 키 2개 눌린게 아니면 그냥 멈추면 됩니다.
                if event.key == pygame.K_RIGHT:
                    if x_doublekey == 1:
                        if x_save == 2:
                            x_switch = 1
                            x_doublekey = 0
                        elif x_save == 1:
                            x_switch = 1
                            x_doublekey = 0
                    else:
                        x_switch = 0
                # z키를 떼면 총알 발사를 중지합니다.
                if event.key == pygame.K_z:
                    attack = 0

            if y_switch == 0:  # 스위치가 0이면
                y_change = 0  # 멈춰있고
            elif y_switch == 1:  # 스위치가 1이면
                y_change = -5  # 5만큼 위로
            elif y_switch == 2:  # 스위치가 2면
                y_change = 5  # 5만큼 아래로

            if x_switch == 0:
                x_change = 0
                unit = pygame.image.load('images/c.png')
            elif x_switch == 1:
                x_change = -5
                unit = pygame.image.load('images/c_l.png')  # 좌측으로 움직일때 이미지
            elif x_switch == 2:
                x_change = 5
                unit = pygame.image.load('images/c_r.png')  # 우측으로 움직일때 이미지

        y += y_change
        x += x_change
        # 총알 발사 함수입니다.
        if attack == 1:
            if attack_count == 5:
                bulletX = x + (unit_width / 2) - 18
                bulletY = y
                bullet_xy.append([bulletX, bulletY])
                attack_count = 0  # 총알을 발사했으면 카운트를 0으로 만들고
            else:
                attack_count += 1  # 카운트가 목표 수치까지 도달하는데 걸리는 시간이 총알 주기가 됩니다.

        # 비행기가 배경화면을 넘어가지 않게 하는 if문
        y += y_change
        if y < 0:
            y = 0
        elif y > height - unit_height:
            y = height - unit_height

        x += x_change
        if x < 0:
            x = 0
        elif x > width - unit_width:
            x = width - unit_width

        # 게임판을 흰색으로 채우기
        gamepad.fill(BGcolor)
        BG_X += 5
        BG_X2 += 5

        if BG_X == BG_height:
            BG_X = -BG_height
        if BG_X2 == BG_height:
            BG_X2 = -BG_height

        # 배경화면 호출함.
        into_Game(BG,0,BG_X)
        into_Game(BG1,0,BG_X2)
        
        # 적이 지나간 횟수 표시
        Score(enemy_passed)

        # 킬스코어 표시
        killScore(enemy_kill)
        
        # 적이 2번 이상 지나가면 게임오버 표시
        if enemy_passed > 2:
            gameOver()
            break

        # 적이 화면을 넘어가면 재생성하는 if문
        enemy_y += 6
        if enemy_y >= height:
            # 적이 파괴되지 않고 지나가면 카운트 1씩 증가
            enemy_passed += 1
            enemy_x = random.randrange(0,width-108)
            enemy_y = -67
            enemy_hp = 2

        # 방해물이 없다면 방해물이 나오는 속도를 조절하는 함수
        if fire == None:
            fire_y += 50
        else:
            fire_y += 10
        if fire_y >= height:
            fire_x = random.randrange(0,width-61)
            fire_y = -140
            random.shuffle(fires)
            fire=fires[0]

        # enumerate는 튜플형태로 반환한다 [인덱스,값]
        if len(bullet_xy) != 0:
            for index,positon in enumerate(bullet_xy):
                positon[1] -= 15
                bullet_xy[index][1] = positon[1]
                # 총알이 적에 명중
                if positon[1]<enemy_y:
                    if positon[0] > enemy_x and positon[0] < enemy_x + enemy_width:
                        enemy_hpc = 1
                        if is_enemy_dead == False:  # 적이 파괴되면 총알을 막지 않습니다.
                            into_Game(effect, enemy_x, enemy_y)
                            bullet_xy.remove(positon)
                            effect_count += 1
                            if effect_count > 5:
                                effect_count = 0
                            if enemy_hp == 0:  # hp가 0이되면
                                enemy_kill += (700-y)/2  # 킬점수+가산점 추가하고
                                KillPlus = (700-y)/2
                                is_enemy_dead=True  # 적을 사망처리
                                PrintScore = True  # 점수 출력
                # 총알 배열에서 
                if positon[1] <= -50:
                    try:
                        bullet_xy.remove(positon)
                    except:
                        pass

        # 적 파괴시 가산점 점수 표시
        if PrintScore == True:
            def plusScore(count):
                global gamepad
                font = pygame.font.SysFont(None, 30)
                text = font.render("+ " + str(count), True, [0,0,255])
                gamepad.blit(text, (enemy_x, enemy_y + 90))

            plusScore(KillPlus)

        #  적 hp를 1씩 감소시키는 과정입니다
        if enemy_hpc == 1:
            enemy_hp -= 1
            enemy_hpc = 0

        # 적이 폭발하는 과정입니다.
        if not is_enemy_dead:
            into_Game(enemy,enemy_x,enemy_y)
        else:
            into_Game(boom,enemy_x,enemy_y)
            boom_count += 1
            if boom_count > 20:
                boom_count = 0
                enemy_x = random.randrange(0,width-108)
                enemy_y = -67
                enemy_hp = 2  # hp를 초기화 시켜줍니다.
                is_enemy_dead=False
                PrintScore = False  #점수출력도 끝!
        # 적과 기체가 충돌했는지 확인하고 충돌이면 게임오버
        if is_enemy_dead==False:  # 적 파괴시 잔해에 죽지 않도록 조치
            if (y+19 < enemy_y + enemy_height and y+19 > enemy_y)or(y+unit_height-19>enemy_y and y+unit_height-19<enemy_y+enemy_height):
                if (x+13<enemy_x+enemy_width and x+13>enemy_x):
                    crash()
                    break
                elif (x+unit_width-13 > enemy_x and x+unit_width-13<enemy_x+enemy_width):
                    crash()
                    break
                elif (enemy_x > x and enemy_x+enemy_width < x + unit_width):
                    crash()
                    break
        # 적과 파이어볼이 충돌했는지 확인하고 충돌이면 게임오버
        if fire[1]!=None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height

            if (y < fire_y + fireball_height and y > fire_y) or (
                    y + unit_height > fire_y and y + unit_height < fire_y + fireball_height):
                if (x < fire_x + fireball_width and x > fire_x):
                    crash()
                    break
                elif (x + unit_width > fire_x and x + unit_width < fire_x + fireball_width):
                    crash()
                    break
                elif (fire_x > x and fire_x + fireball_width < x + unit_width):
                    crash()
                    break

        # 적과 방해물 호출
        into_Game(enemy,enemy_x,enemy_y)
        if fire[1] != None:
            into_Game(fire[1],fire_x,fire_y)

        if len(bullet_xy)!=0:
            for bx,by in bullet_xy:
                into_Game(bullet,bx,by)
        # 비행기 호출함.
        into_Game(unit,x,y)

        # 게임판을 그림
        pygame.display.update()
        #fps 60으로 설정합니다,
        clock.tick(60)

    sleep(2)
    GameOver()  # 죽어서 break로 for을 빠져나오면 2초 멈췄다가 게임오버화면을 출력합니다.
    # 초기화한 pygame종료합니다.
    pygame.quit()
    quit()

def gameoverScore(count):  # 게임오버시 스코어를 표현하기위한 함수입니다.
    global gamepad
    font = pygame.font.SysFont(None, 40)
    text = font.render(" " + str(count), True, [0,0,255])
    gamepad.blit(text, (265, 238))

def GameOver():
    global GOBG
    GReset = False

    while GReset == False:  # 화면 안넘어가게(종료안되게)막아주는 장치입니다.
        into_Game(GOBG, 0, 0)
        gameoverScore(enemy_kill)
        pygame.display.update()    # 게임오버화면 호출함.
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # 마우스로 창 닫으면 꺼집니다.
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  #  r버튼을 누르면 재시작합니다.
                    runGame()
                if event.key == pygame.K_RETURN:  #  엔터를 누르면 메인으로갑니다.
                    MainTitle()

def MainTitle():
    global maintitle
    GReset = False
    while GReset == False:  # 화면 안넘어가게(종료안되게)막아주는 장치입니다.
        into_Game(maintitle, 0, 0)
        pygame.display.update()    # 게임오버화면 호출함.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 마우스로 창 닫으면 꺼집니다.
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  #  r버튼을 누르면 재시작합니다.
                    runGame()

#게임을 초기화 하고 시작하는 함수입니다.
def initGame():
    #전역 변수로 설정합니다.
    global gamepad,clock,unit,BG,BG1,GOBG,maintitle
    global enemy,fires,bullet,boom,effect
    fires=[]
    #파이게임 라이브러리를 초기화함 꼭 호출해줘야 합니다.
    pygame.init()
    #게임 판 화면 설정
    gamepad=pygame.display.set_mode((width,height))
    # 게임 제목 설정
    pygame.display.set_caption("떴다 떴다 비행기")
    #비행기 이미지 로딩
    unit=pygame.image.load('images/c.png')
    # 배경화면 로딩
    BG = pygame.image.load('images/bg.png')
    BG1 = BG.copy()
    GOBG = pygame.image.load('images/gobg.png')
    maintitle = pygame.image.load('images/maintitle.png')
    # 적 이미지 및 방해물 추가
    enemy=pygame.image.load('images/enemy.png')
    fires.append((0,pygame.image.load('images/fireball.png')))
    fires.append((1,pygame.image.load('images/fireball2.png')))
    # 불덩어리 2개와 None객체 5개 넣을 리스트
    for i in range(5):
        fires.append((i+2,None))
    # 총알이미지 추가
    bullet=pygame.image.load('images/bullet.png')
    # 폭발이미지 추가
    boom=pygame.image.load('images/boom.png')
    effect = pygame.image.load('images/effect.png')
    # 초당 프레임을 위한 변수 생성
    clock = pygame.time.Clock()
    # runGame 함수 호출
    MainTitle()

initGame()
