#!/usr/bin/env python
# coding: utf-8

# In[16]:


import collections,copy
import pygame
from pygame.locals import *
import sys, random


#SB:1$, BB:2$, Everyone has 100$ at first.
SB,BB = 1,2
buy_in = 100
how_many_p = 2
pot = 0
tips = []
f_tips = []
if_actioned = []
if_noplay = []
for i in range(how_many_p):
    tips.append(buy_in)
    f_tips.append(0)
    if_actioned.append(0)
    if_noplay.append(0)
#f_tips means tips in front of the player

whoBB = random.randrange(how_many_p)
def pay_SB_BB():
    global tips,f_tips,whoBB,if_actioned
    
    whoBB = (whoBB + 1) % how_many_p
    whoSB = whoBB - 1
    x = 0
    y = 0
    if tips[whoBB] < BB:
        f_tips[whoBB] = tips[whoBB]
        tips[whoBB] = 0
        if_actioned[whoBB] = 1
        x = 1
    if tips[whoSB] < SB:
        f_tips[whoSB] = tips[whoSB]
        tips[whoSB] = 0
        if_actioned[whoSB] = 1
        y = 1
        
    if x == 0:
        tips[whoBB] -= BB
        f_tips[whoBB] += BB
    if y == 0:
        tips[whoSB] -= SB
        f_tips[whoSB] += SB    

def bet(n,money):
    global tips,f_tips,if_actioned
    
    if f_tips[n] != 0:
        print("You cannot bet.")
        return False
    elif tips[n] < money or money < BB:
        print("You cannot bet",money)
        return False
    else:
        tips[n] -= money
        f_tips[n] += money
        if_actioned[n] = 1
        return True

def rai_se(n,money):
    global tips,f_tips,if_actioned
    f_tips2 = f_tips
    f_tips2.sort()
    
    if tips[n] + f_tips[n] < money:
        print("You cannot raise",money)
        return False
    elif sum(f_tips) == 0 or money < max(f_tips) + f_tips2[-2]:
        print("You cannot raise.")
        return False
    else:
        tips[n] += f_tips[n] - money
        f_tips[n] = money
        if_actioned[n] = 1
        return True

def call(n):
    global tips,f_tips,if_actioned
    
    if sum(f_tips) == 0:
        print("You cannot call.")
        return False
    elif max(f_tips) > tips[n] + f_tips[n]:
        f_tips[n] += tips[n]
        tips[n] = 0
        if_actioned[n] = 1
        return True
    else:
        tips[n] -= max(f_tips) - f_tips[n]
        f_tips[n] = max(f_tips)
        if_actioned[n] = 1
        return True

def fold(n):
    global f_tips,pot,if_actioned,if_noplay
    
    if f_tips[n] == max(f_tips) or tips[n] == 0:
        print("You cannot fold.")
        return False
    else:
        pot += f_tips[n]
        f_tips[n] = 0
        if_actioned[n] = 1
        if_noplay[n] = 1   
        return True

def check(n):
    global if_actioned
    
    if f_tips[n] == max(f_tips):
        if_actioned[n] = 1
        return True
    else:
        print("You cannot check.")
        return False
        
def if_next():
    if 0 in if_actioned:
        return False
    else:
        if 0 in tips:
            b = []
            c = []
            for i in range(how_many_p):
                if not tips[i]:
                    b.append(i)
                    c.append(f_tips[i])
                    f_tips[i] = 0
            a = collections.Counter(f_tips)
            if len(a) == 1:
                return True
            elif len(a) == 2:
                if max(c) <= max(f_tips):
                    return True
                else:
                    return False
            else:
                return False    
            
        else:
            a = collections.Counter(f_tips)
            if 0 in f_tips:
                if len(a) == 2:
                    return True
                else:
                    return False
            else:
                if len(a) == 1:
                    return True
                else:
                    return False
            
def make_pot():
    global pot,f_tips,if_actioned
    
    if_actioned = []
    for i in range(how_many_p):
        pot += f_tips[i]
        f_tips[i] = 0
        if_actioned.append(0)  
        
