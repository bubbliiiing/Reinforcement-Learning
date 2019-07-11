import numpy as np
import pandas as pd

class QL:
    def __init__(self, actions, learning_rate=0.05, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions      #初始化可以进行的各种行为，传入为列表
        self.lr = learning_rate     #学习率，用于更新Q_table的值
        self.gamma = reward_decay   #当没有到达终点时，pre预测值对原值的影响
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
        self.check_observation(observation_after)        #检查是否存在预测状态对应的方向状态
        q_predict = self.q_table.loc[observation_now,action]        #预测状态对应的Q值
        if done:
            q_influence = score     #如果完成了则预测状态对当前的Q值影响的为score，本例子中此时score为1
        else:
            q_influence = score + self.gamma * self.q_table.loc[observation_after, :].max()  #如果完成了则预测状态对当前的Q值影响的为score+预测状态各个方向最大的Q值，本例子中此时score为0
        self.q_table.loc[observation_now, action] += self.lr * (q_influence - q_predict)  #更新当前观测状态对应的Q值

    def check_observation(self,observation):
        if observation not in self.q_table.index:               #如果不存在 
            self.q_table = self.q_table.append(                 #则通过series函数生成新的yi'lie
                pd.Series(
                    [0]*len(self.actions),
                    index=self.actions,
                    name=observation,)
            )