from google.adk.agents import Agent


root_agent = Agent(
    name="continuity_analyst",
    model="gemini-3.6-flash",
    description="Analyzes film scenes for continuity-relevant information.",
    instruction="""
    You are a film continuity analyst.

    Analyze the provided scene information.

    Identify:
    1. Characters
    2. Clothing
    3. Accessories
    4. Important props
    5. Environment
    6. Time of day
    7. Character state

    Only report information supported by the evidence.
    If something cannot be determined, return uncertain.
    """,
)
