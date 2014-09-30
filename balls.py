import pygame ,sys
from pygame.locals import*

#defining colors
RED = pygame.Color(255, 0, 0, 10)
GREEN = pygame.Color(0, 255, 0, 10)
BLUE = pygame.Color(0, 0, 255, 10)
WHITE = []

#defining an array of greyscales
for i in range (256):
	WHITE.append(pygame.Color(i, i, i, i))

#defining window size
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#checking window dimensions
assert WINDOWWIDTH < 641 and WINDOWHEIGHT < 481, 'YOU\'LL NEED MORE PAPER FOR THIS WALL'
assert WINDOWWIDTH * 3 == WINDOWHEIGHT * 4, 'THE SCREEN\'S A BIT ASCREW'

#defining window margins
MARGIN = (int) (WINDOWHEIGHT * WINDOWWIDTH / 20480)
TOPMARGIN = 5 * MARGIN
BOTTOMMARGIN = MARGIN

#defining symbolic constants
LEFT = -1
CENTER = 0
RIGHT = 1

#defining game parameters
LENGTH = 50
BEGINTIME = (WINDOWHEIGHT - TOPMARGIN - BOTTOMMARGIN) * 3
BONUS = 10

#defining game play parameters
FPS = 100
SPEED = (int) (WINDOWHEIGHT / (2 * FPS))

#defining in-game messages
LAW = ('TOUGH LUCK', '', 'NOT BAD', 'BETTER', 'BRILLIANT', 'TAKE A BOW')
INLAW = ('THE RULES ARE SIMPLE, THE GAME IS NOT', 'FOR THOSE WHO PLEASURE SOUGHT :', 'USE THE KEYS, LEFT AND RIGHT,', 'TO ALLEVIATE YOUR POOR PLIGHT.', 'YOU MUST \'MEMBER TO WATCH YOUR HEALTH', 'AS YOU SET ABOUT TO MIND YOUR WEALTH.', 'ENTER SPACES, NOW AND THEN,', 'TO DOUBLE YOUR BALLS, THEN AGAIN :', 'TOO MUCH, TOO LITTLE. BE A MAN', 'AND SCORE, IF YOU CAN.')
OUTLAW = ('BUT ONLY THOSE FEW, TRULY BRAVE,', 'AND FEWER STILL, WHO GREATNESS CRAVE,', 'WOULD RETURN TO THE GAME', 'AND NOT ESCAPE, ALL THE SAME.')
LAWYER = ('SCORE : http://www.bensound.com/royalty-free-music/track/jazzy-frenchy', 'SOUNDS : http://www.pacdv.com/sounds/mechanical_sound_effects/ cling_1.wav, cling_2.wav', 'BACKGROUND : http://www.hdwalls.info/wallpapers/2013/05/black-background-fabric-ii--480x640.jpg', '', 'CODE : AMITRAJIT SARKAR : aaiijmrtt@gmail.com')

def main():

	global SCREEN, SURFACE, BACKGROUND, LARGEFONT, FONT, SMALLFONT, TIMER, BALL, PADDLE, SOUNDBALLS, SOUNDPADDLE, BEST

	#initiazling pygame module
	pygame.init()

	TIMER = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	SURFACE = pygame.Surface.convert_alpha(SCREEN)
	BACKGROUND = pygame.image.load('background.jpg').convert()
	LARGEFONT = pygame.font.Font('freesansbold.ttf', MARGIN * 8 / 5)
	FONT = pygame.font.Font('freesansbold.ttf', MARGIN)
	SMALLFONT = pygame.font.Font('freesansbold.ttf', MARGIN * 4 / 5)
	SOUNDBALLS = pygame.mixer.Sound('ball.wav')
	SOUNDPADDLE = pygame.mixer.Sound('paddle.wav')
	BEST = 0

	pygame.display.set_caption('BALLS')
	pygame.mixer.music.load('score.mp3')
	pygame.mixer.music.play(-1, 0)

	#initializing pregame parameters and displaying pregame messages
	pregame()
	begin()

	#main game loop
	while True:

		#initializing game parameters
		initialize()

		while len(BALLS) > 0 and TIME > 0 and PADDLE [3] > 0:

			#checking game events
			check()

			#updating game state
			update()

			#rendering updated state
			paint()

			TIMER.tick(FPS)

		#updating highscore
		if SCORE > BEST:
			BEST = SCORE

		#checking for game overs
		if end():
			exit()

