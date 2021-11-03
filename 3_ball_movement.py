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
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
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
character_to_x = 0 #좌우니까 x만

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
ball_speed_y = [-18, -15, -12, -9] #index 0(공1),1(공2),2(공3),3(공4)

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




#2. 이벤트 루프
running = True #게임 진행 여부
while running:
    dt = clock.tick(60) # 게임 화면의 초당 프레임 수를 설정

    #3. 이벤트 처리 
    for event in pygame.event.get(): #event.get()을 통해 사용자의 움직임을 받음
        if event.type == pygame.QUIT: #창의 x버튼
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed

            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    #4. 게임 캐릭터 위치 (가로/세로 경계값)
    character_x_pos += character_to_x #캐릭터의 위치는 키보드로 움직인 만큼의 위치

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


    #타이머 집어 넣기 ( 경과 시간 )

    # 글자 실제 반영 (시간, True, 글자 색상 (*고정))

    # 시간 처리

    pygame.display.update() #화면을 계속해서 그려주는 함수

#시간 오버 게임 종료시 약간의 텀을 주고 종료
pygame.time.delay(2000)

# 게임 종료시 pygame 종료
pygame.quit()