winner = 0
def if_gamefinish():
    global winner
    for i in range(how_many_p):
        if tips[i] == 0:
            tips.remove(0)
        else:
            winner = i
    if len(tips) == 1:
        return True
    else:
        return False
    
def if_dealfinish():
    global if_noplay
    for i in range(how_many_p):
        if tips[i] == 0:
            if_noplay[i] = 1
            
    z = collections.Counter(if_noplay)
    if z[0] == 1 and z[1] == how_many_p - 1:
        return True
    elif z[1] == how_many_p:
        return True
    else:
        return False

def dealer(a):
    if if_noplay[a] or not tips[a]:
        return dealer((a + 1)% how_many_p)
    else:
        #アクション受付
        if if_next():
            make_pot()
        else:
            dealer((a + 1)% how_many_p)    

def ini():
    global dec
    dec = []
    for i in range(4):
        for j in range(13):
            dec.append((Marks[i],Numbers[j]))
            
def draw():
    drawcard = dec.pop(random.randrange(len(dec)))
    return drawcard            


def if_flush(hand):
    if hand[0][0] ==  hand[1][0] ==  hand[2][0] ==  hand[3][0] == hand[4][0]:
        return True
    else:
        return False

def if_straight(hand):
    hand_num = []
    for i in range(5):
        hand_num.append(hand[i][1])
    hand_num.sort()  
    
    if hand_num[0]+4 == hand_num[1]+3 == hand_num[2]+2 == hand_num[3]+1 == hand_num[4]:
        return True
    elif hand_num[0] == 1 and hand_num[1] == 10 and hand_num[1]+3 == hand_num[2]+2 == hand_num[3]+1 == hand_num[4]:
        return True
    else:
        return False

def if_pairs(hand):
    c = 0 
    #c counts pairs.
    #If hand is one pair,if_pairs(hand) returns 1 (2C1)
    #If hand is two pairs,if_pairs(hand) returns 2 (2C1 * 2)
    #If hand is three of a kind,if_pairs(hand) returns 3 (3C2)
    #If hand is full house,if_pairs(hand) returns 4 (2C1 + 3C2)
    #If hand is four of a kind,if_pairs(hand) returns 6 (4C2)
    for i in range(4):
        for j in range(i+1,5):
            if hand[i][1] == hand[j][1]:
                c += 1
    return(c)
    
def strength(hand):
    f = if_flush(hand)
    s = if_straight(hand)
    p = if_pairs(hand)
    if f and s:
        return 8
    #8 means straight flush
    elif p == 6:
        return 7
    #7 means four of a kind
    elif p == 4:
        return 6
    #6 means full house
    elif f:
        return 5
    #5 means flush
    elif s:
        return 4
    #4 means straight
    elif p == 3:
        return 3
    #3 means three of a kind
    elif p == 2:
        return 2
    #2 means two pairs
    elif p == 1:
        return 1
    #1 means one pairs
    else:
        return 0
    #0 means high card
    
#In the next function,
#2 means player1 wins
#1 means draw
#0 means player2 wins

