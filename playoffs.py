import numpy as np
import pandas as pd
from pandas import DataFrame
import tetris

number_of_rounds = 5
df = DataFrame(pd.read_csv("output.txt"))
df.columns = ["score", "w0", "w1", "w2", "w3"]
data_df = df.nlargest(16, "score")[["w0", "w1", "w2", "w3"]]
data = data_df.values.tolist()

#returns the weights of the genetic strain that won the most number of rounds
def fight(wt_a, wt_b):

    wins_a = 0
    wins_b = 0

    for _ in range(number_of_rounds):
        try:
            app = tetris.TetrisApp(wt_a, True)
            app.run()
            score_a = app.score
        except ValueError: 
            print(app.board)
            print(app.block)

        try:
            app = tetris.TetrisApp(wt_b, True)
            app.run()
            score_b = app.score
        except ValueError: 
            print(app.board)
            print(app.block)        

        if score_a > score_b:
            wins_a += 1
            print("Player A wins with score of {}".format(score_a))
        else:
            wins_b += 1
            print("Player B wins with score of {}".format(score_b))


    if wins_a > wins_b:
        winner = "A"
    else:
        winner = "B"

    print("Player {} advances".format(winner))
    print("************************")
    return wt_a if winner == "A" else wt_b

#takes a list and recursively halve it using the function passed in
#every two items are compared using the function and the winner is kept
#will eventually return a list of 1 item
def halve(li, func):
    if len(li) == 1:
        return li

    return halve([a if func(a, b) else b for a, b in zip(li[::2], li[1::2])], func)

matches = []

#1-16
matches.append(data[0])
matches.append(data[15])

#8-9
matches.append(data[7])
matches.append(data[8])

#4-13
matches.append(data[3])
matches.append(data[12])

#5-12
matches.append(data[4])
matches.append(data[11])

#2-15
matches.append(data[1])
matches.append(data[14])

#7-10
matches.append(data[6])
matches.append(data[9])

#3-14
matches.append(data[2])
matches.append(data[13])

#6-11
matches.append(data[5])
matches.append(data[10])

print(halve(matches, fight))