#function to initialize game parameters
def initialize():

	global  BALLS, PADDLE, TIME, SCORE, COUNT, PAUSE

	BALLS = [[MARGIN, TOPMARGIN, SPEED, SPEED]]
	PADDLE = [WINDOWWIDTH / 2, WINDOWHEIGHT - 2 * BOTTOMMARGIN, 0, LENGTH]
	TIME = BEGINTIME
	SCORE = 0
	COUNT = 1
	PAUSE = False

#function to display messages on screen
def messages(text, font, color, leftness, upness, position):

	textsurf = font.render(text, True, color)
	textrect = textsurf.get_rect()
	if position == CENTER:
		textrect.midtop = (leftness, upness)
	elif position == LEFT:
		textrect.topleft = (leftness, upness)
	elif position == RIGHT:
		textrect.topright = (leftness, upness)
	SURFACE.blit(textsurf, textrect)
	return textrect.left

#function to pause
def wait(proceed):

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				exit()
			elif event.type == KEYUP or event.type == MOUSEBUTTONUP:
				return proceed

#function to display startup screen
def pregame():

	backrect = BACKGROUND.get_rect()
	SURFACE.blit(BACKGROUND, backrect)

	messages('BALLS', LARGEFONT, BLUE, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 5 * MARGIN, CENTER)
	messages('PRESS SOMETHING', SMALLFONT, GREEN, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 5 * MARGIN, CENTER)
	messages('CLICK ANYTHING', SMALLFONT, GREEN, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 7 * MARGIN, CENTER)

	SCREEN.blit(SURFACE, SURFACE.get_rect())
	pygame.display.update()
	wait(True)

#function to display pregame messages
def begin():

	backrect = BACKGROUND.get_rect()
	SURFACE.blit(BACKGROUND, backrect)

	for i in range(10):
		messages(INLAW[i], FONT, BLUE, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + ( 2 * i - 9 ) * MARGIN, CENTER)

	SCREEN.blit(SURFACE, SURFACE.get_rect())
	pygame.display.update()
	wait(True)

#function to update game state
def update():

	global  BALLS, PADDLE, TIME, SCORE, COUNT

	COUNT = len(BALLS)
	TIME -= COUNT
	PADDLE[3] = (int) (2 * (LENGTH - TIME / 50))

	for ball in BALLS:
		lost = False
		if ball[0] < MARGIN and ball[2] < 0:
			ball[2] = SPEED * COUNT
		elif ball[0] > WINDOWWIDTH - MARGIN and ball[2] > 0:
			ball[2] = - SPEED * COUNT
		if ball[1] < TOPMARGIN and ball[3] < 0:
			ball[3] = SPEED * COUNT
		elif ball[1] > PADDLE[1] and ball[3] > 0:
			if ball[0] < PADDLE[0] + PADDLE[3] / 2  and ball[0] + PADDLE[3] / 2 > PADDLE[0]:
				ball[3] = -SPEED * COUNT
				TIME *= 2
				SCORE += BONUS * COUNT
				SOUNDPADDLE.play()
			else:
				lost = True
		ball[0] += ball[2]
		ball[1] += ball[3]
		if lost:
			BALLS.remove(ball)

	if PADDLE[0] < MARGIN + PADDLE[3] / 2:
		PADDLE[0] = MARGIN + PADDLE[3] / 2
		if PADDLE[2] < 0:
			PADDLE[2] = 0
	elif PADDLE[0] > WINDOWWIDTH - MARGIN - PADDLE[3] / 2:
		PADDLE[0] = WINDOWWIDTH - MARGIN - PADDLE[3] / 2
		if PADDLE[2] > 0:
			PADDLE[2] = 0
	PADDLE[0] += PADDLE[2]

#function to check for game events
def check():

	global  BALLS, PADDLE, SCORE

	events = pygame.event.get()
	for event in events:
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			exit()
		elif event.type == KEYUP and event.key == K_RETURN:
			wait(True)
		elif (event.type == KEYDOWN and event.key == K_LEFT) or pygame.key.get_pressed()[K_LEFT]:
			if PADDLE[2] < 0 :
				PADDLE[2] -= 3 * SPEED
			else:
				PADDLE[2] = -3 * SPEED
		elif (event.type == KEYDOWN and event.key == K_RIGHT) or pygame.key.get_pressed()[K_RIGHT]:
			if PADDLE[2] > 0:
				PADDLE[2] += 3 * SPEED
			else:
				PADDLE[2] = 3 * SPEED
		elif event.type == KEYUP and (event.key == K_LEFT or event.key == K_RIGHT):
			PADDLE[2] = 0
		elif (event.type == KEYUP and event.key == K_SPACE) or event.type == MOUSEBUTTONUP:
			newballs = []
			for ball in BALLS:
				newballs.append([ball[0], ball[1], -ball[2], -ball[3]])
			BALLS.extend(newballs)
			SCORE += BONUS * COUNT
			SOUNDBALLS.play()
		elif event.type == MOUSEMOTION:
			mousex, mousey = pygame.mouse.get_pos()
			PADDLE[0] = mousex

