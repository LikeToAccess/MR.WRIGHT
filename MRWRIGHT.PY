#pylint:disable=C0103
#pylint:disable=C0111
#pylint:disable=C0325
#pylint:disable=W0312
import os, sys
from time import sleep


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
				ver, plat, ostype = text
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
try:
	question = raw_input("\nInstall with file? (y/n)\n> ")
except NameError:
	question = input("\nInstall with file? (y/n)\n> ")
if question.lower().replace(" ","") == "y":
	install_init("pygame-1.9.4-cp36-cp36m-macosx_10_11_intel.whl")
else:
	install_init("pygame")
	
try:
	import pygame
	has_pygame = True
except ImportError as e:
	print(str(e)+", failed installation")#. Attempting last resort")
'''
try:
	os.system("pip install pygame")
except Exception as e:
	print e
'''
#============================
# END PYGAME INSTALL /\ /\ /\
#============================
 
				
pygame.init()
print("Instillation Success!")
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
dark_grey = (180,180,180)

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


#============================
# ESSENTIAL FUNCTIONS \/ \/ \/
#============================

def write_file(text,filename="player.txt"):
    f = open(filename, "w")
    f.write(text)
    f.close()

def quit_game():
    pygame.quit()
    sys.exit()

def blitImg(img, x, y):
    screen.blit(pygame.image.load(str(img)),(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text(text,x,y,size=100):
    largeText = pygame.font.Font("Raleway-Medium.ttf", int(size))
    TextSurf, TextRect = text_objects((text), largeText)
    TextRect.center = ((x),(y))
    screen.blit(TextSurf, TextRect)

def button(text,x,y,w,h,ic,ac,action=None,params=None,reactive=False):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1:
            if reactive:
                pygame.draw.rect(screen, bright_green, (x,y,w,h))
            if action != None:
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

#============================
# SCREENS \/ \/ \/
#============================

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
        text('"It\'s pronounced hams."', 220,570, quoteSize)

        # Player2
        button("", 375,195,260,310, white,bright_grey, write_file,"player1",True)
        blitImg("player2.png", 380,200)
        text('Lucas Farrar-Collins:', 500, 540, nameSize)
        text('"Gimme you lunch money!"', 500,570, quoteSize)

        # Player3
        button("", 655,195,260,310, white,bright_grey, write_file,"player1",True)
        blitImg("player3.png", 660,200)
        text('Raven Barickman:', 780, 540, nameSize)
        text('"BBBBVVVVVBVBVBVBBB..."', 780,570, quoteSize)

        # Player4
        button("", 935,195,260,310, white,bright_grey, write_file,"player1",True)
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
    quit_game()
    # insert local game here!!!

def online_play():
    quit_game()

def campain():
    quit_game()

def credit():
    quit_game()

#============================
# MENUS \/ \/ \/
#============================

def game_menu():
    sleep(0.2)
    while True:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        blitImg("background1.png",0,0)
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
        button("Campain", 725,450,300,100, blue,       dark_blue,   campain)
        button("Credits", 275,575,300,100, grey,       dark_grey,   credit)
        button("Quit",    725,575,300,100, bright_red, red,         quit_game)
        text("MR.WRIGHT GET OVER HERE", width/2, 190, width/15)


        pygame.display.update()
        clock.tick(120)

#============================
# MAIN EXECUTION \/ \/ \/
#============================

if __name__ == "__main__":
    main_menu()
