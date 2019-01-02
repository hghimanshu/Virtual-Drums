import pygame

pygame.init()
drum1 = pygame.mixer.Sound("Sounds\\sample1.wav")
drum2 = pygame.mixer.Sound("Sounds\\sample2.wav")
drum3 = pygame.mixer.Sound("Sounds\\sample4.wav")
drum4 = pygame.mixer.Sound("Sounds\\sample5.wav")
drum5 = pygame.mixer.Sound("Sounds\\sample6.wav")


def sound_checker(x,y):
    if x in range(70, 130):
        if y in range(80, 140):
            pygame.mixer.Sound.play(drum1)
    if x in range(170, 230):
        if y in range(60, 120):
            pygame.mixer.Sound.play(drum2)
    if x in range(270, 330):
        if y in range(40, 100):
            pygame.mixer.Sound.play(drum3)
    if x in range(370, 430):
        if y in range(60, 120):
            pygame.mixer.Sound.play(drum4)
    if x in range(470, 530):
        if y in range(80, 1400):
            pygame.mixer.Sound.play(drum5)
