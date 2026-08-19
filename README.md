# swarm

Lightweight multi-agent orchestration framework. Spawn, coordinate, and chain LLM agents with minimal boilerplate.

## Why

Most agent frameworks are bloated or locked to one provider. `swarm` gives you:

- **Provider-agnostic** — OpenAI, Anthropic, local (Ollama/vLLM), any OpenAI-compatible endpoint
- **Composable agents** — define skills, chain them, let them delegate
- **Minimal overhead** — no langchain, no 200 dependencies, just clean Python
- **Observable** — built-in trace logging, cost tracking, latency metrics

## Install

```bash
pip install swarm-ai
```

## Quick Start

```python
from swarm import Agent, Swarm

researcher = Agent(
    name="researcher",
    model="gpt-4o",
    instructions="You research topics thoroughly and return structured findings.",
)

writer = Agent(
    name="writer", 
    model="claude-sonnet-4-20250514",
    instructions="You write concise technical summaries from research data.",
)

swarm = Swarm(agents=[researcher, writer])

result = swarm.run(
    task="Research AMD MI300X GPU performance vs NVIDIA H100, then write a comparison.",
    pipeline=["researcher", "writer"],
)
print(result.output)
print(f"Total cost: ${result.total_cost:.4f} | Latency: {result.total_latency:.1f}s")
```

## Architecture

```
┌─────────────────────────────────────────┐
│              Swarm Orchestrator          │
├─────────┬─────────┬─────────┬───────────┤
│ Agent A │ Agent B │ Agent C │  Agent N  │
├─────────┴─────────┴─────────┴───────────┤
│           Provider Router                │
├──────┬──────┬──────┬──────┬─────────────┤
│OpenAI│Claude│Gemini│Ollama│ vLLM/Custom │
└──────┴──────┴──────┴──────┴─────────────┘
```

## Features

### Agent Definition

```python
from swarm import Agent, tool

@tool
def search_web(query: str) -> str:
    """Search the web and return results."""
    # your implementation
    ...

agent = Agent(
    name="web-researcher",
    model="gpt-4o",
    instructions="Research using web search.",
    tools=[search_web],
    max_iterations=5,
)
```

### Pipelines

```python
# Sequential pipeline
swarm.run(task="...", pipeline=["research", "analyze", "write"])

# Parallel fan-out
swarm.run(task="...", parallel=["researcher_a", "researcher_b"], then="synthesizer")

# Conditional routing
swarm.run(task="...", router="classifier", routes={
    "technical": "engineer",
    "creative": "writer",
    "data": "analyst",
})
```

### Provider Config

```python
from swarm import Provider

providers = [
    Provider("openai", api_key="sk-..."),
    Provider("anthropic", api_key="sk-ant-..."),
    Provider("ollama", base_url="http://localhost:11434"),
    Provider("custom", base_url="http://my-vllm:8000/v1", api_key="token"),
]

swarm = Swarm(providers=providers)
```

### Observability

```python
# Built-in cost + latency tracking
result = swarm.run(task="...")
print(result.trace)  # full execution trace
print(result.cost_breakdown)  # per-agent costs
print(result.latency_breakdown)  # per-agent latency

# Export to JSON for dashboards
result.export("run_trace.json")
```

## Configuration

```yaml
# swarm.yaml
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    default_model: gpt-4o
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}  
    default_model: claude-sonnet-4-20250514

agents:
  researcher:
    model: gpt-4o
    instructions: Research topics thoroughly.
    tools: [search_web, read_url]
    
  writer:
    model: claude-sonnet-4-20250514
    instructions: Write concise summaries.

defaults:
  max_retries: 3
  timeout: 60
  log_level: INFO
```

## Roadmap

- [x] Multi-provider support
- [x] Sequential & parallel pipelines
- [x] Tool/function calling
- [x] Cost tracking
- [ ] Streaming responses
- [ ] Memory/context persistence
- [ ] Web UI dashboard
- [ ] Agent-to-agent communication protocol

## License

MIT
