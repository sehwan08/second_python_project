import pygame
import os #경로 설정 라이브러리

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



#2. 이벤트 루프
running = True #게임 진행 여부
while running:
    dt = clock.tick(60) # 게임 화면의 초당 프레임 수를 설정

    #3. 이벤트 처리 
    #print("FPS: "+str(clock.get_fps())) # 프레임 속도 확인
    #이 부분도 'pygame' 사용 시 반드시 필요하다 몰라도 된다. 적기만 하자
    for event in pygame.event.get(): #event.get()을 통해 사용자의 움직임을 받음
        if event.type == pygame.QUIT: #창의 x버튼
            running = False


    #4. 게임 캐릭터 위치 (가로/세로 경계값)


    #5. 충돌 처리


    #6. 화면에 그리기 (.blit)

    screen.blit(background, (0,0))
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