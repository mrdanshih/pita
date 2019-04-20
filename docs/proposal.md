---
layout: default
title:  Proposal
---

# PETA - We don’t kill animals; we hoard them

##  Project Proposal
### Summary
The main idea of the project is based on collecting and gathering wild animals (rabbits) that spawn in the world and protecting them from monsters (wolves) that are trying to eat them. The agent will have no previous knowledge of the benefits/consequences of his actions in the world. The spawning of animals or monsters will be based on speech input in real-time. A user will be able to spawn various types of animals and monsters using pre-defined key phrases. During a 60 second time period, the agent will need to take actions that will maximize his final reward.

The agent will have access to a detailed 2D grid of the world that specifies the location of each animal and monster. Based on his curre
nt state, the agent will produce an action (STAY, MOVE, KILL, COLLECT). Another input to the project will be the user’s audio, which will be used to spawn animals or monsters in real time. 

### AI/ML Algorithms
We expect to use reinforcement learning to train the agent, Dijkstra’s algorithm for navigation, and NLP to process the voice input. 

### Evaluation Plan
We will be measuring the success of our project based on the final number of points the agent receives in the 60 second time frame. Each animal that the agent is able to collect will be +10 points. The baseline for our project will be an agent that just stands in one place and doesn’t do anything, which will result in a final score of 0. For the voice input aspect of the project, we will measure the percentage of speech input recognized and classified correctly. 

We know our agent is performing as expected if he chooses to collect the animals and kill the monsters. Sanity cases could include a world with just 1 animal and a world with just 1 monster. In the first case, we expect the agent to collect the animal to maximize his score. In the second case, we expect the agent to kill the monster. We have broken down our project into three main algorithms: voice input processing, reinforcement learning, and navigation. To verify the voice input part of the project, we will conduct tests to see if the generated animal/monster is correct. To verify navigation, we will test our implementation of Dijkstra’s algorithm to see if the agent is taking the shortest path. To verify our reinforcement learning, we will check the agent’s actions throughout the program. Our moonshot case is an agent that can autonomously respond to new user-spawned animals or monsters and successfully defend the collected animals from the enemy monsters.