#function to render game screen
def paint():

	backrect = BACKGROUND.get_rect()
	SURFACE.blit(BACKGROUND, backrect)

	messages('BEST: ' + str(BEST), FONT, BLUE, MARGIN, TOPMARGIN - 4 * MARGIN, LEFT)
	messages('SCORE: ' + str(SCORE), FONT, BLUE, MARGIN, TOPMARGIN - 2 * MARGIN, LEFT)
	leftwealth = messages('WEALTH', FONT, RED, WINDOWWIDTH - MARGIN, TOPMARGIN - 4 * MARGIN, RIGHT)
	lefthealth = messages('HEALTH', FONT, GREEN, WINDOWWIDTH - MARGIN, TOPMARGIN - 2 * MARGIN, RIGHT)

	pygame.draw.rect(SURFACE, RED, pygame.Rect(leftwealth - MARGIN - (int) (WINDOWWIDTH * TIME / 6000), TOPMARGIN - 4 * MARGIN, max((int) (WINDOWWIDTH * TIME / 6000), 0), MARGIN / 2), 0)
	pygame.draw.rect(SURFACE, GREEN, pygame.Rect(lefthealth -  MARGIN - (int) (WINDOWWIDTH * PADDLE [3] / 200), TOPMARGIN - 2 * MARGIN, max((int) (WINDOWWIDTH * PADDLE [3] / 200 ), 0) , MARGIN / 2), 0)

	if (SCORE / 100) % 2 == 1 and len(BALLS) > 0:
		pygame.draw.rect(SURFACE, WHITE[255 * BALLS [0][1] / WINDOWHEIGHT], pygame.Rect(PADDLE[0] - PADDLE[3] / 2, PADDLE[1], PADDLE[3], BOTTOMMARGIN / 2 ), 0)
	else:
		pygame.draw.rect(SURFACE, WHITE[255], pygame.Rect(PADDLE[0] - PADDLE[3] / 2, PADDLE[1], PADDLE[3], BOTTOMMARGIN / 2), 0)
	for ball in BALLS:
		if (SCORE / 100) % 2 == 1 and len(BALLS) > 0:
			pygame.draw.circle(SURFACE, WHITE[255 * BALLS[0][1] / WINDOWHEIGHT], (ball[0], ball[1]), (int) (MARGIN/3), 0)
		else:
			pygame.draw.circle(SURFACE, WHITE[255], (ball[0], ball[1]), (int)(MARGIN / 3), 0)

	SCREEN.blit(SURFACE, SURFACE.get_rect())
	pygame.display.update()

#function to display endgame messages
def end():

	pygame.time.wait(1000)

	backrect = BACKGROUND.get_rect()
	SURFACE.blit(BACKGROUND, backrect)

	for i in range (5):
		if 10 ** i > SCORE:
			messages((str) (SCORE) + ' : ' + LAW[i], FONT, BLUE, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 7 * MARGIN, CENTER)
			break
	else:
		messages((str) (SCORE) + ' : ' + LAW[5], FONT, BLUE, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 7 * MARGIN, CENTER)

	for i in range (4):
		messages(OUTLAW[i], FONT, GREEN, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + (2 * i - 3) * MARGIN, CENTER)

	SCREEN.blit(SURFACE, SURFACE.get_rect())
	pygame.display.update()
	wait(False)

#function to display postgame messages
def exit():

	pygame.mixer.music.fadeout(2000)

	for j in range (2 * FPS):

		backrect = BACKGROUND.get_rect()
		SURFACE.blit(BACKGROUND, backrect)

		for i in range (5):
			messages(LAWYER[i], SMALLFONT, WHITE[255 - abs(255 - j * 255 / FPS)], WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + (2 * i - 4) * MARGIN, CENTER)

		SCREEN.blit(SURFACE, SURFACE.get_rect())
		pygame.display.update()

	pygame.quit()
	sys.exit()

if __name__ == '__main__':

	main ( )
