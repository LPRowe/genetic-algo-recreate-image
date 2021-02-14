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
    



def ga():
    '''
    The genetic algorithm (ga) run function:
        
        creates a population of random agents
        
        checks each agent in the population ot see how well it fits the desired goal
        
        Picks the best agents to be parents and breed
        
        Creates new agents using cross over
        
        Adds in a few (3%) mutations to add variance that may not be large enough in the initial population
    '''
    global generations, in_img_size, in_img, population
    
    #each agent is a random string
    agents = init_agents(population, in_img_size)
    
    for generation in range(generations):
        print('Generation: '+str(generation)+' Fit: '+str(agents[0].fitness))
        
        
        agents=fitness(agents)
        agents=selection(agents)
        
        plt.imsave(savefile+'/'+str(generation)+'.png',~np.reshape(agents[0].arr,(in_x,in_y)),cmap='Blues')

        agents=crossover(agents)
        agents=mutation(agents,mutation_rate)
        
        if any(agent.fitness==1.0 for agent in agents):
            print('Threshold met!')
            break

def init_agents(population,img_size):
    '''generates a number of agents equal to the population'''
    return [Agent(in_img_size) for _ in range(population)]

def fitness(agents):
    for agent in agents:
        score=0
        for idx in range(in_img_size):
            if agent.arr[idx]==in_img[idx]:
                score+=1
        agent.fitness=score/len(agent.arr)
            
    return agents

def selection(agents):
    agents=sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    
    #Show the best fit agent of the current population
    #plt.imshow(np.reshape(agents[0].arr,(50,50)))
    
    #Take the top 20% of agents (4 agents) to move on
    agents=agents[:int(0.2*len(agents))]
    
    return agents

def crossover(agents):
    offspring=[]
    
    for i in range(int(0.5*(population-len(agents)))):
        
        #There is potential for picking the same parent but thats ok for now
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        
        #Create two random children
        child1=Agent(in_img_size)
        child2=Agent(in_img_size)
        
        #Choose a random location to make the crossover
        split=random.randint(0,in_img_size)
        
        #Construct children according to their parents dna
        child1.arr=np.array(list(parent1.arr[0:split])+list(parent2.arr[split:in_img_size]))
        child2.arr=np.array(list(parent2.arr[0:split])+list(parent1.arr[split:in_img_size]))

        offspring.append(child1)
        offspring.append(child2)
        
    agents.extend(offspring)
    
    return agents

def mutation(agents,mutation_rate):
    '''For each letter in the string there is a chance of it mutating (0.03)
    If the letter mutates, swap that index with a random letter'''
    
    for agent in agents:
        for idx in range(len(agent.arr)):
            if random.uniform(0.0, 1.0) <= mutation_rate: 
                agent.arr=np.array(list(agent.arr[:idx])+[random.choice(values)]+list(agent.arr[idx+1:in_img_size]))
    
    return agents

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

def 

if __name__=='__main__':
    population=500
    generations=300
    mutation_rate=0.03
    
    
    
    in_img_name=r'images\python-logo-50-50.png'
    in_img=np.array(Image.open(in_img_name))
    in_img=black_and_white(in_img)
    in_x,in_y=in_img.shape
    in_img=np.reshape(in_img,(1,-1))[0]
    
    in_img_size=len(in_img)
    
    savefile='./'+in_img_name.split('.')[0]
    if os.path.exists(savefile)!=True:
        os.makedirs(savefile)
    
    ga()