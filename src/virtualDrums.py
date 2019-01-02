import pygame
import cv2
import numpy as np
import time
from soundGenerator import sound_checker


camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Virtual Drums")
screen = pygame.display.set_mode([640,480])
clock = pygame.time.Clock()
color = [255,0,0]

black = (0,0,0)

low_color = np.array([75, 133, 77]) 
up_color = np.array([149, 255, 255]) 

green = (0,200,0)
red = (200,0,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

def objectTracker(frame, kernelOpen, kernelClose):
    
    ################# OBJECT TRACKER USING HSV COLORSPACE #################
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ht, wd = frame.shape[:2]
    
    mask = cv2.inRange(hsv, low_color, up_color)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelClose)
    _, contours, _ = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        radius = int(radius)
        M = cv2.moments(c)
        try:
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/ M["m00"]))
            x, y = center
        except:
            center = int(ht/2), int(wd/2)
        if radius > 25:
#            cv2.circle(frame, (int(x), int(y)), radius, (88, 50, 255), 5)
            sound_checker(x,y)
            cv2.circle(frame, center, 5, color, -3)
    
    
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    
def button(msg, x,y,w,h,inactiveColor, activeColor, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, activeColor, (x, y, w,h))
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, inactiveColor, (x, y, w,h))
    
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurface, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    screen.blit(textSurface, textRect)

def text_objects(text, font):
    textSurf = font.render(text, True, black)
    return textSurf, textSurf.get_rect()

def msg_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 60)
    textSurface, textRect = text_objects(text, largeText)
    textRect.center = ((640/2),(480/2))
    screen.blit(textSurface, textRect)
    
    pygame.display.update()
    time.sleep(2)
    
    game_loop()

    
def game_intro():
    
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        screen.fill([255,255,255])
        largeText = pygame.font.Font('freesansbold.ttf', 60)
        textSurface, textRect = text_objects("Virtual Drums", largeText)
        textRect.center = ((640/2),(480/2))
        screen.blit(textSurface, textRect)
        
        button("GO!!", 150,350,150,60,green, bright_green, "play")
        
        button("QUIT!!", 350,350,150,60,red, bright_red, "quit")
        
        pygame.display.update()
        clock.tick(15)


#
def making_drums(frame, x, y, w, h, color, thickness):
     
    #################  MAKING DRUMS ON THE SCREEN ###################### 
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    
    

def game_loop():

    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))

    gameExit = False
    try:
        while not gameExit:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            ret, frame = camera.read()
    		 
            ########## DISPLAYING ON THE SCREEN ##############
            screen.fill([0,0,0])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            making_drums(frame, 70, 80, 60, 60, (255,255,0), 3)
            making_drums(frame, 170, 60, 60, 60, (255,0,0), 3)
            making_drums(frame, 270, 40, 60, 60, (0,255,0), 3)
            making_drums(frame, 370, 60, 60, 60, (0,255,255), 3)
            making_drums(frame, 470, 80, 60, 60, (255,0,255), 3)
            
            objectTracker(frame, kernelOpen, kernelClose)
            
            pygame.display.update() 
            clock.tick(60)
                
    except:
        camera.release()
        pygame.quit()
        cv2.destroyAllWindows()


game_intro()
game_loop()
