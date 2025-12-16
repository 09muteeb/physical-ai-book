---
sidebar_position: 5
---

# Hands-on Exercises: Module 1

These exercises will help you practice the concepts learned in Module 1. They are organized by difficulty level: beginner, intermediate, and advanced.

## Beginner Exercises

### Exercise 1: Publisher-Subscriber Pair
Create a simple publisher that sends "Hello, ROS 2!" messages every second and a subscriber that prints these messages to the console.

**Steps:**
1. Create a new ROS 2 package
2. Implement a publisher node that sends String messages to a topic called "hello_topic"
3. Implement a subscriber node that listens to "hello_topic" and logs the received messages
4. Run both nodes and verify they communicate properly

### Exercise 2: Understanding Node Communication
Use ROS 2 tools to visualize the communication between nodes:
1. Run `ros2 topic list` to see available topics
2. Run `ros2 node list` to see active nodes
3. Use `ros2 topic echo <topic_name>` to monitor a topic
4. Use `ros2 node info <node_name>` to see node details

## Intermediate Exercises

### Exercise 3: AI Agent Bridge
Create a simple AI agent that:
1. Subscribes to a sensor topic (e.g., simulated laser scan data)
2. Makes a simple decision based on the sensor input (e.g., if obstacle distance < 1.0m, turn right)
3. Publishes velocity commands to control a robot

### Exercise 4: Service Implementation
Create a service that:
1. Accepts a request to "navigate to goal"
2. Processes the request (simple simulation)
3. Returns a response with the result

## Advanced Exercises

### Exercise 5: Complete Navigation System
Build a complete system that:
1. Uses multiple sensors (laser, camera simulation)
2. Implements a simple path planning algorithm
3. Controls a simulated robot to navigate to a goal while avoiding obstacles
4. Uses URDF for the robot model

### Exercise 6: Integration Challenge
Combine all concepts learned in this module:
1. Create a system that uses AI for decision making
2. Implements proper ROS 2 communication patterns
3. Uses URDF for robot representation
4. Includes both publisher-subscriber and service communication

## Exercise Solutions

Solutions to these exercises can be found in the `examples/solutions/` directory of this repository.

## Tips for Success

1. Start with the beginner exercises and work your way up
2. Use the ROS 2 documentation when you encounter issues
3. Experiment with different parameters to understand how systems behave
4. Don't hesitate to modify examples to understand how they work
5. Join the ROS 2 community forums for additional help and resources