import logging
import random
from os import path
import csv
import pandas as pd

def pvt(the_var):
    print(the_var)
    print(type(the_var))

def roll_2_die():
    return (random.randint(1,6), random.randint(1,6))

# craps_roll_log = r'.\craps_roll_log.txt'
craps_roll_log = r'.\craps_roll_log.csv'

# basic logging using csv module
if not path.exists(craps_roll_log):
    with open(craps_roll_log, 'a') as file_object:
        file_object.write('log_datetime,game_key,game_roll_count,roll_resulting_tuple,roll_resulting_tuple_sum,win_game_or_lose_game_or_point_game,win_roll_or_lose_roll_or_roll_again\n')
# if we hit the else statement, it is because the log file exists which means there will the column to identify state
else:
    df = pd.read_csv(craps_roll_log)
    # largest_csv_game_key = list(df['game_key'].unique())[-1] + 1
    current_game_key = int(list(df['game_key'].unique())[-1] + 1)
    
logging.basicConfig(filename=craps_roll_log, level=logging.INFO, format='%(asctime)s.%(msecs)03d,%(message)s',datefmt="%Y-%m-%d %H:%M:%S")

dice = [set() for each_index_in_list in range(14)]

# Here in the nested for loop below we are filling into the 13 empty sets, all the possible combinaitons of die rolls
for roll_a in range(1,7):
    for roll_b in range(1,7):
        roll_tuple = (roll_a, roll_b)
        roll_sum = sum(roll_tuple)
        dice[roll_sum].add(roll_tuple)

# setting the goal or rules for the game into 2 tiers - on the first roll cna fall into [win or lose] or [point]
lose = set(dice[2] | dice[3] | dice[12])
win = set(dice[7] | dice[11])
set_point = set(dice[4] | dice[5] | dice[6] | dice[8] | dice[9] | dice[10])

# we're initiating defualt values for variables
i_still_have_the_possibility_of_playing = True  #telling us when the game ends
point_set_sum = 0 #tells us the winning sum in case we dont win or lose on first roll and enter point_world
counter = 0 # keeping track of which roll we are in during the game
print(f'Start of the counter =  {counter}')

# begin playing the game
while i_still_have_the_possibility_of_playing:
    counter += 1
    print(f'How many rolls = counter variable = {counter}')
    a_roll = (random.randint(1,6), random.randint(1,6))
    a_roll_for_log = ' + '.join([str(x) for x in a_roll])
    sum_of_roll = sum(a_roll)
    # Tells us we are in not in point world if point_set_sum == 0, thus we are in the initial round
    if point_set_sum == 0:
        if a_roll in lose:
            print(f'LOSE {a_roll}')
            win_game_or_lose_game_or_point_game = 'lose_game'
            winning_losing_roll_again = 'losing_roll'
            i_still_have_the_possibility_of_playing = False
        elif a_roll in win:
            print(f'WIN {a_roll}')
            win_game_or_lose_game_or_point_game = 'win_game'
            winning_losing_roll_again = 'winning_roll'
            i_still_have_the_possibility_of_playing = False
        else:
            print(f'POINT = {a_roll}, Need to roll a sum equal to {sum(a_roll)}')
            win_game_or_lose_game_or_point_game = 'point_game'
            winning_losing_roll_again = 'roll_again'
            point_set = a_roll
            point_set_sum = sum(a_roll)
            point = dice[point_set_sum]
    else: #With this else statement we hop into points world
        print(f'WE ARE IN POINT WORLD, POINT WORLD ROLL = {a_roll}')
        if dice[sum(a_roll)] == dice[7]:
            print(f'LOSE {a_roll}')
            winning_losing_roll_again = 'losing_roll'
            i_still_have_the_possibility_of_playing = False
        elif dice[sum(a_roll)] == dice[point_set_sum]:
            print(f'WIN {a_roll}')
            winning_losing_roll_again = 'winning_roll'
            i_still_have_the_possibility_of_playing = False
        else:
            print(f'NEED ANOTHER ROLL! This roll was {a_roll} with sum equal to {sum(a_roll)} not 7 or {point_set_sum}')
            winning_losing_roll_again = 'roll_again'
    # message = f'{counter};{a_roll};{sum(a_roll)};{win_game_or_lose_game_or_point_game};{winning_losing_roll_again}'
    message = f'{current_game_key},{counter},{a_roll_for_log},{sum_of_roll},{win_game_or_lose_game_or_point_game},{winning_losing_roll_again}'

    logging.info(message)

