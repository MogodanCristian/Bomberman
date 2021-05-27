import pygame
import time
import random
import threading

stone_img=pygame.image.load('stone.png')
brick_img=pygame.image.load('brick.png')
def stone(x,y):
	screen.blit(stone_img,(x,y))
def brick(x,y):
		screen.blit(brick_img,(x,y))
unit=64
screen_width=unit*15
screen_height=unit*11
n=15
m=11
class maze:
	screen=pygame.display.set_mode((screen_width,screen_height))
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
	
	def set_matrix():
		for i in range(m):
			for j in range(n):
				if (maze_mat[i][j]==0) and not(i==0 and j==0) and not(i==0 and j==1) and not(i==1 and j==0) and not(i==10 and j==14) and not(i==9 and j==14) and not(i==10 and j==13):
					maze_mat[i][j]=random.choice([2,2,2,2,0])
	def draw_maze():
		for i in range(m):
			for j in range(n):
				if maze_mat[i][j]==1:
					stone(j*unit,i*unit)
				elif  maze_mat[i][j]==2:
					brick(j*unit,i*unit)
