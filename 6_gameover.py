import pygame
import os

from pygame.constants import K_RIGHT #경로 설정 라이브러리

pygame.init() # 초기화 반드시 필요 -> 'pygame' 사용 시 반드시 선언

#화면 크기 설정
screen_width = 640 #가로 
screen_height = 480 #세로
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Pang!") #게임 이름

#FPS
clock = pygame.time.Clock()

####################################################################################

#1.사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 폰트, 시간 등)

current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") #현재 파일 위치 + images 폴더 위치 반환

# 배경
background = pygame.image.load(os.path.join(image_path, "background.jpg"))

# 스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.jpg"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지 높이를 알아야 공이 스테이지 사이에서만 움직임

# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 움직임
character_to_x_LEFT = 0 #좌우니까 x만
character_to_x_RIGHT = 0

# 캐릭터 이동 속도
character_speed = 5


# 무기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기 발수 (한번에 여러발 가능)
weapons = []

# 무기 이동 속도
weapon_speed = 10



# 공 (4개를 각각 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png")),
]

# 공 속도 (크기에 따라 속도가 각기 다름)
ball_speed_y = [-18, -15, -13, -12] #index 0(공1),1(공2),2(공3),3(공4)

# 공 정보
balls = []

#최초 발생 큰공 추가
balls.append({
    "pos_x" : 50, #공 x좌표
    "pos_y" : 50, #공 y좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, #공 x축 이동 방향, -3 = 왼쪽, +3 = 오른쪽
    "to_y" : -6, #공 y축 이동 방향
    "init_speed_y" : ball_speed_y[0] #y 최초 속도
})

#사라질 무기, 공 정보
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 40)

total_time = 5
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

#게임 조건 3가지 세팅 / TimeOut/Mission Complete, GameOver
game_result = "Game Over!"


#2. 이벤트 루프
running = True #게임 진행 여부
while running:
    dt = clock.tick(50) # 게임 화면의 초당 프레임 수를 설정

    #3. 이벤트 처리 
    for event in pygame.event.get(): #event.get()을 통해 사용자의 움직임을 받음
        if event.type == pygame.QUIT: #창의 x버튼
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed

            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    #4. 게임 캐릭터 위치 (가로/세로 경계값)
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT #캐릭터의 위치는 키보드로 움직인 만큼의 위치

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] #무기 위치를 올림

    # 무기가 천장에 닿으면 사라짐
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #공이 가로 화면 끝에 맞으면 다시 돌아 오도록
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        #공이 세로(스테이지에 닿을 때)에 맞으면 다시 튕기도록
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]
        else: #공이 다시 튕긴 후 속도가 증가
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    #5. 충돌 처리
    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        #공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        #충돌 체크
        if character_rect.colliderect(ball_rect):
            running = False
            break

        
        #공과 무기들 충돌
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx 
                ball_to_remove = ball_idx

                #가장 작은 공이 아니면 다음 단계의 공으로 나눔
                if ball_img_idx < 3:
                    #현재 공 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보 (인덱스가 커질수록 공이 작아지기때문에 +1)
                    samll_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    samll_ball_width = samll_ball_rect.size[0]
                    samll_ball_height = samll_ball_rect.size[1]

                    #왼쪽으로 쪼개지는 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (samll_ball_width / 2), #공 x좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (samll_ball_height / 2), #공 y좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : -3, #공 x축 이동 방향, -3 = 왼쪽, +3 = 오른쪽
                        "to_y" : -6, #공 y축 이동 방향
                        "init_speed_y" : ball_speed_y[ball_img_idx + 1] #y 최초 속도
                    })
                    #오른쪽으로 쪼개지는 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (samll_ball_width / 2), #공 x좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (samll_ball_height / 2), #공 y좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : +3, #공 x축 이동 방향, -3 = 왼쪽, +3 = 오른쪽
                        "to_y" : -6, #공 y축 이동 방향
                        "init_speed_y" : ball_speed_y[ball_img_idx + 1] #y 최초 속도
                    })
                break
        else: # 게임 계속 진행
            continue #안쪽 for문 조건이 맞지 않으면 continue
        break
            
    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #모든 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False
    

    #6. 화면에 그리기 (.blit)
    screen.blit(background, (0,0))
 
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))


    # 시간 처리
    # 타이머 집어 넣기 ( 경과 시간 )
    # 글자 실제 반영 (시간, True, 글자 색상 (*고정))
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10,10))

    # 시간 초과 시
    if total_time - elapsed_time <= 0:
        game_result =  "Time Over"
        running = False

    pygame.display.update() #화면을 계속해서 그려주는 함수

#시간 오버 게임 종료시 약간의 텀을 주고 종료
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), (int(screen_height / 2))))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)


# 게임 종료시 pygame 종료
pygame.quit()