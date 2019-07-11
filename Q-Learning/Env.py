import numpy as np
import pandas as pd
import time 

class Env:
    def __init__(self,column,maze_column):
        self.column = column                        #表示地图的长度
        self.maze_column = maze_column - 1          #宝藏所在的位置
        self.x = 0                                  #初始化x
        self.map = np.arange(column)                #给予每个地点一个标号
        self.count = 0                              #用于技术一共走了多少步
        

    def draw(self):
        a = []
        for j in range(self.column) :               #更新图画
            if j == self.x:
                a.append('o')
            elif j == self.maze_column:
                a.append('m')
            else:
                a.append('_')
        interaction = ''.join(a)
        print('\r{}'.format(interaction),end = '')
        

    def get_observation(self):
        return self.map[self.x]                     #返回现在在所


    def get_terminal(self):
        if self.x == self.maze_column:              #如果得到了宝藏，则返回已经完成
            done = True
        else:
            done = False
        return done


    def update_place(self,action):
        self.count += 1                              #更新的时候表示已经走了一步
        if action == 'right':                                  
            if self.x < self.column - 1:
                self.x += 1
        elif action == 'left':   #left
            if self.x > 0:
                self.x -= 1

    def get_prediction(self,action):
        if action == 'right':                        #获得预测位置，并获得在预测位置是否拿到宝藏
            if self.x + 1 == self.maze_column:
                score = 1
                pre_done = True
            else:
                score = 0
                pre_done = False
            return self.map[self.x + 1],score,pre_done
        elif action == 'left':   #left
            if self.x - 1 == self.maze_column:
                score = 1
                pre_done = Ture
            else:
                score = 0
                pre_done = False
            return self.map[self.x - 1],score,pre_done
        


    def retry(self):            #初始化
        self.x = 0
        self.count = 0