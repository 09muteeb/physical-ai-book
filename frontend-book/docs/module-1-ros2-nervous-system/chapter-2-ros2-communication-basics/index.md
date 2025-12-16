---
sidebar_position: 2
---

# Chapter 2: ROS 2 Communication Basics

## Nodes, Topics, and Services

In ROS 2, communication between different parts of a robot system happens through three primary mechanisms: nodes, topics, and services. Understanding these concepts is fundamental to creating effective robotic systems.

### Nodes

Nodes are the fundamental building blocks of a ROS 2 system. Each node is a process that performs a specific computation. Nodes can be written in different programming languages (C++, Python, etc.) and can run on different machines, yet they all participate in the same peer-to-peer network.

A node might represent:
- A sensor driver (e.g., camera, LiDAR)
- A control algorithm
- A perception module
- A user interface
- A data logger

### Topics

Topics are named buses over which nodes exchange messages. The communication pattern is publish-subscribe, where one or more nodes publish messages to a topic, and one or more nodes subscribe to that topic to receive messages.

This pattern is ideal for:
- Continuous data streams (sensor data, robot state)
- Broadcasting information to multiple consumers
- Decoupling publishers from subscribers

### Services

Services provide a request-response communication pattern. A client node sends a request to a service, and a server node processes the request and returns a response. This is synchronous communication, meaning the client waits for the response.

Services are appropriate for:
- One-off requests (e.g., "calibrate sensor")
- Operations that return a result after processing
- Actions that should only be performed by one server

## Publisher-Subscriber vs Request-Response

The publisher-subscriber pattern and request-response pattern serve different purposes in robotic systems:

### Publisher-Subscriber Pattern
- **Asynchronous**: Publishers don't wait for responses
- **Many-to-many**: Multiple publishers can publish to the same topic, and multiple subscribers can listen to the same topic
- **Continuous**: Data flows continuously from publishers to subscribers
- **Use case**: Sensor data, robot state, sensor streams

### Request-Response Pattern (Services)
- **Synchronous**: Client waits for a response from the server
- **One-to-one**: One client talks to one server at a time
- **Discrete**: Each request generates one response
- **Use case**: Actions, calculations, configuration changes

## Sensor-to-AI-to-Actuator Data Flow

A typical robotic system follows a pattern where data flows from sensors through AI processing to actuator commands:

1. **Sensors** publish raw data (images, laser scans, IMU readings) to topics
2. **Perception nodes** subscribe to sensor topics, process the data, and publish processed information (detected objects, maps, etc.)
3. **AI decision-making nodes** subscribe to perception data, make decisions, and publish commands
4. **Controller nodes** subscribe to commands and send low-level control signals to actuators
5. **Actuators** perform physical actions and may publish feedback about their state

This flow ensures that information moves efficiently through the system while maintaining modularity and separation of concerns.

## Practical Example: Simple Publisher and Subscriber

Here's a simple example of how a publisher and subscriber work in ROS 2 using Python:

```python
# Publisher example
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This demonstrates the basic structure of a ROS 2 publisher node that sends messages to a topic.

Here's a corresponding subscriber that receives these messages:

```python
# Subscriber example
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Complete working examples of these nodes can be found in the examples directory.

In the next chapter, we'll explore how to bridge AI agents with ROS 2 and create complete AI-to-control pipelines.

## Summary

In this chapter, we've covered:

- The three primary communication mechanisms in ROS 2: nodes, topics, and services
- The differences between publisher-subscriber and request-response communication patterns
- The typical sensor-to-AI-to-actuator data flow in robotic systems
- Practical examples of publisher and subscriber nodes using Python and rclpy

These communication patterns form the backbone of how AI systems interact with robot hardware, enabling the flow of information necessary for intelligent robot behavior.