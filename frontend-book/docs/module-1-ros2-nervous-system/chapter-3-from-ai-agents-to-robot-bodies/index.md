---
sidebar_position: 3
---

# Chapter 3: From AI Agents to Robot Bodies

## Bridging Python AI Agents using rclpy

One of the most powerful aspects of ROS 2 is its ability to bridge AI agents with physical robot systems. Using rclpy, the Python client library for ROS 2, we can connect sophisticated AI algorithms to robot hardware seamlessly.

Python is particularly well-suited for this integration because:
- It has rich ecosystems for AI and machine learning (TensorFlow, PyTorch, scikit-learn)
- It's widely used in research and prototyping
- The rclpy library provides a clean interface to ROS 2 functionality

### Basic AI-to-ROS 2 Bridge Pattern

The fundamental pattern for connecting AI agents to ROS 2 involves:

1. **Perception**: Subscribe to sensor data topics from the robot
2. **AI Processing**: Apply AI algorithms to interpret sensor data
3. **Action Selection**: Decide on appropriate actions based on AI outputs
4. **Actuation**: Publish commands to robot control topics

Here's a template for this pattern:

```python
import rclpy
from rclpy.node import Node
import numpy as np
# Import your AI libraries here (TensorFlow, PyTorch, etc.)

class AIBridgeNode(Node):
    def __init__(self):
        super().__init__('ai_bridge_node')

        # Subscribe to sensor data
        self.subscription = self.create_subscription(
            # Appropriate message type for your sensor
            YourSensorMessageType,
            'sensor_topic_name',
            self.sensor_callback,
            10
        )

        # Publisher for robot commands
        self.publisher = self.create_publisher(
            # Appropriate message type for robot commands
            RobotCommandType,
            'robot_command_topic',
            10
        )

        # Initialize your AI agent here
        self.ai_agent = self.initialize_ai_agent()

    def initialize_ai_agent(self):
        # Load or create your AI agent
        # This could be a neural network, decision tree, etc.
        pass

    def sensor_callback(self, msg):
        # Convert ROS message to format for AI agent
        sensor_data = self.process_sensor_message(msg)

        # Run AI inference
        action = self.ai_agent.predict(sensor_data)

        # Convert AI output to ROS command
        command_msg = self.create_command_message(action)

        # Publish command to robot
        self.publisher.publish(command_msg)

        self.get_logger().info(f'Published action: {action}')

def main(args=None):
    rclpy.init(args=args)
    ai_bridge_node = AIBridgeNode()

    try:
        rclpy.spin(ai_bridge_node)
    except KeyboardInterrupt:
        pass
    finally:
        ai_bridge_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## High-Level AI-to-Control Pipeline

A complete AI-to-control pipeline typically includes multiple layers of processing:

### 1. Perception Layer
- Processes raw sensor data (cameras, LiDAR, IMU, etc.)
- Extracts meaningful features for higher-level reasoning
- May include computer vision, SLAM, object detection

### 2. Cognition/Decision Layer
- High-level reasoning and planning
- Goal selection and path planning
- May use reinforcement learning, symbolic AI, or other approaches

### 3. Motion Planning Layer
- Translates high-level goals into specific movements
- Considers robot kinematics and dynamics
- Generates trajectories and waypoints

### 4. Control Layer
- Low-level control of actuators
- Ensures precise execution of motions
- Handles real-time constraints

## Practical Example: Simple AI Agent with Robot Control

Let's look at a more concrete example of an AI agent that controls a simple robot:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

class SimpleNavigationAgent(Node):
    def __init__(self):
        super().__init__('simple_navigation_agent')

        # Subscribe to laser scan data for obstacle detection
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        # Publisher for velocity commands
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        # Simple timer for decision making
        self.timer = self.create_timer(0.1, self.decision_callback)

        # State variables
        self.scan_data = None
        self.obstacle_detected = False

    def scan_callback(self, msg):
        # Store the latest scan data
        self.scan_data = msg.ranges

        # Simple obstacle detection: check if anything is closer than 1 meter
        if self.scan_data:
            min_distance = min([d for d in self.scan_data if d != float('inf')], default=float('inf'))
            self.obstacle_detected = min_distance < 1.0

    def decision_callback(self):
        if self.scan_data is None:
            return

        cmd_msg = Twist()

        if self.obstacle_detected:
            # Turn to avoid obstacle
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.5  # Turn right
        else:
            # Move forward
            cmd_msg.linear.x = 0.5
            cmd_msg.angular.z = 0.0

        self.cmd_vel_publisher.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    agent = SimpleNavigationAgent()

    try:
        rclpy.spin(agent)
    except KeyboardInterrupt:
        pass
    finally:
        agent.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This example demonstrates a simple AI agent that navigates by avoiding obstacles based on laser scan data.

## Introduction to URDF for Humanoid Robots

URDF (Unified Robot Description Format) is an XML format for representing a robot model. It describes the robot's physical structure, including:

- Links (rigid parts of the robot)
- Joints (connections between links)
- Inertial properties
- Visual and collision properties
- Materials

Here's a simple example of a URDF for a basic humanoid robot:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.2"/>
  </joint>

  <!-- Left arm -->
  <link name="left_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.3"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="left_arm_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_arm"/>
    <origin xyz="0.15 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>
</robot>
```

URDF files are essential for:
- Robot simulation in Gazebo
- Robot visualization in RViz
- Kinematic calculations
- Collision detection

In the next section, we'll explore how to integrate AI agents with simulated robots using URDF models.

## Summary

In this chapter, we've covered:

- How to bridge Python AI agents with ROS 2 using the rclpy library
- The typical AI-to-control pipeline with perception, cognition, motion planning, and control layers
- A practical example of an AI-based robot controller
- Introduction to URDF (Unified Robot Description Format) for humanoid robots
- A complete example of a simple humanoid robot URDF model

These concepts tie together the communication patterns from Chapter 2 with practical AI integration, providing the foundation for building complete AI-robot systems. The combination of ROS 2's communication infrastructure, Python's AI capabilities, and URDF's robot description enables sophisticated Physical AI applications.