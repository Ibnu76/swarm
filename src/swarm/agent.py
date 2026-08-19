"""Agent definition and execution logic."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

from swarm.provider import Provider


@dataclass
class Agent:
    """A single LLM-powered agent with optional tools."""

    name: str
    model: str
    instructions: str = ""
    tools: list[Callable] = field(default_factory=list)
    max_iterations: int = 10
    temperature: float = 0.7
    provider: Provider | None = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Agent must have a name")

    def run(self, task: str, context: dict[str, Any] | None = None) -> "AgentResult":
        """Execute the agent on a single task."""
        from swarm.executor import execute_agent
        return execute_agent(self, task, context)

    def __repr__(self) -> str:
        return f"Agent(name={self.name!r}, model={self.model!r}, tools={len(self.tools)})"


@dataclass
class AgentResult:
    """Result from a single agent execution."""

    output: str
    agent_name: str
    model: str
    cost: float = 0.0
    latency: float = 0.0
    iterations: int = 0
    tool_calls: list[dict] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
