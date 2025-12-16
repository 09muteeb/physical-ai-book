---
sidebar_position: 4
---

# Module 1 Quiz: ROS 2 and the Robotic Nervous System

Test your understanding of the concepts covered in Module 1.

## Question 1
What is the primary role of ROS 2 in a robotic system?

A) To act as the robot's artificial intelligence
B) To serve as the communication infrastructure connecting AI to robot bodies
C) To provide power to robot actuators
D) To replace traditional programming languages

## Question 2
Which communication pattern is best suited for continuous sensor data streams?

A) Service request-response
B) Publisher-subscriber
C) Direct function calls
D) File-based communication

## Question 3
What does the "rclpy" library provide?

A) A way to connect Python AI agents to ROS 2
B) A simulation environment for robots
C) A hardware interface for sensors
D) A visualization tool for robot data

## Question 4
In the sensor-to-AI-to-actuator data flow, what happens first?

A) AI makes a decision
B) Actuators perform an action
C) Sensors publish raw data
D) Commands are sent to the robot

## Question 5
What is URDF used for in robotics?

A) To program robot movements
B) To define robot physical structure and properties
C) To communicate between nodes
D) To store sensor data

---

## Answer Key

1. B - ROS 2 serves as the communication infrastructure connecting AI to robot bodies, acting as the "nervous system" of the robot.

2. B - The publisher-subscriber pattern is ideal for continuous data streams like sensor data, where multiple subscribers might need the information.

3. A - The rclpy library is the Python client library for ROS 2, allowing Python AI agents to interface with ROS 2.

4. C - In the sensor-to-AI-to-actuator flow, sensors publish raw data first, which is then processed by AI systems, leading to commands sent to actuators.

5. B - URDF (Unified Robot Description Format) is an XML format for representing a robot model, describing its physical structure, links, joints, and properties.