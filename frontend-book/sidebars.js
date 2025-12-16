// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Physical AI Introduction',
      items: [
        'intro',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2-nervous-system/index',
        {
          type: 'category',
          label: 'Chapter 1: ROS 2 and Physical AI',
          items: ['module-1-ros2-nervous-system/chapter-1-ros2-and-physical-ai/index'],
        },
        {
          type: 'category',
          label: 'Chapter 2: ROS 2 Communication Basics',
          items: ['module-1-ros2-nervous-system/chapter-2-ros2-communication-basics/index'],
        },
        {
          type: 'category',
          label: 'Chapter 3: From AI Agents to Robot Bodies',
          items: ['module-1-ros2-nervous-system/chapter-3-from-ai-agents-to-robot-bodies/index'],
        },
        'module-1-ros2-nervous-system/quiz',
        'module-1-ros2-nervous-system/exercises',
        'module-1-ros2-nervous-system/quickstart-validation',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twins, Simulation, and Human-Robot Interaction',
      items: [
        'module-2-digital-twins-simulation-hri/index',
        {
          type: 'category',
          label: 'Chapter 1: Digital Twins in Robotics',
          items: ['module-2-digital-twins-simulation-hri/chapter-1-digital-twins/index'],
        },
        {
          type: 'category',
          label: 'Chapter 2: Gazebo Physics Simulation',
          items: ['module-2-digital-twins-simulation-hri/chapter-2-gazebo-physics-simulation/index'],
        },
        {
          type: 'category',
          label: 'Chapter 3: Unity-Based Human-Robot Interaction',
          items: ['module-2-digital-twins-simulation-hri/chapter-3-unity-human-robot-interaction/index'],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3-isaac-ai-brain/index',
        {
          type: 'category',
          label: 'Chapter 1: NVIDIA Isaac Sim Overview',
          items: ['module-3-isaac-ai-brain/chapter-1-isaac-sim-overview/index'],
        },
        {
          type: 'category',
          label: 'Chapter 2: Isaac ROS for Perception',
          items: ['module-3-isaac-ai-brain/chapter-2-isaac-ros-perception/index'],
        },
        {
          type: 'category',
          label: 'Chapter 3: Path Planning with Nav2',
          items: ['module-3-isaac-ai-brain/chapter-3-nav2-path-planning/index'],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) for LLM-Driven Robotics',
      items: [
        'module-4-vla-robotics/index',
        {
          type: 'category',
          label: 'Chapter 1: Voice-to-Action with OpenAI Whisper',
          items: ['module-4-vla-robotics/chapter-1-voice-to-action/index'],
        },
        {
          type: 'category',
          label: 'Chapter 2: Cognitive Planning with LLMs',
          items: ['module-4-vla-robotics/chapter-2-cognitive-planning/index'],
        },
        {
          type: 'category',
          label: 'Chapter 3: Capstone Project – The Autonomous Humanoid',
          items: ['module-4-vla-robotics/chapter-3-autonomous-humanoid/index'],
        },
      ],
    },
    // Add more modules here as they are created
  ],
};

export default sidebars;