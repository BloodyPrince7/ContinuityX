# AI Architecture & Continuity Engine

## Overview
CineTrace AI Agent architecture for film continuity tracking, multimodal scene analysis, and inconsistency detection.

## Structure
- `agents/`: AI agents and reasoning modules (e.g. `agents/continuity_agent/agent.py`)
- `schemas/`: Strongly-typed Pydantic schemas representing scene states, characters, props, environment (`schemas/scene_state.py`)
- `tests/`: Automated unit and integration test suite (`tests/test_continuity_agent.py`)
- `test_data/`: Sample film frames and test fixtures (`test_data/scene_01/`)
- `docs/`: Architectural specifications, API documentation, and research notes

---

## Phase 1 — Step 3: Multimodal Scene State Observation

### Current Architecture Flow

```
IMAGE / FILM FRAME
        ↓
CONTINUITY ANALYST (Google ADK Agent)
        ↓
GEMINI MULTIMODAL (gemini-3.6-flash)
        ↓
STRUCTURED SCENE STATE (SceneState JSON)
```

### Observation vs. Error Detection
At this stage, the **Continuity Analyst** is strictly an **observation agent**:
- It inspects the visual frame (or image) without hallucination.
- It extracts characters, clothing, accessories, injuries, props, interaction hands, and environmental lighting.
- For ambiguous, out-of-frame, or unidentifiable properties, it explicitly assigns `"uncertain"` or `"not_visible"`.
- It **does NOT** determine continuity errors yet. Downstream stages (Continuity Comparison, Investigation Agent, Judge Agent) will consume these structured `SceneState` snapshots across takes/scenes to perform temporal diffing and verification.
