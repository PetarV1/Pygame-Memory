import random, time, pygame
from pygame.event import wait
pygame.init()
SCREEN = (800,450)
DISPLAY = pygame.display.set_mode(SCREEN)

#Boje
ZELENA = (107,142,35)
BIJELA = (255, 255, 255)
CRNA = (0, 0, 0)
CRVENA = (255, 0, 0)

#Fontovi i tekst
KRAJ = pygame.font.SysFont("Arial", 80)
ARIAL_50 = pygame.font.SysFont("Arial", 50)
ARIAL_35 = pygame.font.SysFont("Arial", 35)
ARIAL_20 = pygame.font.SysFont("Arial", 20)

#Konstante vezane uz igru
DULJINA_KARTICA = 100
MARGINA_KARTICA = 10
KARTICA_POZICIJA_X = 40
KARTICA_POZICIJA_Y = 20
RED = 4
STUPAC = 5

Lista_kartica = [i for i in range(10) for j in range(2)]
random.shuffle(Lista_kartica)
VRIJEDNOSTI_KARTICA = [Lista_kartica[i*len(Lista_kartica) // RED:(i+1)*len(Lista_kartica) // RED] for i in range(RED)]
MREZA_KARTICA = [[] for i in range(RED)]
for i in range(RED):
    if i == 0:
        for j in range(STUPAC):
            if j == 0:
                MREZA_KARTICA[i].append(pygame.Rect(MARGINA_KARTICA, MARGINA_KARTICA, DULJINA_KARTICA, DULJINA_KARTICA))
            else:
                MREZA_KARTICA[i].append(pygame.Rect(MREZA_KARTICA[i][j-1].x + DULJINA_KARTICA + MARGINA_KARTICA, MARGINA_KARTICA, DULJINA_KARTICA, DULJINA_KARTICA))
    else:
        for j in range(STUPAC):
            if j == 0:
                MREZA_KARTICA[i].append(pygame.Rect(MARGINA_KARTICA, MREZA_KARTICA[i-1][0].y + DULJINA_KARTICA + MARGINA_KARTICA, DULJINA_KARTICA, DULJINA_KARTICA))
            else:
                MREZA_KARTICA[i].append(pygame.Rect(MREZA_KARTICA[i][j-1].x + DULJINA_KARTICA + MARGINA_KARTICA, MREZA_KARTICA[i-1][0].y + DULJINA_KARTICA + MARGINA_KARTICA, DULJINA_KARTICA, DULJINA_KARTICA))
global otvorene
otvorene = []
global jednake
jednake = []
global razlicite
razlicite = []
global pokreti
pokreti = 0

#Glavna petlja igre
while True:
    for event in pygame.event.get():
        #Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()

    pressed = list(pygame.mouse.get_pressed())
    for i in range(len(pressed)):
        if pressed[i]:
            for i in range(RED):
                for j in range(STUPAC):
                    mouse_pos = list(pygame.mouse.get_pos())
                    if mouse_pos[0] >= MREZA_KARTICA[i][j].x and mouse_pos[1] >= MREZA_KARTICA[i][j].y and mouse_pos[0] <= MREZA_KARTICA[i][j].x + DULJINA_KARTICA and mouse_pos[1] <= MREZA_KARTICA[i][j].y + DULJINA_KARTICA:
                        global instanca
                        instanca = False
                        for k in range(len(otvorene)):
                            if otvorene[k] == [i, j]:
                                instanca = True

                        for k in range(len(jednake)):
                            if jednake[k] == [i, j]:
                                instanca = True

                        if instanca == False:
                            otvorene.append([i, j])
                            
    if len(otvorene) == 2:
        pokreti += 1
        if VRIJEDNOSTI_KARTICA[otvorene[0][0]][otvorene[0][1]] == VRIJEDNOSTI_KARTICA[otvorene[1][0]][otvorene[1][1]]:
            jednake.extend(otvorene)
            otvorene.clear()
            
        else:
            razlicite.extend(otvorene)
            otvorene.clear()

    #Ocisti ekran
    DISPLAY.fill(CRNA)

    #Crtanje kartica na ekranu u odredjenoj boji
    for i in range(RED):
        for j in range(STUPAC):
            pygame.draw.rect(DISPLAY, (255, 255, 255), MREZA_KARTICA[i][j])
            
    #Otvaranje kartica i provjera
    if otvorene:
        for i in otvorene:
            text = str(VRIJEDNOSTI_KARTICA[i[0]][i[1]])
            render = ARIAL_50.render(text, True, CRNA)
            DISPLAY.blit(render, (MREZA_KARTICA[i[0]][i[1]].x + KARTICA_POZICIJA_X, MREZA_KARTICA[i[0]][i[1]].y + KARTICA_POZICIJA_Y))

    if jednake:
        for i in jednake:
            text = str(VRIJEDNOSTI_KARTICA[i[0]][i[1]])
            render = ARIAL_50.render(text, True, ZELENA)
            DISPLAY.blit(render, (MREZA_KARTICA[i[0]][i[1]].x + KARTICA_POZICIJA_X, MREZA_KARTICA[i[0]][i[1]].y + KARTICA_POZICIJA_Y))

    if razlicite:
        for i in razlicite:
            text = str(VRIJEDNOSTI_KARTICA[i[0]][i[1]])
            render = ARIAL_50.render(text, True, CRVENA)
            DISPLAY.blit(render, (MREZA_KARTICA[i[0]][i[1]].x + KARTICA_POZICIJA_X, MREZA_KARTICA[i[0]][i[1]].y + KARTICA_POZICIJA_Y))

    #Ostalo crtanje na ekranu
    Naslov = ARIAL_35.render("Memory", True, BIJELA)
    DISPLAY.blit(Naslov, (570, 10))
    Pokreti_u_igri = ARIAL_20.render("Pokreti: " + str(pokreti), True, ZELENA)
    DISPLAY.blit(Pokreti_u_igri, (580, 75))

    #Provjera je li igra zavrsila, tj. je li pobjeda
    if len(jednake) == 20:
        DISPLAY.fill(CRNA)
        Pobjeda = KRAJ.render("Pobijedili ste! ", True, ZELENA)
        DISPLAY.blit(Pobjeda, (200, 100))
        Pobjeda_pokreti = ARIAL_20.render("Broj pokreta: " + str(pokreti), True, ZELENA)
        DISPLAY.blit(Pobjeda_pokreti, (250, 240))
        pygame.display.flip()
        time.sleep(3)
        break
    
    pygame.display.flip()
    if razlicite:
        time.sleep(1)
        razlicite.clear()