---
layout: default
title: Proposal
---

# PETA - We don’t kill animals; we hoard them

## Project Proposal

### Summary

The main idea of the project is based on herding wild sheep that spawn in the world into a pre-built pen and protecting them from monsters (wolves) that are trying to eat them. The agent will have no previous knowledge of the benefits/consequences of his actions in the world. The spawning of animals or monsters will be based on speech input in real-time. A user will be able to spawn various types of animals and monsters using pre-defined key phrases. During a 60 second time period, the agent will need to take actions that will maximize his final reward.

The agent will have access to a detailed 2D grid of the world that specifies the location of each animal and monster. Based on his current state, the agent will produce an action. The actions may include: [Moving to a target sheep, lead sheep back to pen, kill a target wolf]. Another input to the project will be the user’s audio, which will be used to spawn animals or monsters in real time.

### AI/ML Algorithms

We expect to use reinforcement learning, via deep Q learning to train the agent, since there are a huge number of possible states. Dijkstra's algorithm will be used for agent navigation actions. For the stretch goal of the project, NLP would be used to process the voice input.

### Evaluation Plan

We will be measuring the success of our project based on the final number of points the agent receives in the 60 second time frame. Each animal that the agent is able to collect will be +10 points. The baseline for our project will be an agent that just stands in one place and doesn’t do anything, which will result in a final score of 0. For the voice input aspect of the project, we will measure the percentage of speech input recognized and classified correctly.

We know our agent is performing as expected if he chooses to collect the sheep and kill the wolves. Sanity cases could include  a world with just sheep hoarding (no wolves), a world with 1 sheep and 1 wolf, a world with sheep and 1 wolf, etc.

In the first case, we expect the agent to collect the animals to maximize his score. In the second case, we expect the agent to choose between hoarding the 1 sheep or killing the wolf to prevent the loss of the sheep. We have broken down our project into three main algorithms: voice input processing, reinforcement learning, and navigation. To verify the voice input part of the project, we will conduct tests to see if the generated animal/monster is correct. To verify navigation, we will test our implementation of Dijkstra’s algorithm to see if the agent is taking the shortest path. To verify our reinforcement learning, we will check the agent’s actions throughout the program. Our moonshot case is an agent that can autonomously respond to new user-spawned animals or monsters and successfully defend the collected animals from the enemy monsters.

### Appointment with Instructor

Thursday, April 25 3:00pm - 3:15pm.
