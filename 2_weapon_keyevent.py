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


#무기 이동 속도
weapon_speed = 10



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




    #5. 충돌 처리


    #6. 화면에 그리기 (.blit)

    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

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