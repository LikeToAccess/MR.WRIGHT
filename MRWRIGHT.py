#REMINDER TO USE LOW RES IMAGES ALWAYS
import os, sys, random
from time import sleep, time


#============================
# PYGAME INSTALL \/ \/ \/
#============================
try:
    import pygame
    has_pygame = True
except ImportError as e:
    import pip
    has_pygame = False
    try:
        print(str(e)+", failed import\n\nYou will have to make a ONE TIME INSTALL on this computer\n")
        print("python support: {}".format(sys.version_info))
        import pip._internal
        if hasattr(pip, "_internal"):
            supported = pip._internal.pep425tags.get_supported()
            for index, text in enumerate(supported):
                ver, plat, ostype = text # error here
                print("pip support: {}, {}, {}".format(ver,plat,ostype))
		#sleep(2)
        else:
            import wheel.pep425tags
            print(wheel.pep425tags.get_supported())
    except ImportError as e:
        print(str(e)+", failed pip info")

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def install_init(module):
    if not has_pygame:
        try:
            import pip.main
        except:
            pass
        try:
            install(module)
        except Exception as e:
            print(str(e)+", failed installation")

if not has_pygame:
    try:
        question = raw_input("\nInstall with file? (y/n)\n> ")
    except NameError:
        question = input("\nInstall with file? (y/n)\n> ")
    if question.lower().replace(" ","") == "y":
        install_init("pygame-1.9.4-cp37-cp37m-macosx_10_11_intel.whl")
    else:
        install_init("pygame")
    try:
        import pygame
        has_pygame = True
    except ImportError as e:
        print(str(e)+", failed installation")#. Attempting last resort")

#============================
# END PYGAME INSTALL /\ /\ /\
#============================


pygame.init()
print("Installation Success!")
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
#print(width, height)  # out: 1280 1024
pygame.display.set_caption('Get Over Here Mr.Wright!!!')
clock = pygame.time.Clock()
gameIcon = pygame.image.load('icon1.png')
pygame.display.set_icon(gameIcon)

#============================
black = (0,0,0)
white = (255,255,255)

bright_grey = (215,215,215)
grey = (200,200,200)
dark_grey = (100,100,100)

bright_yellow = (255,255,0)
yellow = (255,215,0)
dark_yellow = (250,180,0)

bright_red = (255,0,0)
red = (200,0,0)

bright_blue = (100,150,255)
blue = (55,100,255)
dark_blue = (25,50,255)

bright_green = (0,255,0)
green  = (0,200,0)

light_brown = (160,113,69)
dark_brown = (100,53,9)


#============================
# ESSENTIAL FUNCTIONS \/ \/ \/
#============================

def write_file(text,filename="player.txt"):
    f = open(filename, "w")
    f.write(text)
    f.close()

def read_file(filename="player.txt",line=False):
    f = open(filename, "r")
    data = f.read()
    f.close()
    if line:
        data = data.split("\n")[line-1]
    return data

def quit_game():
    pygame.quit()
    sys.exit()

def blitImg(img,x,y,width=None,height=None):
    if width and height:
        picture = pygame.image.load(img)
        picture = pygame.transform.scale(picture,(width,height))

        pic_rect = picture.get_rect()
        pic_rect = pic_rect.move((x,y))
        screen.blit(picture, pic_rect)
    else:
        screen.blit(pygame.image.load(str(img)),(x,y))

##def blitImg(img,x,y):
##    screen.blit(pygame.image.load(str(img)),(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text(text,x,y,size=100):
    largeText = pygame.font.Font("Raleway-Medium.ttf", int(size))
    TextSurf, TextRect = text_objects((text), largeText)
    TextRect.center = ((x),(y))
    screen.blit(TextSurf, TextRect)

def text_uncentered(text,x,y,size=100):
    largeText = pygame.font.Font("Raleway-Medium.ttf", int(size))
    TextSurf, TextRect = text_objects((text), largeText)
    screen.blit(TextSurf, (x,y))

def button(text,x,y,w,h,ic,ac,action=None,params=None,reactive=False, sleeptime=0.0):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1:
            if reactive:
                pygame.draw.rect(screen, bright_green, (x,y,w,h))
            if action != None:
                sleep(sleeptime)
                if params:
                    action(params)
                else:
                    action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.Font("Raleway-Medium.ttf",int(width/28))  # 45
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def box(x,y,w,h,c):
    pygame.draw.rect(screen,c,[x,y,w,h])

