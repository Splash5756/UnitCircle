import pygame
import sys
import math
import copy
from decimal import Decimal

global window
window = None

global Cord
Cord = []

global font
font = None

#sayfayı oluştur
def init():
    global window
    global font

    pygame.init()
    window = pygame.display.set_mode((500,500),pygame.SCALED | pygame.SRCALPHA | pygame.RESIZABLE,depth=32,vsync=0)
    window.fill((255,255,255))
    pygame.display.flip()
    font = pygame.font.SysFont(name="Calibri", size=12)

# sayfanın merkezini bul
def CenterOfWindow():
    return [250,250]

# X ve Y yi çiz
def Xline():
    #açık gri ile (150,150,150)
    color = (150,150,150)
    cords = (0,CenterOfWindow()[1],500,1)
    pygame.draw.rect(window,color,cords)


def Yline():
    #açık gri ile (150,150,150)
    color = (150,150,150)
    cords = (CenterOfWindow()[0],0,1,500)
    pygame.draw.rect(window,color,cords)

#taylor yöntemi
def sin(X):
    # terim sayısı için X/10 <= 7 7 terim kullan x/10 > 7 x/10 terim kullan (sadece int)
    term = 9

    func = math.radians(X)
    for i in range(1,term):
        func += ((math.pow((math.radians(X)),((i*3)-(i-1)))*(math.pow(-1,i))))/float(math.factorial(((i*3)-(i-1))))

    return func

def cos(X):
    term = 9
    func = 0

    if X <= 90 and X >= 0:
        func = 1
        for i in range(1,term):
            func += Decimal(math.pow(math.radians(X),math.exp2(i))*math.pow(-1,i)) / Decimal(math.factorial(int(math.exp2(i))))
    elif X >= 90 and X <= 180:
        nX = X - 180
        func = 1
        for i in range(1,term):
            func += Decimal(math.pow(math.radians(nX),math.exp2(i))*math.pow(-1,i)) / Decimal(math.factorial(int(math.exp2(i))))
        func = func * -1
    elif X >= 180 and X <= 270:
        func = 1
        nX = X - 180
        for i in range(1,term):
            func += Decimal(math.pow(math.radians(nX),math.exp2(i))*math.pow(-1,i)) / Decimal(math.factorial(int(math.exp2(i))))
        func = func * -1
    elif X >= 270 and X <= 360:
        func = 1
        nX = 360 - X
        for i in range(1,term):
            func += Decimal(math.pow(math.radians(nX),math.exp2(i))*math.pow(-1,i)) / Decimal(math.factorial(int(math.exp2(i))))
    
    return func

# 1. bölgeyi çiz
def Cycle():
    # 0 , 90 arası
    color = (0,0,0)
    
    # X ve Y kordinatlarında bir üçgen simule edip sinA cosA yı hesapla
    
    #400 / 2 = 200 
    #cosX SinX olan kordinata (CosX + (125 * 2) ,450 - SinX,1,1) bir kare çiz
    for x in range(0,9001):
        cord = (float((250 - (cos(((x/100))))*200)),float((250 - (sin(((x/100))))*200)),1,1)
        pygame.draw.rect(window,color,cord)
        Cord.append(copy.copy(cord))
    for x in range(9001,18001):
        cord = (float((250 - (cos(((x/100))))*200)),float((250 - (sin(((x/100))))*200)),1,1)
        pygame.draw.rect(window,color,cord)
        Cord.append(copy.copy(cord))
    for x in range(18001,27001):
        cord = (float((250 - (cos(((x/100))))*200)),float((250 - (sin(((x/100))))*200)),1,1)
        pygame.draw.rect(window,color,cord)
        Cord.append(copy.copy(cord))
    for x in range(27001,36001):
        cord = (float((250 - (cos(((x/100))))*200)),float((250 - (sin(((x/100))))*200)),1,1)
        pygame.draw.rect(window,color,cord)
        Cord.append(copy.copy(cord))
    
def resetCycle():
    for c in Cord:
        pygame.draw.rect(window,(0,0,0),c)

def main():
    init()
    Xline()
    Yline()
    Cycle()
    loop()

def loop():
    global font

    while True:
        # Olayları kontrol et
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and keys[pygame.K_F4]:
            pygame.quit()
            sys.exit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        

        window.fill((255,255,255))
        Xline()
        Yline()
        resetCycle()

        m = pygame.mouse.get_pos()
        if not m[0]-250 == 0:
            degree = math.degrees(math.atan((250-m[1])/(m[0]-250)))
            if (250-m[1]) >= 0 and (m[0]-250) <= 0:
                degree = 180 + degree
            elif (250-m[1]) <= 0 and (m[0]-250) <= 0:
                degree = 180 + degree
            elif (250-m[1]) <= 0 and (m[0]-250) >= 0:
                degree = 360 + degree
            
            pygame.draw.line(window,(0,0,250),(250,250),(250 + (float(cos(degree)*200)),(250 + (sin((degree)*-1)*200))))
            # SinX doğru parçası
            pygame.draw.line(window,(0,250,0),((250+ (float(cos(degree)*200))),250),(250 + (float(cos(degree)*200)),(250 + (sin((degree)*-1)*200))))
            # CosX doğru parçası
            pygame.draw.line(window,(250,0,0),(250,(250 + (sin((degree)*-1)*200))),(250 + (float(cos(degree)*200)),(250 + (sin((degree)*-1)*200))))
            # noktanın kordinatlarını yaz
            # tanjant cotanjant ekle
        else:
            if 250-m[1] > 0:
                pygame.draw.line(window,(0,0,250),(250,250),(250,50))
                degree = 90
            elif 250-m[1] <0:
                degree = 270
                pygame.draw.line(window,(0,0,250),(250,250),(250,450))

        #textleri ayarla
        Fcos: pygame.surface.Surface = font.render(f"cos{float(degree):.3f} = {float(cos(degree)):.3f}", True, (0, 0, 0))
        Fsin: pygame.surface.Surface = font.render(f"sin{float(degree):.3f} = {float(sin(degree)):.3f}", True, (0, 0, 0))
        
        #cos doğrusunun uzunluğunu al / 2 yap (negatif veya pozitif olarak) sonra 250. pixele ekle (X konumu için)
            #cos doğrusunun uzunluğu 
        #sin doğrununun uzunluğunu al (negatif veya pozitif olarak) sonra 250. pixele ekle (Y konumu için)
        cosXY = ((250+ (float(cos(degree)*200)/2)),(250 + (sin((degree)*-1)*200)))
        #sin doğrusunun uzunluğunu al / 2 yap (negatif veya pozitif olarak) sonra 250. pixele ekle (Y konumu için)
        #cos doğrununun uzunluğunu al (negatif veya pozitif olarak) sonra 250. pixele ekle (X konumu için)
        sinXY = ((250+ (float(cos(degree)*200))),(250 + (sin((degree)*-1)*200)/2))

        window.blit(Fcos,cosXY)
        window.blit(Fsin,sinXY)

        # Ekranı güncelle
        pygame.display.flip()

if __name__ == "__main__":
    main()