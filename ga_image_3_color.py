# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 23:58:35 2020

@author: Logan Rowe

Trains an agent to mimic a target image using the genetic algorithm

To keep things simple the image is limited to to three colors.
"""

import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import random

class Agent(object):
    def __init__(self, n):
        self.arr = [random.randint(0, 2) for _ in range(n)]
        self.fitness = -1
        
    def __str__(self):
        return '\nFitness: '+str(self.fitness)
    
def ga(generations, target, population, save_file, color_scheme, survival_fraction = 0.2, mutation_rate = 0.03):
    '''
    The genetic algorithm (ga) run function:
        creates a population of random agents
        checks each agent in the population ot see how well it fits the desired goal
        Picks the best agents to be parents and breed
        Creates new agents using cross over
        Adds in a few (3%) mutations to add variance that may not be large enough in the initial population
    '''
    global R, C
    agents = [Agent(len(target)) for _ in range(population)]
    MUTATION_RATE = mutation_rate
    
    for generation in range(1, generations + 1):
        print('Generation: ', str(generation), 'Fit:', str(agents[0].fitness))
        fitness(agents, target)
        agents = selection(agents, 0.2)
        mutation_rate = mutation_rate * (1 - agents[0].fitness)
        
        save_agent(agents[0].arr, save_file, color_scheme, generation)

        crossover(agents, survival_fraction, population)
        mutation(agents, mutation_rate, survival_fraction)
        
        if any(agent.fitness == 1.0 for agent in agents):
            print('Threshold met!')
            break
        
def save_agent(arr, save_file, color_scheme, generation):
    #save_arr = [[(0,)*3 for _ in range(C)] for _ in range(R)]
    save_arr = [[[0 for _ in range(3)] for _ in range(C)] for _ in range(R)]
    for i in range(R):
        for j in range(C):
            save_arr[i][j] = color_scheme[arr[i*C + j]]
    save_arr = np.array(save_arr)
    plt.imsave(save_file+'/'+str(generation).zfill(4)+'.png', save_arr)

def fitness(agents, target):
    for agent in agents:
        agent.fitness = sum(agent.arr[i] == target[i] for i in range(len(target))) / len(target)

def selection(agents, survival_fraction):
    agents.sort(key = lambda a: a.fitness, reverse = True)
    return agents[:int(survival_fraction * len(agents))]

def crossover(agents, survival_fraction, population):
    j = int(population * survival_fraction)
    n = len(agents[0].arr)
    while len(agents) < population:        
        #There is potential for picking the same parent but thats ok for now
        parent1 = random.choice(agents[:j])
        parent2 = random.choice(agents[:j])
        
        #Create two random children
        child1 = Agent(n)
        child2 = Agent(n)
        
        # Randomly cross over genes
        for i in range(n):
            if random.random() >= 0.5:
                child1.arr[i], child2.arr[i] = parent1.arr[i], parent2.arr[i]
            else:
                child1.arr[i], child2.arr[i] = parent2.arr[i], parent1.arr[i]
                
        agents.append(child1)
        agents.append(child2)

def mutation(agents, mutation_rate, survival_fraction):
    '''For each pixel in the agent there is a chance of it mutating (0.03)
    If the pixel mutates, swap the pixel with a random different value [0, 1, 2].'''
    j = int(len(agents) * survival_fraction)
    for agent in agents[j:]:
        for i in range(len(agent.arr)):
            if random.random() <= mutation_rate:
                agent.arr[i] = random.choice([0, 1, 2])

def black_and_white(img):
    '''Converts image to black and white:
        
        returns arr where arr[arr<np.mean(arr)]=0 and arr[arr>=np.mean(arr)]=1
    '''
    arr=img[:,:,0]+img[:,:,1]+img[:,:,2]
    arr=arr/3
    
    threshold=np.mean(arr)
    
    arr[arr<threshold]=int(0)
    arr[arr>=threshold]=int(1)
    
    return arr.astype(int)

def guess_color(r, g, b):
    """Categorize pixel based on RGB values 2: white, 1: yellow, 0: blue"""
    maxi = max(r, g, b)
    ave = (r + g + b) / 3
    return 2 if ave >= 80 else 0 if maxi == b else 1

def get_target(image):
    return [[guess_color(*image[i][j][:3]) for j in range(C)] for i in range(R)]

if __name__=='__main__':
    global R, C
    
    color_scheme = {1: [float(255/255), float(208/255), float(64/255)], # yellow
                    0: [float(55/255), float(112/255), float(161/255)], # blue
                    2: [float(255/255), float(255/255), float(255/255)]}
    
    name = r'images\python-logo-50-50.png'
    img = np.array(Image.open(name))
    R, C, D = img.shape
    target = get_target(img)
    target = sum(target, [])
    
    savefile='./'+name.split('.')[0]
    if os.path.exists(savefile)!=True:
        os.makedirs(savefile)
        
    settings = {"generations": 300,
                "target": target,
                "population": 1000,
                "save_file": "./python_logo",
                "color_scheme": color_scheme,
                "survival_fraction": 0.2,
                "mutation_rate": 1
                }
    
    ga(**settings)