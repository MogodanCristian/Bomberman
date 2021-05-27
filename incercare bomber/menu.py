import incercare_bomber
import pygame

pygame.init()
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
font=pygame.font.Font('freesansbold.ttf',32)
font1=pygame.font.Font('freesansbold.ttf',64)
disp_message1=font1.render("-----------------BomberMan-----------------",True,(255,255,255))
disp_message=font.render("Start game...? Y/N",True,(255,255,255))
screen.fill((100,192,119))
screen.blit(disp_message1,(0,100))
screen.blit(disp_message,(400,300))
pygame.display.update()
running_menu=True
try_again_msg=font.render("Play again? Y/N",True,(255,255,255))
while running_menu:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running_menu=False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_y:
				incercare_bomber.game()
				screen.blit(try_again_msg,(400,300))
				pygame.display.update()
			if event.key == pygame.K_n:
				running_menu=False


