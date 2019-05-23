---
layout: default
title: Proposal
---

# PETA - We don’t kill animals; we hoard them

## Project Proposal

### Summary

The main idea of the project is based on collecting and gathering wild animals (sheep) from the world and luring them into a pen. The agent will have no previous knowledge of the benefits/consequences of his actions in the world. During a set duration of time (20 seconds), the agent must maximize the number of sheep they can reach and lure back into the pen.

The agent will have access to a detailed 2D grid of the world that specifies the location of each animal in it. The agent will choose an action to perform, either moving north, west, east, or south, based on what it’s learned so far about the world. It will receive positive reward for successfully reaching the sheep and negative reward for movement (steps taken). The negative reward increases as the distance of the agent from the sheep increases and decreases when the agent is closer to the sheep.

### AI/ML Algorithms

We expect to use reinforcement learning, via deep Q learning to train the agent, since there are a huge number of possible states. 

### Evaluation Plan

We will be measuring the success of our project based on the final number of points the agent receives in the 20 second time frame. Each animal that the agent is able to collect will be +10 points. The baseline for our project will be an agent that just stands in one place and doesn’t do anything, which will result in a final score of 0.

We know our agent is performing as expected if he chooses to approach the sheep and uses wheat to lure it. Sanity cases could include a world with just having the agent reach a static destination, reach a sheep, and then learn how to use wheat, etc.

In the first case, we expect the agent to go to the desired destination using purely RL and rewards. The second case, the agent should be able to get fairly close to a sheep.  The third would be to switch their item to wheat which can be used to lure sheep. We use deep Q reinforcement learning. We will check the agent’s actions throughout the program for maximizing its reward. Our moonshot case is an agent that can autonomously respond to different configurations of sheep.

### Appointment with Instructor

Thursday, April 25 3:00pm - 3:15pm.
