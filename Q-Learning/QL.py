import numpy as np
import pandas as pd

class QL:
    def __init__(self, actions, learning_rate=0.05, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions      #初始化可以进行的各种行为，传入为列表
        self.lr = learning_rate     #学习率，用于更新Q_table的值
        self.gamma = reward_decay   #当没有到达终点时，下一环境对当前环境的影响
        self.epsilon = e_greedy     #随机选择几率为1-e_greedy，当处于e_greedy内时，不随机选择。
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)     #生成q_table，列向量为columns

    def choose_action(self,observation):
        self.check_observation(observation)        #检测是否到达过这个点，如果没到达过，在Q表中增加这个节点
        action_list = self.q_table.loc[observation,:]           #取出当前observation所在的不同方向
        
        if(np.random.uniform() < self.epsilon):    #如果在epsilon几率内
            action = np.random.choice(action_list[action_list == np.max(action_list)].index)    #选出当前observation中Q值最大的方向
        else:
            action = np.random.choice(self.actions)      #如果不在epsilon内，则随机选择一个动作
        return action                                    #返回应当做的action

    def learn(self,observation_now,action,score,observation_after,done):
        self.check_observation(observation_after)        #检查是否存在下一环境对应的方向状态
        q_predict = self.q_table.loc[observation_now,action]        #获得当前状态下，当前所作动作所对应的预测得分
        if done:
            q_target = score     #如果完成了则q_target为下一个环境的实际情况得分，本例子中此时score为1
        else:
            q_target = score + self.gamma * self.q_table.loc[observation_after, :].max()  #如果未完成则取下一个环境若干个动作中的最大得分作为这个环境的价值传递给当前环境
        #根据所处的当前环境对各个动作的预测得分和下一步的环境的实际情况更新当前环境的q表
        self.q_table.loc[observation_now, action] += self.lr * (q_target - q_predict)  

    def check_observation(self,observation):
        if observation not in self.q_table.index:               #如果不存在 
            self.q_table = self.q_table.append(                 #则通过series函数生成新的一列
                pd.Series(
                    [0]*len(self.actions),
                    index=self.actions,
                    name=observation,)
            )