def det_winner(p1_hand,p2_hand):
    if strength(p1_hand) > strength(p2_hand):
        return 2
    elif strength(p1_hand) < strength(p2_hand):
        return 0
    else:
            p1_numbers = []
            p2_numbers = []
            for i in range(5):
                p1_numbers.append(p1_hand[i][1])
                p2_numbers.append(p2_hand[i][1])
            p1_numbers.sort()
            p2_numbers.sort()
            
            if strength(p1_hand) == 0 or strength(p1_hand) == 4 or strength(p1_hand) == 5 or strength(p1_hand) == 8:    
                if p1_numbers[0] == 1 and p2_numbers[0] != 1:
                    return 2
                elif p1_numbers[0] != 1 and p2_numbers[0] == 1: 
                    return 0
                else:
                    for i in range(1,6):
                        if p1_numbers[-i] > p2_numbers[-i] :
                            return 2
                        elif p1_numbers[-i] < p2_numbers[-i] :
                            return 0
                    if p1_numbers == p2_numbers:
                        return 1

            elif strength(p1_hand) == 1:
                    a1 = collections.Counter(p1_numbers)
                    a2 = collections.Counter(p2_numbers)
                    b1 = [i for i in a1 if a1[i] == 2]
                    b2 = [i for i in a2 if a2[i] == 2]
                    if b1[0] == 1 and b2[0] != 1:
                        return 2
                    elif b2[0] == 1 and b1[0] != 1:
                        return 0
                    else:
                        if b1[0] > b2[0]:
                                return 2
                        elif b1[0] < b2[0]:
                                return 0
                        else:
                            p1_numbers.remove(b1[0])
                            p2_numbers.remove(b2[0])
                            if p1_numbers[0] == 1 and p2_numbers[0] != 1:
                                    return 2
                            elif p1_numbers[0] != 1 and p2_numbers[0] == 1:
                                    return 0
                            else:        
                                for i in range(1,4):
                                    if p1_numbers[-i] > p2_numbers[-i] :
                                        return 2
                                    elif p1_numbers[-i] < p2_numbers[-i] :
                                        return 0
                                if p1_numbers == p2_numbers:
                                    return 1

            elif strength(p1_hand) == 2:
                    a1 = collections.Counter(p1_numbers)
                    a2 = collections.Counter(p2_numbers)
                    b1 = [i for i in a1 if a1[i] == 2]
                    b2 = [i for i in a2 if a2[i] == 2]
                    c1 = [i for i in a1 if a1[i] == 1]
                    c2 = [i for i in a2 if a2[i] == 1]
                    b1.sort()
                    b2.sort()
                    if b1[0] == 1 and b2[0] != 1:
                        return 2
                    elif b2[0] == 1 and b1[0] != 1:
                        return 0
                    else:
                        for i in range(1,3):
                                if b1[-i] > b2[-i] :
                                    return 2
                                elif b1[-i] < b2[-i] :
                                    return 0
                                    
                        if c1[0] == 1 and c2[0] != 1:
                                  return 2
                        elif c1[0] != 1 and c2[0] == 1:
                                  return 0
                        else:
                            if c1[0] > c2[0]:
                                return 2
                            elif c1[0] < c2[0]:
                                return 0
                            else:
                                return 1

            elif strength(p1_hand) == 3:
                    a1 = collections.Counter(p1_numbers)
                    a2 = collections.Counter(p2_numbers)
                    b1 = [i for i in a1 if a1[i] == 3]
                    b2 = [i for i in a2 if a2[i] == 3]
                    if b1[0] == 1 and b2[0] != 1:
                        return 2
                    elif b2[0] == 1 and b1[0] != 1:
                        return 0
                    else:
                        if b1[0] > b2[0]:
                                return 2
                        elif b1[0] < b2[0]:
                                return 0
                        else:
                            p1_numbers.remove(b1[0])
                            p2_numbers.remove(b2[0])
                            if p1_numbers[0] == 1 and p2_numbers[0] != 1:
                                    return 2
                            elif p1_numbers[0] != 1 and p2_numbers[0] == 1:
                                    return 0
                            else:
                                for i in range(1,3):
                                    if p1_numbers[-i] > p2_numbers[-i] :
                                        return 2
                                    elif p1_numbers[-i] < p2_numbers[-i] :
                                        return 0
                                if p1_numbers == p2_numbers:
                                        return 1
                                        

            elif strength(p1_hand) == 6:
                    a1 = collections.Counter(p1_numbers)
                    a2 = collections.Counter(p2_numbers)
                    b1 = [i for i in a1 if a1[i] == 3]
                    b2 = [i for i in a2 if a2[i] == 3]
                    c1 = [i for i in a1 if a1[i] == 2]
                    c2 = [i for i in a2 if a2[i] == 2]
                    if b1[0] == 1 and b2[0] != 1:
                        return 2
                    elif b1[0] != 1 and b2[0] == 1:
                        return 0
                    else:
                        if b1[0] > b2[0]:
                                return 2
                        elif b1[0] < b2[0]:
                                return 0
                        else:
                            if c1[0] == 1 and c2[0] != 1:
                                    return 2
                            elif c1[0] != 1 and c2[0] == 1:
                                    return 0
                            else:
                                if c1[0] > c2[0]:
                                    return 2
                                elif c1[0] < c2[0]:
                                    return 0
                                else:
                                    return 1

            elif strength(p1_hand) == 7:
                    a1 = collections.Counter(p1_numbers)
                    a2 = collections.Counter(p2_numbers)
                    b1 = [i for i in a1 if a1[i] == 4]
                    b2 = [i for i in a2 if a2[i] == 4]
                    c1 = [i for i in a1 if a1[i] == 1]
                    c2 = [i for i in a2 if a2[i] == 1]
                    if b1[0] == 1 and b2[0] != 1:
                        return 2
                    elif b2[0] == 1 and b1[0] != 1:
                        return 0
                    else:
                        if b1[0] > b2[0]:
                                return 2
                        elif b1[0] < b2[0]:
                                return 0
                        else:
                            if c1[0] == 1 and c2[0] != 1:
                                    return 2
                            elif c1[0] != 1 and c2[0] == 1:
                                    return 0
                            else:
                                if c1[0] > c2[0]:
                                    return 2
                                elif c1[0] < c2[0]:
                                    return 0
                                else:
                                    return 1
                      

                    