def controls(is_online=False, boxes_dodged=0, speed=4.8):
    if is_online:
        global deltaX
        global deltaY
    else:
        global deltaX
        global deltaY
        global deltaWrightX
        global deltaWrightY

    car_speed = speed + boxes_dodged*0.3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                deltaY -= car_speed
            if event.key == pygame.K_s:
                deltaY += car_speed
            if event.key == pygame.K_a:
                deltaX -= car_speed
            if event.key == pygame.K_d:
                deltaX += car_speed

            if not is_online:
                if event.key == pygame.K_UP:
                    deltaWrightY -= car_speed
                if event.key == pygame.K_LEFT:
                    deltaWrightX -= car_speed
                if event.key == pygame.K_DOWN:
                    deltaWrightY += car_speed
                if event.key == pygame.K_RIGHT:
                    deltaWrightX += car_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                deltaY = 0
            if event.key == pygame.K_a:
                deltaX = 0
            if event.key == pygame.K_s:
                deltaY = 0
            if event.key == pygame.K_d:
                deltaX = 0

            if not is_online:
                if event.key == pygame.K_UP:
                    deltaWrightY = 0
                if event.key == pygame.K_LEFT:
                    deltaWrightX = 0
                if event.key == pygame.K_DOWN:
                    deltaWrightY = 0
                if event.key == pygame.K_RIGHT:
                    deltaWrightX = 0

def line(color,is_closed,points_list,stroke_width):
    pygame.draw.lines(screen,color,is_closed,points_list,stroke_width)

def car(car,face,x,y,offset=[75,40]):
    x_off, y_off = offset
    x_off, y_off = int(x_off), int(y_off)
    blitImg(car,x,y)
    blitImg(face,x+x_off,y+y_off)

def stripe(x,y,stripe_width,stripe_leangth,color):
    line(color,False,[(x,y),(x,y+stripe_leangth)],stripe_width)

#============================
# SCREENS \/ \/ \/
#============================

def win_screen(player):
    print(player)

    if player == 1:
        text("The Trouble Makers WIN!", int(width/4),200, 43)  # left wins
        text("I'm Hit!", int(width/4*3),200, 53)  # right is hit
    if player == 2:
        text("Mr.Wright is VICTORIOUS!", int(width/4*3),200, 43)  # right wins
        text("I'm Hit!", int(width/4),200, 53)  # left is hit

    while True:
        #screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button("Back", width/2+80,605,300,100, bright_red,red, player_select, sleeptime=0.3)
        button("Again", width/2-380,605,300,100, bright_green, green, local_play,True)

        pygame.display.update()
        clock.tick(120)
    quit_game()

def player_select():
    nameSize = 26
    quoteSize = 18
    while True:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        text("Select Your Trouble Maker!", 650,100,90)

        # Player1
        button("", 95,195,260,310, white,bright_grey, write_file,"player1",True)
        blitImg("player1.png", 100,200)
        text('Mr. Hammes:', 220, 540, nameSize)
        text('"It\'s pronounced \'hams.\'"', 220,570, quoteSize)

        # Player2
        button("", 375,195,260,310, white,bright_grey, write_file,"player2",True)
        blitImg("player2.png", 380,200)
        text('Lucas Farrar-Collins:', 500, 540, nameSize)
        text('"Give me your food!"', 500,570, quoteSize)

        # Player3
        button("", 655,195,260,310, white,bright_grey, write_file,"player3",True)
        blitImg("player3.png", 660,200)
        text('Raven Barickman:', 780, 540, nameSize)
        text('"BBBBVVVVVBVBVBVBBB..."', 780,570, quoteSize)

        # Player4
        button("", 935,195,260,310, white,bright_grey, write_file,"player4",True)
        blitImg("player4.png", 940,200)
        text('Simon Hoska:', 1060, 540, nameSize)
        text('"It\'s Eric time!"', 1060,570, quoteSize)

        button("Start", 275,605,300,100, bright_green, green, local_play,True)
        button("Back",  725,605,300,100, bright_red,   red,   main_menu)

        pygame.display.update()
        clock.tick(120)

