# Physical AI Book - Frontend

This is the frontend component of the Physical AI Book, built with Docusaurus. It contains educational content about connecting AI logic to robot bodies using ROS 2.

## About

The Physical AI Book is designed for AI students and developers new to robotics. It provides a comprehensive guide to understanding how AI systems can interact with physical robots, with a focus on the Robot Operating System 2 (ROS 2) as the "nervous system" that connects AI logic to robot bodies.

## Modules

### Module 1: The Robotic Nervous System (ROS 2)
- Chapter 1: ROS 2 and Physical AI
- Chapter 2: ROS 2 Communication Basics
- Chapter 3: From AI Agents to Robot Bodies

### Module 2: Digital Twins, Simulation, and Human-Robot Interaction
- Chapter 1: Digital Twins in Robotics
- Chapter 2: Gazebo Physics Simulation
- Chapter 3: Unity-Based Human-Robot Interaction

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- Chapter 1: NVIDIA Isaac Sim Overview
- Chapter 2: Isaac ROS for Perception
- Chapter 3: Path Planning with Nav2

### Module 4: Vision-Language-Action (VLA) for LLM-Driven Robotics
- Chapter 1: Voice-to-Action with OpenAI Whisper
- Chapter 2: Cognitive Planning with LLMs
- Chapter 3: Capstone Project – The Autonomous Humanoid

## Local Development

1. Make sure all dependencies are installed:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

To build the website for production:

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. See `.github/workflows/deploy.yml` for the deployment configuration.

## Contributing

To add new content:
1. Create new markdown files in the `docs/` directory following the existing structure
2. Update `sidebars.js` to include new pages in the navigation
3. Test locally before committing