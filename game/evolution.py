import simulation
from characters import *
import NeuralNet as nn
import copy
import multiprocessing
from multiprocessing import Pool
from functools import partial
import json

if __name__ == "__main__":
    scoresOverTime = []
    generation = 1
    population = [AiPlayer(brain=nn.Brain([0,0,0], [0,0,0])) for _ in range(0,50)]
    mode = "m"
    while mode == "m" or mode == "s":
        try:
            results = []
            print(f"Generation: {generation}")
            if mode == "m":
                pool = Pool(4)
                results = pool.map(simulation.run, population)
                pool.close()
                pool.join()
            else:
                for player in population:
                    results.append(simulation.run(player))
            results = sorted(results, key=lambda k: k['score'], reverse=True)
            best = results[0]
            maxScore = best['score']
            print(f"Best Score: {best['score']}")
            newPopulation = [copy.deepcopy(best['player']) for player in results]
            for player in newPopulation:
                player.mutate(random.randrange(0,3))
            newPopulation[0] = best['player']
            population = newPopulation
            generation +=1
            if maxScore <= 2000:
                mode = "m"
            elif maxScore >= 2100:
                mode = "s"
            elif maxScore >= 5000:
                mode = input("Mode (s/m/q): ")
            scoresOverTime.append(maxScore)
            with open("socresOverTime.json", 'w') as f:
                json.dump(scoresOverTime, f)
        except KeyboardInterrupt as e:
            break