def local_play(select_done=False):
    if not select_done:
        player_select()

    global deltaX
    global deltaY
    global deltaWrightX
    global deltaWrightY

    crashed_p1, crashed_p2 = False, False
    player1 = read_file('player.txt').replace("player","car")+".png"
    face1 = read_file('player.txt').replace("player","face")+".png"
    player2 = "car5.png"
    face2 = "face5.png"

    deltaX,deltaY = 0,0
    deltaWrightX,deltaWrightY = 0,0
    wrightX,wrightY = 800,200
    x,y = 100,200
    car_height = 190  # 233
    car_width = 98    # 108
    player_off = read_file(player1.replace(".png",".txt"), 2).split("|")
    wright_off = read_file(player2.replace(".png",".txt"), 2).split("|")
    player_speed = float(read_file(player1.replace(".png",".txt"), 5))
    # get head offset and upgrade info from "car1.txt"

    box_width = 100
    box_height = 100
    box_x = random.randrange(0,width-int(box_width))
    box_y = -500
    box_speed = 3.5
    boxes_dodged = 0
    p1_dodged = 0
    p2_dodged = 0
    half_width = width/2
    stripe_y = 0

    while True:
        screen.fill(dark_grey)

        #============================
        # ROAD STRIPES \/ \/ \/
        #============================
        stripe(20,0, 20,height, yellow)  # left stripe on left side
        stripe(half_width-25,0, 20,height, white)  # right stripe on left side
        for i in range(-4,4):
            stripe(width/4,stripe_y+300*i, 20,86, white)  # mid stripe on left side

        stripe(half_width+25,0, 20,height, white)  # left stripe on right side
        stripe(width-20,0, 20,height, yellow) # right stripe on right side
        for i in range(-4,4):
            stripe(width/4*3,stripe_y+300*i, 20,86, white) # mid stripe on right side

        stripe_y += box_speed
        #============================
        # ROAD STRIPES /\ /\ /\
        #============================

        box(box_x,box_y,box_width,box_height,dark_brown)
        box_y += box_speed
        #blitImg("road.png",0,box_y)

        controls(False, boxes_dodged, player_speed)

        line(black,False,[(half_width,0),(half_width,height)],10)
        car(player1,face1,x,y,player_off)
        car(player2,face2,wrightX,wrightY,wright_off)

        text_uncentered("Dodged: {}".format(p1_dodged),17,11, 18)
        text_uncentered("Dodged: {}".format(p2_dodged),half_width+22,11, 18)

        y +=  deltaY
        x +=  deltaX
        wrightY += deltaWrightY
        wrightX += deltaWrightX

        #============================
        # COLLISION \/ \/ \/
        #============================
        if y < -50 or y+car_height > height+35:  # if car is above or below screen
            crashed_p1 = True
        elif x < -5 or x > half_width-car_width:  # if car is too far left or right
            crashed_p1 = True
        if y < box_y+box_height and y+car_height > box_y:  # if car a box
            if x > box_x and x < box_x+box_width or x+car_width > box_x and x+car_width < box_x+box_width:
                crashed_p1 = True

        if wrightY < -50 or wrightY > height-car_height+35:  # if car is above or below screen
            crashed_p2 = True
        elif wrightX < half_width or wrightX+car_width > width+5:  # if car is too far left or right
            crashed_p2 = True
        if wrightY < box_y+box_height and wrightY+car_height > box_y:  # if car a box
            if wrightX > box_x and wrightX < box_x+box_width or wrightX+car_width > box_x and wrightX+car_width < box_x+box_width:
                crashed_p2 = True
        #============================
        # COLLISIONS /\ /\ /\
        #============================

        if crashed_p1 == True:
            win_screen(2)
        elif crashed_p2 == True:
            win_screen(1)

        if box_y > height:
            if box_x > half_width:
                p2_dodged += 1
            else:
                p1_dodged += 1

            if random.choice([True,False]):  # decides if box goes on left or right
                box_x = random.randrange(0,int(half_width)-int(box_width)-10)  # box goes left
            else:
                box_x = random.randrange(int(half_width)+10,width-int(box_width))  # box goes right
            box_y = 0-box_height

            box_speed = box_speed*1.009+0.5
            boxes_dodged += 1
            box_width += (random.randrange(1,boxes_dodged+2)+boxes_dodged) / 4
            box_height += (random.randrange(1,boxes_dodged+2)+boxes_dodged) / 4

        if stripe_y+86 > 386:
            stripe_y = 0


        pygame.display.update()
        clock.tick(120)
        #average: 210ms

def online_play():
    quit_game()

def campaign():
    quit_game()

def credit():
    quit_game()

#============================
# MENUS \/ \/ \/
#============================

def shop_menu():
    sleep(0.2)
    while True:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        #blitImg()

def game_menu():
    sleep(0.2)
    while True:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        blitImg("background1.png", 0,0, width,height)
        button("Local",  275,540,300,100, yellow, dark_yellow, local_play)
        button("Online", 725,540,300,100, yellow, dark_yellow, online_play)

        pygame.display.update()
        clock.tick(120)

def main_menu():
    sleep(0.2)
    while True:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button("Play",    275,450,300,100, yellow,     dark_yellow, game_menu)  # width/4.65,height/2.28,width/4.27,height/10.24
        button("Campaign", 725,450,300,100, blue,       dark_blue,   campaign)
        button("Credits", 275,575,300,100, grey,       dark_grey,   credit)
        button("Quit",    725,575,300,100, bright_red, red,         quit_game)
        text("MR.WRIGHT GET OVER HERE", width/2, 190, width/15)


        pygame.display.update()
        clock.tick(120)

#============================
# MAIN EXECUTION \/ \/ \/
#============================

if __name__ == "__main__":
    try: main_menu()
    except Exception as e: print(str(e))

pygame.quit()
quit()
