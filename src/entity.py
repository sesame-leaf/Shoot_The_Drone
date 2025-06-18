import pygame
import math
import sys
import os

class Person:
    def __init__(self, feet_pos:tuple[int, int], size_constant:int):
        """
        Person 클래스 생성자
        
        Args:
            feet_pos: 캐릭터의 발 위치 (bottom center)
            size_constant: 크기 상수
        """
        self.__feet_pos = feet_pos
        self.__size_constant = size_constant
        
        # 다리 속성
        self.__leg_len = 6 * self.__size_constant
        self.__leg_width = 5
        self.__leg_color = "#0000ff"
        
        # 몸통 속성
        self.__torso_len = 5 * self.__size_constant
        self.__torso_width = 7
        self.__torso_color = "#000000"
        
        # 머리 속성
        self.__head_len = 3 * self.__size_constant
        self.__head_width = 5
        self.__head_color = "#fbceb1"
        
        # 팔 속성
        self.__arm_len = 5 * self.__size_constant
        self.__arm_width = 3
        self.__arm_color = "#fbceb1"
        
        # 몸 전체 속성 계산
        self.__body_width = max(self.__leg_width, self.__torso_width, self.__head_width)
        self.__head_height = self.__leg_len + self.__torso_len + self.__head_len
        
        # 어깨 위치 계산 (팔의 회전축)
        self.__global_shoulder_pos = (self.__feet_pos[0], self.__feet_pos[1]-(self.__leg_len + self.__torso_len)+1)
        
        # 팔의 각도와 손의 위치
        self.__arm_angle = 0.0
        self.__hand_pos = (self.__global_shoulder_pos[0], self.__global_shoulder_pos[1])
        
    def move_arm_pos(self, cursor_pos:tuple[int, int]):
        """커서 위치에 따라 팔의 각도와 손 위치 업데이트"""
        # cursor 위치에 따라 arm의 각도를 계산
        dx = cursor_pos[0] - self.__global_shoulder_pos[0]
        dy = cursor_pos[1] - self.__global_shoulder_pos[1]
        
        # 어깨와 커서의 각도 계산
        self.__arm_angle = math.atan2(dy, dx)
        
        # 손 위치 업데이트
        self.__hand_pos = (
            self.__global_shoulder_pos[0] + math.cos(self.__arm_angle) * self.__arm_len,
            self.__global_shoulder_pos[1] + math.sin(self.__arm_angle) * self.__arm_len
        )
        
    def draw(self, screen:pygame.Surface) -> None:
        """캐릭터 그리기"""
        # 다리 그리기
        pygame.draw.line(
            screen, 
            self.__leg_color,
            (self.__feet_pos[0] - self.__leg_width//2, self.__feet_pos[1]),
            (self.__feet_pos[0] - self.__leg_width//2, self.__feet_pos[1] - self.__leg_len),
            self.__leg_width
        )
        pygame.draw.line(
            screen, 
            self.__leg_color,
            (self.__feet_pos[0] + self.__leg_width//2, self.__feet_pos[1]),
            (self.__feet_pos[0] + self.__leg_width//2, self.__feet_pos[1] - self.__leg_len),
            self.__leg_width
        )
        
        # 몸통 그리기
        pygame.draw.line(
            screen,
            self.__torso_color,
            (self.__feet_pos[0], self.__feet_pos[1] - self.__leg_len),
            (self.__feet_pos[0], self.__feet_pos[1] - (self.__leg_len + self.__torso_len)),
            self.__torso_width
        )
        
        # 머리 그리기
        pygame.draw.circle(
            screen,
            self.__head_color,
            (self.__feet_pos[0], self.__feet_pos[1] - (self.__leg_len + self.__torso_len + self.__head_len//2)),
            self.__head_len//2
        )
        
        # 팔 그리기
        pygame.draw.line(
            screen,
            self.__arm_color,
            self.__global_shoulder_pos,
            self.__hand_pos,
            self.__arm_width
        )

    def get_hand_pos(self) -> tuple[int, int]:
        """손의 위치 반환"""
        return self.__hand_pos
    
    def get_arm_angle(self) -> float:
        """팔의 각도 반환"""
        return self.__arm_angle
    
    def set_shoulder_pos(self, shoulder_pos:tuple[int, int]):
        """어깨 위치 설정 (팔의 회전축)"""
        self.__global_shoulder_pos = shoulder_pos


class Bullet:
    def __init__(self, position:tuple[int, int], angle:float, speed:float=20.0):
        """
        총알 클래스 생성자
        
        Args:
            position: 총알의 초기 위치
            angle: 총알의 발사 각도 (라디안)
            speed: 총알의 속도 (기본값: 20.0)
        """
        self.__position = position
        self.__angle = angle
        self.__speed = speed
        self.__radius = 3  # 총알 반지름
        self.__color = "#FF0000"  # 빨간색 총알
        self.__gravity = 0.4  # 중력 가속도
        
        # 각도와 속도를 기반으로 x, y 방향 속도 계산
        self.__velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
        self.__active = True
        
    def update(self):
        """총알의 위치 업데이트"""
        if not self.__active:
            return
            
        # 총알 위치 업데이트
        self.__position = (
            self.__position[0] + self.__velocity[0],
            self.__position[1] + self.__velocity[1]
        )
        
        # 중력 적용
        self.__velocity[1] += self.__gravity
        
    def draw(self, screen:pygame.Surface):
        """총알 그리기"""
        if self.__active:
            pygame.draw.circle(screen, self.__color, 
                              (int(self.__position[0]), int(self.__position[1])), 
                              self.__radius)
    
    def set_angle(self, angle:float):
        """총알의 발사 각도 설정"""
        self.__angle = angle
        self.__velocity = [math.cos(angle) * self.__speed, math.sin(angle) * self.__speed]
    
    def set_speed(self, speed:float):
        """총알의 속도 설정"""
        self.__speed = speed
        # 속도가 변경되면 velocity(속도 벡터)도 갱신
        self.__velocity = [math.cos(self.__angle) * speed, math.sin(self.__angle) * speed]
            
    def get_position(self) -> tuple[int, int]:
        """총알의 현재 위치 반환"""
        return self.__position
    
    def get_radius(self) -> int:
        """총알의 반지름 반환"""
        return self.__radius
    
    def is_active(self) -> bool:
        """총알이 활성화 상태인지 확인"""
        return self.__active
    
    def deactivate(self):
        """총알 비활성화"""
        self.__active = False


class Drone:
    def __init__(self, position:tuple[int, int], size:tuple[int, int]):
        """
        드론 클래스 생성자
        
        Args:
            position: 드론의 위치 (좌상단)
            size: 드론의 크기 (너비, 높이)
        """
        self.__position = position
        self.__size = size
        self.__active = True
        
        # 드론 이미지 로드
        try:
            self.__image = pygame.image.load(os.path.join("rcs", "drone.png")).convert_alpha()
            self.__image = pygame.transform.scale(self.__image, self.__size)
        except pygame.error:
            # 이미지 로드 실패시 대체 그래픽으로 빨간색 사각형 사용
            print("Warning: Failed to load drone image. Using fallback graphics.")
            self.__image = pygame.Surface(self.__size, pygame.SRCALPHA)
            self.__image.fill("#FF0000")  # 빨간색으로 표시
        
        # 충돌 감지를 위한 rect
        self.__rect = pygame.Rect(self.__position, self.__size)
        
    def draw(self, screen:pygame.Surface):
        """드론 그리기"""
        if not self.__active:
            return
            
        # 이미지 그리기
        screen.blit(self.__image, self.__position)
    
    def check_collision(self, bullet_pos:tuple[int, int], bullet_radius:int) -> bool:
        """드론과 총알의 충돌 검사"""
        self.__rect.topleft = self.__position  # rect 위치 업데이트
        return self.__rect.collidepoint(bullet_pos)
    
    def hit(self):
        """드론이 맞았을 때 처리"""
        self.__active = False
        
    def is_active(self) -> bool:
        """드론이 활성화 상태인지 확인"""
        return self.__active
    
    def move(self, new_position:tuple[int, int]):
        """드론 위치 이동"""
        self.__position = new_position
        self.__rect.topleft = new_position  # rect 위치도 함께 업데이트
        
    def get_width(self):
        return self.__size[0]
    
    def get_height(self):
        return self.__size[1]


# 테스트용 메인 함수
def main():
    # Pygame 초기화
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("드론 슈팅 게임")
    clock = pygame.time.Clock()
    
    # 객체 생성
    person = Person((400, 500), 5)
    drone = Drone((600, 100), (50, 30))
    bullets = []
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭 시 총알 발사
                hand_pos = person.get_hand_pos()
                arm_angle = person.get_arm_angle()
                bullets.append(Bullet(hand_pos, arm_angle, 20))
                
        # 화면 지우기
        screen.fill("#87CEEB")  # 하늘색 배경
        
        # 바닥 그리기
        pygame.draw.rect(screen, "#8B4513", pygame.Rect(0, 500, 800, 100))
        
        # 마우스 위치에 따라 팔 각도 조정
        person.move_arm_pos(pygame.mouse.get_pos())
        
        # 객체 업데이트 및 그리기
        person.draw(screen)
        drone.draw(screen)
        
        # 총알 업데이트 및 그리기
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            
            # 화면 밖으로 나가면 총알 제거
            pos = bullet.get_position()
            if pos[0] < 0 or pos[0] > 800 or pos[1] < 0 or pos[1] > 600:
                bullets.remove(bullet)
                continue
                
            # 충돌 감지
            if drone.is_active() and bullet.is_active() and drone.check_collision(pos, bullet.get_radius()):
                drone.hit()
                bullet.deactivate()
                
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
