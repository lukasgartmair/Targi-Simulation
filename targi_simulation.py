# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 01:06:58 2016

@author: Lukas
"""
import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit
import scipy
import scipy.stats
import numpy.ma as ma
import random
import itertools
from bisect import bisect

#### spielfeld 

#####################################
# 1  2  3  4 5 
#16 17 18 19 6
#15 24 25 20 7
#14 23 22 21 8
#13 12 11 10 9
######################################

def curve_fiting(size, data):
    x = scipy.arange(len(data))
    #y = scipy.int_(scipy.round_(scipy.stats.vonmises.rvs(5,size=size)*47))
    h = pl.hist(data, bins=len(data)/4, color='w')    
    dist_names = ['gamma', 'beta', 'norm']
    for dist_name in dist_names:
        dist = getattr(scipy.stats, dist_name)
        param = dist.fit(data)
        pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
        pl.plot(pdf_fitted, label=dist_name)
        pl.xlim(0,47)
    pl.legend(loc='upper right')
    pl.show()
    
def get_cross_cards(positions):
    crosses =  {(2,16):17, (2,15):24, (2,14):23, (2,6):17, (2,7):24, (2,8):23,
                (3,16):18, (3,15):25, (3,14):22, (3,6):18, (3,7):25, (3,8):22,
                (4,16):19, (4,15):20, (4,14):21, (4,6):19, (4,7):20, (4,8):21,
                (6,4):19, (6,3):18, (6,2):17, (6,10):19, (6,11):18, (6,12):17,
                (7,4):20, (7,3):25, (7,2):24, (7,10):20, (7,11):25, (7,12):24,
                (8,4):21, (8,3):22, (8,2):23, (8,10):21, (8,11):22, (8,12):23,
                (10,8):21, (10,7):20, (10,6):19, (10,14):21, (10,15):20, (10,16):19,
                (11,8):22, (11,7):25, (11,6):18, (11,14):22, (11,15):25, (11,16):18,
                (12,8):23, (12,7):24, (12,6):17, (12,14):23, (12,15):24, (12,16):17,
                (14,2):23, (14,3):22, (14,4):21, (14,12):24, (14,11):22, (14,10):21,
                (15,2):24, (15,3):25, (15,4):20, (15,12):24, (15,11):25, (15,10):20,
                (16,2):17, (16,3):18, (16,4):19, (16,12):17, (16,11):18, (16,10):19}
                
    permutation = list(itertools.permutations(positions, 2))
    ps = []
    for p in permutation:
        if p in crosses.keys():
            ps.append(crosses[p])
    return (np.unique(np.array(ps))).tolist()
        
def get_counter_card(pos):
    counters =  {2:12, 3:11, 4:10, 6:16, 7:15, 8:14, 10:4, 11:3, 12:2, 14:8, 15:7, 16:6}
    return counters[pos]        
    
def set_targi_randomly(robber_pos):
    cross = False
    while cross==False:    
        positions = [2,3,4,6,7,8,10,11,12,14,15,16]    
        if robber_pos in positions:    
            positions.remove(robber_pos)
        opp_targi_pos = []
        own_targi_pos = []
        for i in range(3):
            opp_targi = random.choice(positions)
            positions.remove(opp_targi)
            counter_card = get_counter_card(opp_targi)
            if counter_card in positions:
                positions.remove(counter_card)        
            own_targi = random.choice(positions)
            positions.remove(own_targi)
            counter_card = get_counter_card(own_targi)
            if counter_card in positions:
                positions.remove(counter_card)           
            own_targi_pos.append(own_targi)
            opp_targi_pos.append(opp_targi)
        if get_cross_cards(own_targi_pos) != []:
            cross = True
    return own_targi_pos, opp_targi_pos

def set_robber(current_pos):
    current_pos += 1
    return current_pos
        
# outside fields        
        
def field1(salt,pepper,dates,gold,siegpunkte):
    #robbery4
    points_or_gold = np.random.randint(0,2)
    if points_or_gold == 0:
        gold -= 1
    else:
        siegpunkte -= 3
    return salt,pepper,dates,gold,siegpunkte

def field2(salt,pepper,dates,gold,siegpunkte):
    # noblemen
    pass
    return salt,pepper,dates,gold,siegpunkte
def field3(salt,pepper,dates,gold,siegpunkte):
    dates += 1
    return salt,pepper,dates,gold,siegpunkte
def field4(salt,pepper,dates,gold,siegpunkte):
    salt += 1
    return salt,pepper,dates,gold,siegpunkte
def field5(salt,pepper,dates,gold,siegpunkte):
    # robbery1       
    points_or_goods = np.random.randint(0,2)
    if points_or_goods == 0:
        robbery = np.random.randint(0,3)
        if robbery == 0:
            salt -= 1
        elif robbery == 1:
            pepper -= 1
        elif robbery == 2:
            dates -= 1
    else:
        siegpunkte -= 1
    return salt,pepper,dates,gold,siegpunkte

def field6(salt,pepper,dates,gold,siegpunkte):
    # händler
    if salt >= 3:
        gold += 1
        salt -= 3
    elif pepper >= 3:
        gold += 1
        pepper -= 3
    elif dates >= 3:
        gold += 1
        dates -= 3
#        # ware gegen ware evtl ergänzen
    return salt,pepper,dates,gold,siegpunkte
def field7(salt,pepper,dates,gold,siegpunkte):
    pepper += 1
    return salt,pepper,dates,gold,siegpunkte
def field8(salt,pepper,dates,gold,siegpunkte):
    dates += 1
    return salt,pepper,dates,gold,siegpunkte
def field9(salt,pepper,dates,gold,siegpunkte):
    # robbery2
    points_or_goods = np.random.randint(0,2)
    if points_or_goods == 0:
        for i in range(2):
            robbery = np.random.randint(0,3)
            if robbery == 0:
                salt -= 1
            elif robbery == 1:
                pepper -= 1
            elif robbery == 2:
                dates -= 1
    else:
        siegpunkte -= 1  
    return salt,pepper,dates,gold,siegpunkte

def field10(own_cross_positions, opp_cross_positions):
    # fata morgana
    rnd_cross_pos = np.random.randint(17,26)
    if (rnd_cross_pos not in own_cross_positions) and (rnd_cross_pos not in opp_cross_positions):
        own_cross_positions[0] = rnd_cross_pos
    return own_cross_positions

def field11(salt,pepper,dates,gold,siegpunkte):
    # silberschmied 
    good_trades = [4,2]
    for t in good_trades:
        if salt >= t:
            siegpunkte += t-1
            salt -= t
        elif pepper >= t:
            siegpunkte += t-1
            pepper -= t
        elif dates >= t:
            siegpunkte += t-1
            dates -= t
    gold_trades = [2,1]
    for gt in gold_trades:
        if gold >= gt:
            siegpunkte += gt*2
            gold -= gt
    return salt,pepper,dates,gold,siegpunkte
    
def field12(salt,pepper,dates,gold,siegpunkte):
    pepper += 1
    return salt,pepper,dates,gold,siegpunkte

def field13(salt,pepper,dates,gold,siegpunkte):
    # robbery3
    points_or_goods = np.random.randint(0,2)
    if points_or_goods == 0:
        for i in range(3):
            robbery = np.random.randint(0,3)
            if robbery == 0:
                salt -= 1
            elif robbery == 1:
                pepper -= 1
            elif robbery == 2:
                dates -= 1
    else:
        siegpunkte -= 2
    return salt,pepper,dates,gold,siegpunkte

    return salt,pepper,dates,gold,siegpunkte
def field14(salt,pepper,dates,gold,siegpunkte,goods_available):
    #karawane # goodcard will not be removed -> rules!
    rnd_pick = np.random.choice(goods_available)
    good = goods[rnd_pick]
    salt += good[2]
    pepper += good[3] 
    dates += good[4]
    gold += good[5]
    return salt,pepper,dates,gold,siegpunkte, goods_available
    
def field15(salt,pepper,dates,gold,siegpunkte, tribes_available):
    #tribes # tribe card will be removed
    rnd_pick = np.random.choice(tribes_available)
    tribe = tribes[rnd_pick]
    tribes_available.remove(rnd_pick)
    salt,pepper,dates,gold,siegpunkte = play_tribe_card(tribe,salt,pepper,dates,gold,siegpunkte)
    return salt,pepper,dates,gold,siegpunkte, tribes_available
    
def field16(salt,pepper,dates,gold,siegpunkte):
    salt += 1
    return salt,pepper,dates,gold,siegpunkte
    
def play_good_card(good,salt,pepper,dates,gold,siegpunkte):

    if np.sum(good) == 3:
        indices = np.where(good!=0)[0].tolist()
        rnd_pick1 = random.choice(indices)
        indices.remove(rnd_pick1)
        rnd_pick2 = random.choice(indices)
        
        good[rnd_pick1] = 0
        good[rnd_pick2] = 0
        
    salt += good[2]
    pepper += good[3] 
    dates += good[4]
    gold += good[5]
    siegpunkte += good[1]
    
    return salt,pepper,dates,gold,siegpunkte
    
    
def play_tribe_card(tribe,salt,pepper,dates,gold,siegpunkte):
    liquid = False
    s = salt
    p = pepper
    d = dates
    g = gold
    liquid = check_liquidity(tribe,s,p,d,g)
    #print(liquid)
    if liquid == True:

        salt -= tribe[2]
        pepper -= tribe[3] 
        dates -= tribe[4]
        gold -= tribe[5]
        siegpunkte += tribe[1]
        
    return salt,pepper,dates,gold,siegpunkte
    
def check_liquidity(tribe,salt,pepper,dates,gold):
    liquid = False
    salt -= tribe[2]
    pepper -= tribe[3] 
    dates -= tribe[4]
    gold -= tribe[5]
    if np.all(np.array([salt,pepper,dates,gold])>=0):
        liquid = True
    return liquid

#############################
##########   MAIN  ##########
#############################

salt_summary = []
pepper_summary = []
dates_summary = []
gold_summary = []
siegpunkte_summary = []

runs = 500
for run in range(runs):

    #0, siegpunkte, costs (salt,pepper,dates,gold)
    
    goods = np.array([[0,0,1,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,2,0,0],[0,0,2,0,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,1,1,1,0],
                      [0,0,0,0,2,0],[0,0,0,0,0,1],[0,1,0,0,0,0],[0,0,1,1,1,0],[0,0,1,0,1,0],[0,0,0,0,0,1],[0,0,0,0,1,0],[0,0,1,1,1,0],[0,0,1,1,0,0],[0,0,0,1,1,0]])
    goods_available = np.arange(0,19).tolist()
    
    # targia = 0, kamelreiter = 1, zelt = 2, brunnen = 3, oase = 4
    # its type,number in the set, siegpunkte, costs (salt,pepper,dates,gold), 
    tribes = np.array([
                        [0,3,2,2,1,0],[0,3,0,1,1,1],
                        [0,2,1,2,1,0],[0,2,0,0,2,1],[0,2,1,2,1,0],
                        [0,1,0,2,0,1], [0,1,0,1,0,1], [0,1,2,0,1,0], [0,1,0,0,1,1],
    
                        [1,3,2,2,1,0],[1,3,1,0,1,1],
                        [1,2,2,1,1,0],[1,2,2,1,2,0],[1,2,0,2,0,1],
                        [1,1,0,0,0,1], [1,1,1,0,0,1], [1,1,1,0,2,0], [1,1,0,0,0,1],
                        
                        [2,3,2,1,2,0],[2,3,0,1,1,1],
                        [2,2,0,1,0,1],[2,2,0,0,1,1],[2,2,1,2,1,0],
                        [2,1,0,2,1,0], [2,1,0,0,1,1], [2,1,0,0,1,1], [2,1,0,1,1,0],      
    
                        [3,3,1,2,2,0],[3,3,1,0,1,1],
                        [3,2,2,1,1,0],[3,2,1,1,2,0],[3,2,1,1,0,1],
                        [3,1,2,0,1,0], [3,1,1,0,0,1], [3,1,0,0,1,1], [3,1,0,0,1,1],    
    
                        [4,3,1,2,2,0],[4,3,1,0,1,1],
                        [4,2,1,1,0,1],[4,2,0,1,1,1],[4,2,0,1,0,1],
                        [4,1,2,1,0,0], [4,0,1,0,0,1], [4,1,2,1,0,0], [4,1,1,1,0,1]   
                        
                        ])
                        
    tribes_available = np.arange(0,44).tolist()
    
    #targias = tribes[0:9]
    #kamelreiter = tribes[9:18]
    #zelt = tribes[18:27]
    #brunnen = tribes[27:36]
    #oase =  tribes[36:45]     
    
    # start ressources
    salt = 2
    pepper = 2
    dates = 2
    gold = 1
    siegpunkte = 4
    
    field_funcs = {1:field1, 2:field2, 3:field3, 4:field4, 5:field5, 6:field6, 7:field7, 8:field8, 9:field9,
                   10:field10, 11:field11,  12:field12, 13:field13, 14:field14, 15:field15, 16:field16}
    
    number_of_plays = 15
    robber_position = 0
    
    # initialize pointers for inside cards
    # goods = 0
    # tribes = 1
    # set up the card configuration
    rnd_setup_goods = random.sample(range(19),5)
    rnd_setup_tribes = random.sample(range(44),4)
    # must be removed here else it can be selected below randomly
    for i in rnd_setup_goods:
        goods_available.remove(i)
    for j in rnd_setup_tribes:
        tribes_available.remove(j)
        
    card_setup = [rnd_setup_goods[0],rnd_setup_tribes[0], rnd_setup_goods[1],
                  rnd_setup_tribes[1],
                  rnd_setup_goods[2],rnd_setup_tribes[2],rnd_setup_goods[3],
                  rnd_setup_tribes[3], rnd_setup_goods[4]]        
    
    f17 = 0
    f18 = 1
    f19 = 0
    f20 = 1
    f21 = 0
    f22 = 1
    f23 = 0
    f24 = 1
    f25 = 0
    
    for turn in range(number_of_plays):
        
        # set up the play
        robber_position = set_robber(robber_position)
        own_targi_positions, opp_targi_positions = set_targi_randomly(robber_position)
        #print(own_targi_positions)
        own_cross_positions = get_cross_cards(own_targi_positions)
        opp_cross_positions = get_cross_cards(opp_targi_positions)
        #print(own_cross_positions)
        fields = own_targi_positions + own_cross_positions # concat lists with +
        
        # set tribes and goods
    
        # get goods and siegpunkte    
        for field  in fields:
            if field < 10:
                func = field_funcs[field]
                salt,pepper,dates,gold,siegpunkte = func(salt,pepper,dates,gold,siegpunkte)
            elif field == 10:
                func = field_funcs[field]
                own_cross_positions = func(own_cross_positions,opp_cross_positions)
            elif field == 14:
                salt,pepper,dates,gold,siegpunkte,goods_available = field14(salt,pepper,dates,gold,siegpunkte,goods_available)
            elif field == 15:
                salt,pepper,dates,gold,siegpunkte,tribes_available = field15(salt,pepper,dates,gold,siegpunkte, tribes_available)
            if field >= 17:
                curr_inside_field = field-17
                # get current variable state
                ftmp = "pointer"
                exec(ftmp + " = 'f%s'" % (field))
                tribe_or_goods = eval(pointer)
                # pick randomly one out of the list available
                if tribe_or_goods == 0:
                    good_rnd_index = card_setup[curr_inside_field] 
                    good_rnd = goods[good_rnd_index]
                    salt,pepper,dates,gold,siegpunkte = play_good_card(good_rnd,salt,pepper,dates,gold,siegpunkte)
                    if good_rnd_index in goods_available:
                        goods_available.remove(good_rnd_index)
                    # now place the other species
                    new_rnd = random.choice(tribes_available)
                    card_setup[curr_inside_field] = new_rnd
                    
                elif tribe_or_goods == 1:
                    tribe_rnd_index = card_setup[curr_inside_field] 
                    tribe_rnd = tribes[tribe_rnd_index]
                    salt,pepper,dates,gold,siegpunkte = play_tribe_card(tribe_rnd,salt,pepper,dates,gold,siegpunkte)      
                    if tribe_rnd_index in tribes_available:
                        tribes_available.remove(tribe_rnd_index)
                    # now place the other species
                    new_rnd = random.choice(goods_available)
                    card_setup[curr_inside_field] = new_rnd
   
                #switch the pointers tribe becomes good and vise versa
                if field == 17:
                    f17 ^= 1
                elif field == 18:
                    f18 ^= 1
                elif field == 19:
                    f19 ^= 1
                elif field == 20:
                    f20 ^= 1
                elif field == 21:
                    f21 ^= 1
                elif field == 22:
                    f22 ^= 1
                elif field == 23:
                    f23 ^= 1
                elif field == 24:
                    f24 ^= 1        
                elif field == 25:
                    f25 ^= 1
    
    salt_summary.append(salt)
    pepper_summary.append(pepper)
    dates_summary.append(dates)
    gold_summary.append(gold)
    siegpunkte_summary.append(siegpunkte)  
   
pl.hist(siegpunkte_summary)
#curve_fiting(runs,siegpunkte_summary)
print(max(siegpunkte_summary))
