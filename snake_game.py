#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time　　   :2019/11/23 19:05
# @Author　   :ZuoZhu
# @ File　　  :snake_game.py
# @Software   :PyCharm

import pygame;
import random;
import copy;
import sys;
from pygame.color import THECOLORS
import time;

class Snake(object):
    def __init__(self):
        # 蛇的模型
        self.snake_list = [[10, 10]];
        self.snake_sourece = 100;
        # 食物模型
        self.snake_foo_point = [random.randint(10, 490), random.randint(10, 490)];
        self.my_rect = [random.randint(10, 490), random.randint(10, 490), 10, 10]
        # 初始化键盘
        self.move_up = False;
        self.move_down = False;
        self.move_left = False;
        self.move_right = False;
        # 设置游戏帧数
        self.clock = pygame.time.Clock();
        # 设置画布
        self.screen = pygame.display.set_mode((500, 500));
        # 游戏主题
        self.title = pygame.display.set_caption('贪吃游戏');
        # 初始化
        pygame.init();



    # 获取事件
    def get_event(self):
        return pygame.event.get();

    # 设置本游戏的事件
    def set_keyDown(self):
        event_list = self.get_event();
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit(0);
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_up = True;
                    self.move_down = False;
                    self.move_left = False;
                    self.move_right = False;
                elif event.key == pygame.K_DOWN:
                    self.move_up = False;
                    self.move_down = True;
                    self.move_left = False;
                    self.move_right = False;
                elif event.key == pygame.K_LEFT:
                    self.move_up = False;
                    self.move_down = False;
                    self.move_left = True;
                    self.move_right = False;
                elif event.key == pygame.K_RIGHT:
                    self.move_up = False;
                    self.move_down = False;
                    self.move_left = False;
                    self.move_right = True;



    # 蛇移动
    def snake_running(self):
        snake_len = len(self.snake_list) - 1;
        # 身体移动
        while snake_len>0:
            self.snake_list[snake_len] = copy.deepcopy(self.snake_list[snake_len - 1]);
            snake_len -= 1;
        # 蛇头移动
        if self.move_up:
            self.snake_list[snake_len][1] -= 10;
            if self.snake_list[snake_len][1] < 0:
                self.snake_list[snake_len][1] = 500
        elif self.move_down:
            self.snake_list[snake_len][1] += 10;
            if self.snake_list[snake_len][1] > 500:
                self.snake_list[snake_len][1] = 0;
        elif self.move_left:
            self.snake_list[snake_len][0] -= 10;
            if self.snake_list[snake_len][0] < 0:
                self.snake_list[snake_len][0] = 500;
        elif self.move_right:
            self.snake_list[snake_len][0] += 10;
            if self.snake_list[snake_len][0] > 500:
                self.snake_list[snake_len][0] = 0;


    def if_collidepoint(self,snake_list_rect):
        snake_head = snake_list_rect[0];
        count_rect = len(snake_list_rect);
        while count_rect>1:
            print('到了这里吗？我是z方法')
            if snake_head.colliderect(snake_list_rect[count_rect-1]):
                pygame.quit();
                sys.exit(0);
            count_rect-=1;

    # 游戏开始
    def game_start(self):
        print('启动游戏开始............')
        while True:
            # 填充背景颜色
            self.screen.fill([255,255,255]);
            # 设置帧数
            self.clock.tick(15);
            self.set_keyDown();
            self.snake_running();
            # 显示食物
            foot_rect = pygame.draw.circle(self.screen, THECOLORS['red'], self.snake_foo_point, 10);
            # 存取蛇的绘画点的信息,为后面碰撞解决的事情
            snake_list_rect = [];
            # 显示蛇
            for pos in self.snake_list:
                snake_rect = pygame.draw.circle(self.screen, THECOLORS['green'], pos, 5);
                snake_list_rect.append(snake_rect);
                if foot_rect.collidepoint(pos):
                    self.snake_list.append(self.snake_foo_point);
                    # 分数+100
                    self.snake_sourece += 100;
                    self.snake_foo_point = [random.randint(10,490),random.randint(10,490)];
                    break;
            self.if_collidepoint(snake_list_rect);
            pygame.display.update();



if __name__ == '__main__':
    s = Snake();
    s.game_start();





