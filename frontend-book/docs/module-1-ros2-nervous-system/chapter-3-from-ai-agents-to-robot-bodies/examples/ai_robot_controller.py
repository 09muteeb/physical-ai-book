#!/usr/bin/env python3
"""
AI Robot Controller Example

This example demonstrates how to bridge an AI agent with a robot using ROS 2.
The AI agent makes decisions based on sensor input and sends commands to the robot.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np
import math


class AIBasedRobotController(Node):
    """
    An AI-based controller that navigates a robot using sensor data.
    This demonstrates the bridge between AI decision-making and robot control.
    """

    def __init__(self):
        super().__init__('ai_robot_controller')

        # Subscribe to laser scan data for navigation
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

        # Timer for AI decision making
        self.timer = self.create_timer(0.2, self.ai_decision_callback)

        # State variables
        self.scan_data = None
        self.safety_threshold = 0.8  # meters
        self.current_state = "EXPLORING"  # EXPLORING, AVOIDING, STOPPED

        self.get_logger().info("AI Robot Controller initialized")

    def scan_callback(self, msg):
        """Process incoming laser scan data"""
        # Store scan data for AI processing
        self.scan_data = np.array(msg.ranges)

        # Filter out invalid ranges (inf or very large values)
        valid_ranges = [r for r in self.scan_data if not math.isinf(r) and r > 0]
        if valid_ranges:
            self.closest_obstacle = min(valid_ranges) if valid_ranges else float('inf')
        else:
            self.closest_obstacle = float('inf')

    def ai_decision_callback(self):
        """Main AI decision-making function"""
        if self.scan_data is None:
            return

        # Simple AI decision logic
        cmd_msg = Twist()

        # Safety check
        if self.closest_obstacle < 0.3:  # Emergency stop
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.0
            self.current_state = "STOPPED"
        elif self.closest_obstacle < self.safety_threshold:  # Avoid obstacle
            cmd_msg.linear.x = 0.2  # Slow forward
            cmd_msg.angular.z = 0.8  # Turn away from obstacle
            self.current_state = "AVOIDING"
        else:  # Explore
            cmd_msg.linear.x = 0.5  # Forward
            cmd_msg.angular.z = 0.0  # Straight
            self.current_state = "EXPLORING"

        # Publish command
        self.cmd_vel_publisher.publish(cmd_msg)

        # Log state
        self.get_logger().info(
            f"State: {self.current_state}, "
            f"Closest obstacle: {self.closest_obstacle:.2f}m, "
            f"Command: lin.x={cmd_msg.linear.x}, ang.z={cmd_msg.angular.z}"
        )


def main(args=None):
    """Main function to run the AI robot controller"""
    rclpy.init(args=args)
    controller = AIBasedRobotController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info("Shutting down AI Robot Controller...")
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()