#Choose the most stronghest hand function
def cms(hand_list):
    if len(hand_list) == 1:
        return hand_list[0]
    else:
        hand_list2 = copy.deepcopy(hand_list)
        if det_winner(hand_list[0],hand_list[1]):
            hand_list2.remove(hand_list[1])
            return cms(hand_list2)
        else: 
            hand_list2.remove(hand_list[0])
            return cms(hand_list2)

#Choose the most stronghest hand from 7 cards function        
def det_hand(hands):
    hand_list = []
    for i in range(6):
        for j in range(i,6):
            copyhands = copy.deepcopy(hands)
            copyhands.pop(i)
            copyhands.pop(j)
            hand_list.append(copyhands)
    return cms(hand_list)                    
                    


# In[ ]:


tramp_dic = {}
Marks = ['♠','♥','♦','♣']
Numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13]
dec = []
for i in range(4):
        for j in range(13):
            dec.append((Marks[i],Numbers[j]))
dec2 = []
def ini():
    global dec
    dec = []
    for i in range(4):
        for j in range(13):
            dec.append((Marks[i],Numbers[j]))
def ini2():
    global dec2
    dec2 = []
    for i in range(4):
        for j in range(13):
            dec2.append((Marks[i],Numbers[j]))            
            
def draw():
    drawcard = dec.pop(random.randrange(len(dec)))
    return drawcard

powercard = [1,13,12,11]
hand = [draw(),draw()]

def count_win(hand,now_board):
    count = 0
    while steps <= 10:
        ini2()
        dec2.remove(hand[0])    
        dec2.remove(hand[1])
        enemy_hand = [draw(),draw()]
        if det_winner(det_hand(hand + now_board),det_hand(enemy_hand + now_board)) == 2:
            count += 1
        steps += 1
    return count    
        
    
    
    


def poker_AI(n,hand,now_board):
    global pot,f_tips,if_actioned
    if now_board == []:
        random_a = random.randrange(100)
        if hand[0][1] in powercard or hand[1][1] in powercard or hand[0][0] == hand[1][0] or hand[0][1] == hand[1][1]:
            if max(f_tips) == BB:
                    rai_se(n,3*BB)
            else:
                if 0 <= random_a < 20:
                    fold(n)
                elif 20 <= random_a < 80:
                    call(n)
                else:
                    rai_se(n,3*max(f_tips))
        else:
            if check(n):
                check(n)
            else:
                fold(n)
                
        
    elif len(now_board) == 3:
        random_a = random.randrange(100)
        if check(n):
            if count_win(hand,now_board) <= 5:
                if 0 <= random_a < 50:
                    bet(n,pot//3)
                
            
        
    #if len(now_board) == 4:
    #if len() == 5:    
        


# In[ ]:




