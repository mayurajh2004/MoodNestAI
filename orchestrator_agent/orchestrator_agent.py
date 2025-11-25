"""
MoodNestAI Orchestrator
High-level agent that coordinates:
- EmotionAgent
- PlannerAgent
- CopingAgent
- Memory
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """Coordinates sub-agents (emotion, planner, coping) and memory."""

    def __init__(self, emotion_agent=None, planner_agent=None, coping_agent=None, memory_bank=None):
        """
        Initialize OrchestratorAgent with optional injected dependencies.
        
        Args:
            emotion_agent: EmotionAgent instance (lazy-loaded if None)
            planner_agent: PlannerAgent instance (lazy-loaded if None)
            coping_agent: CopingAgent instance (lazy-loaded if None)
            memory_bank: MemoryBank instance (lazy-loaded if None)
        """
        self.emotion = emotion_agent
        self.planner = planner_agent
        self.coping = coping_agent
        self.memory = memory_bank





    def _load_agents(self):
        """Lazy-load all agents."""
        if self.emotion is None:
            try:
                from agents.analyzer_agent import AnalyzerAgent
                self.emotion = AnalyzerAgent()
                logger.info("AnalyzerAgent (emotion) loaded")
            except ImportError as e:
                logger.error("Failed to import AnalyzerAgent: %s", e)
                raise

        if self.planner is None:
            try:
                from agents.recommender_agent import RecommenderAgent
                self.planner = RecommenderAgent()
                logger.info("RecommenderAgent (planner) loaded")
            except ImportError as e:
                logger.error("Failed to import RecommenderAgent: %s", e)
                raise

        if self.coping is None:
            try:
                from agents.recommender_agent import RecommenderAgent
                self.coping = RecommenderAgent()
                logger.info("RecommenderAgent (coping) loaded")
            except ImportError as e:
                logger.error("Failed to import RecommenderAgent: %s", e)
                raise

        if self.memory is None:
            try:
                from memory.memory import MemoryBank
                self.memory = MemoryBank()
                logger.info("MemoryBank loaded")
            except ImportError as e:
                logger.error("Failed to import MemoryBank: %s", e)
                raise
    def handle(self, user_input: str) -> str:
        """
        Main workflow:
        1. Analyze mood
        2. Save to memory
        3. Generate coping support
        4. Generate a daily plan (optional)

        Args:
            user_input: User's input text describing their mood/state

        Returns:
            Formatted response with mood, coping support, and suggested plan
        """
        if not user_input or not isinstance(user_input, str):
            logger.warning("Invalid user input: %s", user_input)
            return "Please provide valid input."

        try:
            # Load agents on first use
            self._load_agents()

            # Analyze mood
            mood = self.emotion.analyze(user_input)
            logger.info("Mood analyzed: %s", mood)

            # Log to memory
            self.memory.log_mood(mood)
            logger.debug("Mood logged to memory")

            # Get coping support
            coping = self.coping.get_support(mood)
            logger.debug("Coping support retrieved")

            # Generate plan
            plan = self.planner.generate_plan(mood)
            logger.debug("Plan generated")

            # Format response
            response = (
                f"**Mood detected:** {mood}\n\n"
                f"**Coping support:**\n{coping}\n\n"
                f"**Suggested plan:**\n{plan}"
            )
            return response

        except Exception as e:
            logger.exception("Error in orchestrator handle: %s", e)
            return f"An error occurred: {str(e)}"
