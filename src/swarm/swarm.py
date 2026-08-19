"""Swarm orchestrator — coordinates multiple agents."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from swarm.agent import Agent, AgentResult
from swarm.provider import Provider


@dataclass
class SwarmResult:
    """Aggregated result from a multi-agent pipeline."""

    output: str
    agent_results: list[AgentResult] = field(default_factory=list)
    total_cost: float = 0.0
    total_latency: float = 0.0
    trace: list[dict] = field(default_factory=list)

    @property
    def cost_breakdown(self) -> dict[str, float]:
        return {r.agent_name: r.cost for r in self.agent_results}

    @property
    def latency_breakdown(self) -> dict[str, float]:
        return {r.agent_name: r.latency for r in self.agent_results}

    def export(self, path: str) -> None:
        """Export full trace to JSON."""
        import json
        with open(path, "w") as f:
            json.dump({
                "output": self.output,
                "total_cost": self.total_cost,
                "total_latency": self.total_latency,
                "agents": [
                    {"name": r.agent_name, "model": r.model, "cost": r.cost, "latency": r.latency}
                    for r in self.agent_results
                ],
                "trace": self.trace,
            }, f, indent=2)


class Swarm:
    """Multi-agent orchestrator."""

    def __init__(
        self,
        agents: list[Agent] | None = None,
        providers: list[Provider] | None = None,
    ):
        self.agents: dict[str, Agent] = {}
        self.providers: dict[str, Provider] = {}

        if agents:
            for agent in agents:
                self.agents[agent.name] = agent

        if providers:
            for provider in providers:
                self.providers[provider.name] = provider

    def run(
        self,
        task: str,
        pipeline: list[str] | None = None,
        parallel: list[str] | None = None,
        then: str | None = None,
        router: str | None = None,
        routes: dict[str, str] | None = None,
    ) -> SwarmResult:
        """Execute a multi-agent workflow."""
        from swarm.executor import execute_pipeline, execute_parallel

        if pipeline:
            return execute_pipeline(self, task, pipeline)
        elif parallel:
            return execute_parallel(self, task, parallel, then)
        else:
            # Single agent or router mode
            raise NotImplementedError("Router mode coming soon")

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def __repr__(self) -> str:
        return f"Swarm(agents={list(self.agents.keys())})"
