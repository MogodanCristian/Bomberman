import pygame
import time
import random
from threading import Timer
from pygame import mixer

def game():
	pygame.init()
	start_game=time.time()
	#dimensions for game and screen creation
	unit=64
	n=15
	m=11
	screen_width=unit*(n+2)
	screen_height=unit*m
	screen=pygame.display.set_mode((screen_width,screen_height))
	pygame.display.set_caption("BomberMan")
	icon=pygame.image.load('bomberman_logo.png')
	pygame.display.set_icon(icon)
	
	#playing background music
	mixer.init()
	mixer.music.load("music.mp3")
	mixer.music.set_volume(0.4)
	mixer.music.play()
	#player 1 initial coordinates and image
	player1_Img=pygame.image.load('player1.png')
	player1_X=0
	player1_Y=0
	player1_lives=3
	player1_score=0
	#player 2 initial coordinates and image
	player2_Img=pygame.image.load('player2.png')
	player2_X=(n-1)*unit
	player2_Y=screen_height-unit
	player2_lives=3
	player2_score=0
	#maze entities images
	stone_img=pygame.image.load('stone.png')
	brick_img=pygame.image.load('brick.png')
	plus_life=pygame.image.load('heart.png')
	longer_attack_img=pygame.image.load('aim.png')
	bomb_Img=pygame.image.load('bomb.png')
	explosion_Img=pygame.image.load('explosion.png')
	invincible_img=pygame.image.load('skull.png')
	#draw functions for bombs and players
	def player1(x,y):
		screen.blit(player1_Img,(x,y))
	def player2(x,y):
		screen.blit(player2_Img,(x,y))
	def bomb(x,y):
		screen.blit(bomb_Img,(x,y))
	def explosion(y,x):
		screen.blit(explosion_Img,(y,x))
	bomb1_X=0
	bomb1_Y=0
	bomb2_X=0
	bomb2_Y=0
	#draw functions for the maze entities
	def stone(x,y):
		screen.blit(stone_img,(x,y))
	def brick(x,y):
			screen.blit(brick_img,(x,y))
	def heart(x,y):
		screen.blit(plus_life,(x,y))
	def longer_attack(x,y):
		screen.blit(longer_attack_img,(x,y))
	def invincible(x,y):
		screen.blit(invincible_img,(x,y))
		
	#maze initial coordinates
	maze_mat=[[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
	[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]
	
	#function that randomly generates a maze
	def set_matrix():
			for i in range(m):
				for j in range(n):
					if (maze_mat[i][j]==0) and not(i==0 and j==0) and not(i==0 and j==1) and not(i==1 and j==0) and not(i==10 and j==14) and not(i==9 and j==14) and not(i==10 and j==13):
						maze_mat[i][j]=random.choice([0,0,2,2,0,2,2,2,2,2,0])
	#draw functions for maze
	def draw_maze():
			for i in range(m):
				for j in range(n):
					if maze_mat[i][j]==1:
						stone(j*unit,i*unit)
					elif  maze_mat[i][j]==2:
						brick(j*unit,i*unit)
					elif maze_mat[i][j]==7:
						invincible(j*unit,i*unit)
					elif maze_mat[i][j]==8:
						heart(j*unit,i*unit)
					elif maze_mat[i][j]==9:
						longer_attack(j*unit,i*unit)
	#checking if you are trying to step on a brick or stone
	def colisions(x,y):
		if(maze_mat[int(y/unit)][int(x/unit)]==1 or maze_mat[int(y/unit)][int(x/unit)]==2):
			return 0
		return 1
	def generate_value():
		return random.choice([0,0,0,0,0,0,0,0,0,7,8,9])
	#checking if there is a wall that can explode
	longer_attack_p1=1
	longer_attack_p2=1
	def wall_explosion(x,y,long_attack):
		
		nonlocal walls_destroyed
		if x<(n-1)*unit:
			if maze_mat[int(y/unit)][int((x+unit)/unit)]!=1:
				for j in range (int(x/unit)+1,int(x/unit)+2+long_attack):
					if j>=n:
						break
					explosion(j*unit,y)
					if maze_mat[int(y/unit)][j]==2:
						maze_mat[int(y/unit)][j]=generate_value()
						explosion(j*unit,y)
						walls_destroyed+=1
						break
		if x>0:
			if maze_mat[int(y/unit)][int((x-unit)/unit)]!=1:
				for j in range (int(x/unit)-1,int(x/unit)-2-long_attack,-1):
					if j<0:
						break
					explosion(j*unit,y)
					if maze_mat[int(y/unit)][j]==2:
						maze_mat[int(y/unit)][j]=generate_value()
						explosion(j*unit,y)
						walls_destroyed+=1
						break
		if y<(m-1)*unit:
			if maze_mat[int((y+unit)/unit)][int(x/unit)]!=1:
				for i in range (int(y/unit)+1,int(y/unit)+2+long_attack):
					if i>=m:
						break
					explosion(x,i*unit)
					if maze_mat[i][int(x/unit)]==2:
						maze_mat[i][int(x/unit)]=generate_value()
						explosion(x,i*unit)
						walls_destroyed+=1
						break
		if y>0:
			if maze_mat[int((y-unit)/unit)][int(x/unit)]!=1:
				for i in range (int(y/unit)-1,int(y/unit)-2-long_attack,-1):
					if i<0:
						break
					explosion(x,i*unit)
					if maze_mat[i][int(x/unit)]==2:
						maze_mat[i][int(x/unit)]=generate_value()
						explosion(x,i*unit)
						walls_destroyed+=1
						break
	def is_there_a_block_between_x(x,p_x,y):
		if p_x<x:
			for i in range (int(p_x/unit),int(x/unit)):
				if maze_mat[int(y/unit)][i]==1 or maze_mat[int(y/unit)][i]==2:
					return True
		if p_x>x:
			for i in range (int(p_x/unit),int(x/unit),-1):
				if maze_mat[int(y/unit)][i]==1 or maze_mat[int(y/unit)][i]==2:
					return True
		return False
	def is_there_a_block_between_y(y,p_y,x):
		if p_y<y:
			for i in range (int(p_y/unit),int(y/unit)):
					if maze_mat[i][int(x/unit)]==1 or maze_mat[i][int(x/unit)]==2:
						return True
		if p_y>y:
			for i in range (int(p_y/unit),int(y/unit),-1):
					if maze_mat[i][int(x/unit)]==1 or maze_mat[i][int(x/unit)]==2:
						return True
		return False
	invincible_p1=False
	invincible_p2=False
	def is_player_hit(x,y,p_x,p_y,long,invincible):
		if (p_x>=x-unit*(1+long) and p_y==y and p_x<=x+unit*(1+long) and invincible==False):
			if is_there_a_block_between_x(x,p_x,y)==False:
				return 1
		if (p_y>=y-unit*(1+long) and p_x==x and p_y<=y+unit*(1+long) and invincible==False):
			if  is_there_a_block_between_y(y,p_y,x)==False:
				return 1
		return 0
	
	font=pygame.font.Font('freesansbold.ttf',16)
	def show_player1_lives(x,y):
		disp_player1_lives=font.render("P1 lives: "+ str(player1_lives),True,(0,0,0))
		screen.blit(disp_player1_lives,(x,y))
	
	def show_player2_lives(x,y):
		disp_player2_lives=font.render("P2 lives: "+ str(player2_lives),True,(0,0,0))
		screen.blit(disp_player2_lives,(x,y))	
	
	def show_player1_score(x,y):
		disp_player1_score=font.render("P1 score: "+str(player1_score),True,(0,0,0))
		screen.blit(disp_player1_score,(x,y))
	
	def show_player2_score(x,y):
		disp_player2_score=font.render("P2 score: "+str(player2_score),True,(0,0,0))
		screen.blit(disp_player2_score,(x,y))
	
	#variables that enable to plant just one bomb
	bomb1=False
	bomb2=False
	#randomly generate new values for the matrix
	set_matrix()
	#timers for bombs to explode
	start_time_player_1=0
	start_time_player_2=0
	
	#variables that dont allow the player to plant another bomb until the initial one exploded
	is_planted_player_1=False
	is_planted_player_2=False
	is_first_iteration_player1=True
	is_first_iteration_player2=True
	is_first_iteration_insanity=True
	invincible_start_p1=time.time()
	def player1_makes_pickup(x,y):
		nonlocal longer_attack_p1
		nonlocal player1_lives
		nonlocal invincible_p1
		nonlocal invincible_start_p1
		if(maze_mat[int(y/unit)][int(x/unit)]==7):
			maze_mat[int(y/unit)][int(x/unit)]=0
			invincible_start_p1=time.time()
			invincible_p1=True
		if(maze_mat[int(y/unit)][int(x/unit)]==8):
			player1_lives+=1
			maze_mat[int(y/unit)][int(x/unit)]=0
		if(maze_mat[int(y/unit)][int(x/unit)]==9):
			longer_attack_p1+=1
			maze_mat[int(y/unit)][int(x/unit)]=0
	invincible_start_p2=time.time()
	def player2_makes_pickup(x,y):
		nonlocal longer_attack_p2
		nonlocal player2_lives
		nonlocal invincible_p2
		nonlocal invincible_start_p2
		if(maze_mat[int(y/unit)][int(x/unit)]==7):
			maze_mat[int(y/unit)][int(x/unit)]=0
			invincible_start_p2=time.time()
			invincible_p2=True
		if(maze_mat[int(y/unit)][int(x/unit)]==8):
			player2_lives+=1
			maze_mat[int(y/unit)][int(x/unit)]=0
		if(maze_mat[int(y/unit)][int(x/unit)]==9):
			longer_attack_p2+=1
			maze_mat[int(y/unit)][int(x/unit)]=0

	font2=pygame.font.Font('freesansbold.ttf',45)
	insanity_start=False
	
	#--------------------GAME LOOP-------------------------
	insanity_start_time=time.time()
	clock=pygame.time.Clock()
	running=True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
			if event.type == pygame.KEYDOWN:
				#Movement player1 and restrictions
				if event.key == pygame.K_LEFT and player1_X > 0 and colisions(player1_X-unit,player1_Y)==1:
					player1_X-=unit
				if event.key == pygame.K_RIGHT and player1_X < (n-1)*unit and colisions(player1_X+unit,player1_Y)==1:
					player1_X+=unit
				if event.key == pygame.K_UP and player1_Y > 0 and colisions(player1_X,player1_Y-unit)==1:
					player1_Y-=unit
				if event.key == pygame.K_DOWN and player1_Y < screen_height-unit and colisions(player1_X,player1_Y+unit)==1:
					player1_Y+=unit
				#pause
				if event.key==pygame.K_p:
					pause=True
					pause_text=font2.render("Pause",True,(0,0,0))
					while pause:
						screen.blit(pause_text,(420,300))
						for event in pygame.event.get():
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_p:
									pause=False
						pygame.display.update()
							
				#Movement player2 and restrictions
				if event.key == pygame.K_a and player2_X > 0 and colisions(player2_X-unit,player2_Y)==1:
					player2_X-=unit
				if event.key == pygame.K_d and player2_X < (n-1)*unit and colisions(player2_X+unit,player2_Y)==1:
					player2_X+=unit
				if event.key == pygame.K_w and player2_Y > 0 and colisions(player2_X,player2_Y-unit)==1:
					player2_Y-=unit
				if event.key == pygame.K_s and player2_Y < screen_height-unit and colisions(player2_X,player2_Y+unit)==1:
					player2_Y+=unit
				#Planting the player1 bomb
				if event.key == pygame.K_SPACE and is_planted_player_1 == False:
					bomb1=True
					bomb1_X=player1_X
					bomb1_Y=player1_Y
					start_time_player_1=time.time()
					is_planted_player_1=True
					is_first_iteration_player1=True
				#Planting the player2 bomb
				if event.key == pygame.K_f and is_planted_player_2 == False:
					bomb2=True
					bomb2_X=player2_X
					bomb2_Y=player2_Y
					start_time_player_2=time.time()
					is_planted_player_2=True
					is_first_iteration_player2=True
		screen.fill((100,192,119))
		if bomb1==True:
			bomb(bomb1_X,bomb1_Y)
		if bomb2==True:
			bomb(bomb2_X,bomb2_Y)
		player1(player1_X,player1_Y)
		player2(player2_X,player2_Y)
		draw_maze()
		player1_makes_pickup(player1_X,player1_Y)
		player2_makes_pickup(player2_X,player2_Y)
		show_player1_lives(n*unit,0)
		show_player1_score(n*unit,unit/2)
		show_player2_lives(n*unit,unit)
		show_player2_score(n*unit,unit+unit/2)
		if player1_lives==0:
			if(player2_score>player1_score):
				p2_won=font2.render("Player 2 won!!!!!!!!",True,(0,0,0))
				screen.blit(p2_won,(350,220))
				pygame.display.update()
				time.sleep(3)
				running=False
			elif (player1_score>player2_score):
				p1_won=font2.render("Player 1 won!!!!!!!!",True,(0,0,0))
				screen.blit(p1_won,(350,220))
				pygame.display.update()
				time.sleep(3)
				running=False
			elif(player1_score==player2_score):
				p1_won=font2.render("Remiza!!!!!",True,(0,0,0))
				screen.blit(p1_won,(400,220))
				pygame.display.update()
				time.sleep(3)
				running=False
		if player2_lives==0:
			if (player1_score>player2_score):
				p1_won=font2.render("Player 1 won!!!!!!!!",True,(0,0,0))
				screen.blit(p1_won,(350,220))
				pygame.display.update()
				time.sleep(3)
				running=False
			if(player2_score>player1_score):
				p2_won=font2.render("Player 2 won!!!!!!!!",True,(0,0,0))
				screen.blit(p2_won,(350,220))
				pygame.display.update()
				time.sleep(3)
				running=False
			elif(player1_score==player2_score):
				p1_won=font2.render("Remiza!!!!!",True,(0,0,0))
				screen.blit(p1_won,(400,220))
				pygame.display.update()
				time.sleep(3)
				running=False
		if invincible_p1==True and int(time.time()-invincible_start_p1)==5:
			invincible_p1=False
		if invincible_p2==True and int(time.time()-invincible_start_p2)==5:
			invincible_p2=False
		if int(time.time()-start_time_player_1)==1 and is_first_iteration_player1==True:
			explosion_sound=mixer.Sound("explosion.wav")
			explosion_sound.play()
			walls_destroyed=0
			bomb1=False
			is_planted_player_1 = False
			wall_explosion(bomb1_X,bomb1_Y,longer_attack_p1)
			player1_score+=10*walls_destroyed
			if is_player_hit(bomb1_X,bomb1_Y,player1_X,player1_Y,longer_attack_p1,invincible_p1)==1:
				player1_X=0
				player1_Y=0
				player1_lives-=1
				player1_score-=50
				death_sound=mixer.Sound("death.wav")
				death_sound.play()
			if is_player_hit(bomb1_X,bomb1_Y,player2_X,player2_Y,longer_attack_p1,invincible_p2)==1:
				player2_X=(n-1)*unit
				player2_Y=screen_height-unit
				player2_lives-=1
				player1_score+=50
				death_sound=mixer.Sound("death.wav")
				death_sound.play()
			is_first_iteration_player1=False
		if int(time.time()-start_time_player_2)==1 and is_first_iteration_player2==True:
			explosion_sound=mixer.Sound("explosion.wav")
			explosion_sound.play()
			explosion(bomb2_X,bomb2_Y)
			walls_destroyed=0
			bomb2=False
			is_planted_player_2 = False
			wall_explosion(bomb2_X,bomb2_Y,longer_attack_p2)
			player2_score+=10*walls_destroyed
			if is_player_hit(bomb2_X,bomb2_Y,player1_X,player1_Y,longer_attack_p1,invincible_p1)==1:
				player1_X=0
				player1_Y=0
				player2_score+=50
				player1_lives-=1
				death_sound=mixer.Sound("death.wav")
				death_sound.play()
			if is_player_hit(bomb2_X,bomb2_Y,player2_X,player2_Y,longer_attack_p2,invincible_p2)==1:
				player2_X=(n-1)*unit
				player2_Y=screen_height-unit
				player2_lives-=1
				player2_score-=50
				death_sound=mixer.Sound("death.wav")
				death_sound.play()
			is_first_iteration_player2=False
		if int (time.time()-start_game)==20:
			insanity_text=font2.render("GET PSYCHED!!",True,(0,0,0))
			screen.blit(insanity_text,(420,300))
			insanity_start=True
			insanity_start_time=time.time()			
		if int(time.time()-insanity_start_time)==1:
			is_first_iteration_insanity=True
		if insanity_start==True and is_first_iteration_insanity==True:
			x=random.randint(0,n-1)
			y=random.randint(0,m-1)
			while maze_mat[y][x]==1:
				x=random.randint(0,n-1)
				y=random.randint(0,m-1)
			maze_mat[y][x]=1
			is_first_iteration_insanity=False
			insanity_start_time=time.time()
		if maze_mat[int(player1_Y/unit)][int(player1_X/unit)]==1:
			player1_lives=0
		if maze_mat[int(player2_Y/unit)][int(player2_X/unit)]==1:
			player2_lives=0
		pygame.display.update()