#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame,sys, random , copy , collections
from pygame.locals import *

a = 0
player1_card1 = 0
player1_card2 = 0
player2_card1 = 0
player2_card2 = 0
player3_card1 = 0
player3_card2 = 0
player4_card1 = 0
player4_card2 = 0
player5_card1 = 0
player5_card2 = 0
player6_card1 = 0
player6_card2 = 0
board_card1 = 0
board_card2 = 0
board_card3 = 0
board_card4 = 0
board_card5 = 0

p1card1 = 0
p1card2 = 0
p2card1 = 0
p2card2 = 0
bcard1 = 0
bcard2 = 0
bcard3 = 0
bcard4 = 0
bcard5 = 0


tramp_dic = {}
Marks = ['♠','♥','♦','♣']
Numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13]
dec = []
def ini():
    global dec
    dec = []
    for i in range(4):
        for j in range(13):
            dec.append((Marks[i],Numbers[j]))
            

ini()
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

def det_winner2(p1_hand,p2_hand,board):
    p1_hands = p1_hand + board 
    p2_hands = p2_hand + board
    p1_cards = det_hand(p1_hands)
    p2_cards = det_hand(p2_hands)
    if det_winner(p1_cards,p2_cards) == 2:
        messagebox.showinfo("result","PLAYER1 WINS POT!")
    if det_winner(p1_cards,p2_cards) == 1:
        messagebox.showinfo("result","DRAW")
    if det_winner(p1_cards,p2_cards) == 0:
        messagebox.showinfo("result","PLAYER2 WINS POT!")
        
def draw():
    drawcard = dec.pop(random.randrange(len(dec)))
    return drawcard

def card_update(card): 
    card = pygame.image.load(tramp_dic[draw()])
    card = pygame.transform.scale(card,(60,90))
    
def check_key(key):
    global player1_card1,player1_card2,player2_card1,player2_card2
    global board_card1,board_card2,board_card3,board_card4,board_card5
    global p1card1,p1card2,p2card1,p2card2,bcard1,bcard2,bcard3,bcard4,bcard5
    global a
    
    if key == K_LEFT:
        ini()
        
        p1card1 = draw()
        p1card2 = draw()
        p2card1 = draw()
        p2card2 = draw() 
        
        player1_card1 = pygame.image.load(tramp_dic[p1card1])
        player1_card1 = pygame.transform.scale(player1_card1,(80,120))
        player1_card2 = pygame.image.load(tramp_dic[p1card2])
        player1_card2 = pygame.transform.scale(player1_card2,(80,120))
        player2_card1 = pygame.image.load(tramp_dic[p2card1])
        player2_card1 = pygame.transform.scale(player2_card1,(80,120))
        player2_card2 = pygame.image.load(tramp_dic[p2card2])
        player2_card2 = pygame.transform.scale(player2_card2,(80,120))

        board_card1 = pygame.image.load("image52.png")
        board_card1 = pygame.transform.scale(board_card1,(80,120))
        board_card2 = pygame.image.load("image52.png")
        board_card2 = pygame.transform.scale(board_card2,(80,120))                                         
        board_card3 = pygame.image.load("image52.png")
        board_card3 = pygame.transform.scale(board_card3,(80,120))
        board_card4 = pygame.image.load("image52.png")
        board_card4 = pygame.transform.scale(board_card4,(80,120))                                         
        board_card5 = pygame.image.load("image52.png")
        board_card5 = pygame.transform.scale(board_card5,(80,120))  
        a = 0
        
    elif key == K_RIGHT:
        if a:
            pass
        else:
            bcard1 = draw()
            bcard2 = draw()
            bcard3 = draw()
            bcard4 = draw()
            bcard5 = draw()
            board_card1 = pygame.image.load(tramp_dic[bcard1])
            board_card1 = pygame.transform.scale(board_card1,(80,120))
            board_card2 = pygame.image.load(tramp_dic[bcard2])
            board_card2 = pygame.transform.scale(board_card2,(80,120))
            board_card3 = pygame.image.load(tramp_dic[bcard3])
            board_card3 = pygame.transform.scale(board_card3,(80,120))
            board_card4 = pygame.image.load(tramp_dic[bcard4])
            board_card4 = pygame.transform.scale(board_card4,(80,120))
            board_card5 = pygame.image.load(tramp_dic[bcard5])
            board_card5 = pygame.transform.scale(board_card5,(80,120))
            
            p1_hand = [p1card1,p1card2]
            p2_hand = [p2card1,p2card2]
            board = [bcard1,bcard2,bcard3,bcard4,bcard5]
            det_winner2(p1_hand,p2_hand,board)
            a = 1
        
        
    elif key == K_UP:
        pass
    elif key == K_DOWN:
        pass
    elif key == K_ESCAPE:
        pygame.quit()
    
