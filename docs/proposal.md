---
layout: default
title: Proposal
---

# PITA - Capture the Sheep!

## Project Proposal

### Summary

The main idea of the project is based on herding wild sheep that spawn in the world into a pre-built pen and protecting them from monsters (wolves) that are trying to eat them. The agent will have no previous knowledge of the benefits/consequences of his actions in the world. The spawning of animals or monsters be pre-set in the environment the agent is in. During a 20 second time period, the agent will need to take actions that will maximize his final reward.

The agent will have access to a detailed 2D grid of the world that specifies the location of each animal and monster. Based on his current state, the agent will produce an action. The actions may include: [Moving (Up Down Left Right), Using Wheat to Lure, Navigating Back to the Pen].

In the end, the agent should learn to move towards the sheep and activate his wheat in order to lure the sheep back to the pen. This will provide the agent with the highest final score.

### AI/ML Algorithms

We expect to use reinforcement learning, via deep Q learning to train the agent, since there are a huge number of possible states.

### Evaluation Plan

We will be measuring the success of our project based on the final number of points the agent receives in the 20 second time frame. Each animal that the agent is able to collect will be +500 points. The baseline for our project will be an agent that just stands in one place and doesn’t do anything, which will result in a final score of 0/

We know our agent is performing as expected if he chooses to move toward the sheep, activate his wehat, and return to the pen. In addition, we can check our agent to see if he ever tries to attack the wolf in order to protect the sheep in the world. Sanity cases could include a world with just sheep hoarding (no wolves), a world with 1 sheep and 1 wolf, a world with sheep and 1 wolf, etc.

In the first case, we expect the agent to go to the desired destination using purely RL and rewards. The second case, the agent should be able to get fairly close to a sheep. The third would be to switch their item to wheat which can be used to lure sheep. We use deep Q reinforcement learning. We will check the agent’s actions throughout the program for maximizing its reward. Our moonshot case is an agent that can autonomously respond to different configurations of sheep.

### Appointment with Instructor

Thursday, April 25 3:00pm - 3:15pm.
