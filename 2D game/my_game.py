import pygame,sys,random
from pygame.locals import *


BLACK=(0,0,0)
BROWN=(153,76,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

DIRT=0
STONE=1
WATER=2
COAL=3
CLOUD=4
WOOD=5
AXE=6
FIREPLACE=7
SPEAR=8
MATERIAL=9
ANOTHER_CLOUD=10

cloudx=-200
cloudx1=-100
cloudy=0
cloudy1=100

resources=[DIRT,STONE,WATER,COAL,WOOD,AXE]

textures={
    DIRT:pygame.image.load('dirt.png'),
    STONE:pygame.image.load('stone.png'),
    WATER:pygame.image.load('water.png'),
    COAL:pygame.image.load('coal.png'),
    CLOUD:pygame.image.load('cloud.png'),
    ANOTHER_CLOUD:pygame.image.load('cloud.png'),
    WOOD:pygame.image.load('wood.png'),
    AXE:pygame.image.load('axe.png'),
    FIREPLACE:pygame.image.load('fireplace.png'),
    MATERIAL:pygame.image.load('material.png')
    }

controls={
    DIRT:49,
    STONE:50,
    WATER:51,
    COAL:52,
    WOOD:53,
    AXE:54
    }

inventory={
    DIRT:0,
    STONE:0,
    WATER:0,
    COAL:0,
    WOOD:0,
    AXE:0,
    }

craft={
    AXE:{WOOD:2,STONE:2},
    FIREPLACE:{WOOD:5,COAL:2},
    MATERIAL:{DIRT:1,STONE:1}
    }

playerPos=[0,0]

TILESIZE=50
MAPWIDTH=12
MAPHEIGHT=12

tilemap=[[DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]

for rw in range(MAPHEIGHT):
    for cl in range(MAPHEIGHT):
        randomNumber=random.randint(0,20)
        if randomNumber==0:
            tile=COAL
        elif randomNumber==1 or randomNumber==2:
            tile=WATER
        elif randomNumber<=3 and randomNumber<=7:
            tile=STONE
        elif randomNumber>=10 and randomNumber<=15:
            tile=WOOD
        else:
            tile=DIRT
        tilemap[rw][cl]=tile

pygame.init()

PLAYER=pygame.image.load('char.png')
screen=pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE+100))

INVFONT=pygame.font.Font('FreeSansBold.ttf',18)

pygame.display.set_caption('Survival')

while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if(event.key==K_RIGHT) and playerPos[0]<MAPWIDTH-1:
                playerPos[0]+=1
            elif(event.key==K_LEFT) and playerPos[0]>0:
                playerPos[0]-=1
            elif(event.key==K_DOWN) and playerPos[0]<MAPHEIGHT-1:
                playerPos[1]+=1
            elif(event.key==K_UP) and playerPos[1]>0:
                playerPos[1]-=1

            if event.key==K_SPACE:
                currentTile=tilemap[playerPos[1]][playerPos[0]]
                inventory[currentTile]+=1
                tilemap[playerPos[1]][playerPos[0]]=DIRT

            for key in controls:
                if(event.key==controls[key]):
                    if pygame.mouse.get_pressed()[0]:
                        if key in craft:
                            canBeMade=True
                            for i in craft[key]:
                                if craft[key][i]>inventory[i]:
                                    canBeMade=False
                                    break
                            if canBeMade==True:
                                for i in craft[key]:
                                    inventory[i]-=craft[key][i]
                                inventory[key]+=1
                        else:
                            currentTile=tilemap[playerPos[1]][playerPos[0]]
                            if inventory[key]>0:
                                inventory[key]-=1
                                inventory[currentTile]+=1
                                tilemap[playerPos[1]][playerPos[0]]=key

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            screen.blit(textures[tilemap[row][column]],(column*TILESIZE,row*TILESIZE))
    screen.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))
        

    screen.blit(textures[CLOUD],(cloudx,cloudy))
    screen.blit(textures[ANOTHER_CLOUD],(cloudx1,cloudy1))
    cloudx1+=1
    cloudx+=1
    if cloudx>MAPWIDTH*TILESIZE:
        cloudy=random.randint(0,MAPHEIGHT*TILESIZE)
        cloudy1=random.randint(0,MAPHEIGHT*TILESIZE)
        cloudx=-200
        cloudx1=-100

    placePosition=10
    for item in resources:
        screen.blit(textures[item],(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition+=50
        textObj=INVFONT.render(str(inventory[item]),True,WHITE,BLACK)
        screen.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition+=50

    pygame.display.update()
            