from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw()
    
            
            
                                             

for i in range(52):
    tramp_dic[dec[i]] = "image" + str(i) + ".png"
    
black = (0, 0, 0)
red = (255, 0, 0)
white = (255,255,255)
brown = (115, 66, 41)
orange = (233,168, 38)
green = (0,100,0)

def main():
    global player1_card1,player1_card2,player2_card1,player2_card2
    global board_card1,board_card2,board_card3,board_card4,board_card5
    # ゲームの初期化処理
    pygame.init()
    pygame.display.set_caption("Poker")
    screen = pygame.display.set_mode((1000,800))
    
    FPS = 60
    clock = pygame.time.Clock()
    
    p1card1 = draw()
    p1card2 = draw()
    p2card1 = draw()
    p2card2 = draw()
    
    player1_card1 = pygame.image.load(tramp_dic[p1card1])
    player1_card1 = pygame.transform.scale(player1_card1,(80,120))
    player1_card2 = pygame.image.load(tramp_dic[p1card2])
    player1_card2 = pygame.transform.scale(player1_card2,(80,120))
    player2_card1 = pygame.image.load(tramp_dic[p2card1])
    player2_card1 = pygame.transform.scale(player2_card1,(80,120))
    player2_card2 = pygame.image.load(tramp_dic[p2card2])
    player2_card2 = pygame.transform.scale(player2_card2,(80,120))
                                             
    board_card1 = pygame.image.load("image52.png")
    board_card1 = pygame.transform.scale(board_card1,(80,120))
    board_card2 = pygame.image.load("image52.png")
    board_card2 = pygame.transform.scale(board_card2,(80,120))                                         
    board_card3 = pygame.image.load("image52.png")
    board_card3 = pygame.transform.scale(board_card3,(80,120))
    board_card4 = pygame.image.load("image52.png")
    board_card4 = pygame.transform.scale(board_card4,(80,120))                                         
    board_card5 = pygame.image.load("image52.png")
    board_card5 = pygame.transform.scale(board_card5,(80,120))                                         
                                             
                                             
                                             
    button = pygame.Rect(80, 700, 70, 50)  
    button2 = pygame.Rect(160, 700, 70, 50)
    button3 = pygame.Rect(240, 700, 70, 50)  
    button4 = pygame.Rect(320, 700, 70, 50)
    font = pygame.font.SysFont(None, 25)
                                             
    text1 = font.render("FOLD", True, (0,0,0))
    text2 = font.render("CALL", True, (0,0,0))
    text3 = font.render("BET", True, (0,0,0))
    text4 = font.render("RAISE", True, (0,0,0))
    # ゲームのメインループ --- (*3)
    while True:
        screen.fill(green)
        
        screen.blit(player1_card1,(300,570))
        screen.blit(player1_card2,(360,570))
        screen.blit(player2_card1,(640,140))
        screen.blit(player2_card2,(580,140))
        screen.blit(board_card1,(330,355))                                     
        screen.blit(board_card2,(400,355))  
        screen.blit(board_card3,(470,355))                                       
        screen.blit(board_card4,(540,355))                                       
        screen.blit(board_card5,(610,355))                                       
                                             
        pygame.draw.rect(screen, orange , button)
        pygame.draw.rect(screen, orange , button2)
        pygame.draw.rect(screen, orange , button3)
        pygame.draw.rect(screen, orange , button4)


        screen.blit(text1, (92.5, 717.5))
        screen.blit(text2, (173.75, 717.5))
        screen.blit(text3, (257.5, 717.5))
        screen.blit(text4, (327.5,717.5))
        
        pygame.display.update()
        clock.tick(FPS)
        # イベントを処理する --- (*5)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: 
                    check_key(event.key)     
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    print("red button was pressed")
                if button2.collidepoint(event.pos):
                    print("green button was pressed") 
if __name__ == '__main__':
    main()


# In[ ]:




