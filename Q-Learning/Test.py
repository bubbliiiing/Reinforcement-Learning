from Env import Env
from QL import QL
import numpy as np
import time

LONG = 6                    #总长度为6
MAZE_PLACE = 6              #宝藏在第6位
TIMES = 15                  #进行15次迭代

people = QL(['left','right'])       #生成QLearn主体的对象，包含left和right
site = Env(LONG,MAZE_PLACE)         #生成测试环境
for episode in range(TIMES):
    state = site.get_observation()  #观察初始环境
    site.draw()                     #生成图像
    time.sleep(0.3)                 #暂停
    while(1):
        done = site.get_terminal()  #判断当前环境是否到达最后
        if done:                    #如果到达，则初始化
            interaction = '\n第%s次世代，共使用步数：%s。'%(episode+1 ,site.count)
            print(interaction)
            site.retry()
            time.sleep(2)
            break
        action = people.choose_action(state)                        #获得下一步方向
        state_after,score,pre_done = site.get_target(action)    #获得下一步的环境的实际情况
        people.learn(state,action,score,state_after,pre_done)       #根据所处的当前环境对各个动作的预测得分和下一步的环境的实际情况更新当前环境的q表
        site.update_place(action)                                   #更新位置
        state = state_after                                         #状态更新
        site.draw()                                                 #更新画布
        time.sleep(0.3)
    

print(people.q_table)
