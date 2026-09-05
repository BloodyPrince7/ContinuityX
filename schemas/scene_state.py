"""Scene State Schemas for CineTrace Continuity Intelligence.

Defines strongly-typed Pydantic models for structured visual observations
extracted from film frames by the Continuity Analyst agent.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class CharacterState(BaseModel):
    """Visual state of an observed character in a film frame."""

    name: str = Field(
        description="Name or descriptive identifier of the character (e.g. 'Detective', 'Person in trenchcoat')."
    )
    clothing: List[str] = Field(
        default_factory=list,
        description="Visible garments and their colors/styles (e.g. ['black leather jacket', 'white button-down shirt']).",
    )
    accessories: List[str] = Field(
        default_factory=list,
        description="Visible accessories such as watches, glasses, jewelry, hats, or belts.",
    )
    injuries: List[str] = Field(
        default_factory=list,
        description="Visible injuries, wounds, cuts, bruises, or blood markings (e.g. ['cut over right eyebrow']).",
    )
    position: str = Field(
        default="observed",
        description="Observed posture or physical stance (e.g. 'standing', 'sitting', 'running', 'crouched', 'uncertain').",
    )
    state: str = Field(
        default="observed",
        description="Observed physical or action state (e.g. 'observed', 'speaking', 'alert', 'uncertain').",
    )


class PropState(BaseModel):
    """Visual state and interactions for a key prop or object."""

    name: str = Field(
        description="Name of the object or prop (e.g. 'pistol', 'coffee cup', 'folder', 'glasses')."
    )
    appearance: str = Field(
        default="uncertain",
        description="Visual description and physical attributes (e.g. 'silver semi-automatic handgun', 'ceramic mug').",
    )
    color: str = Field(
        default="uncertain",
        description="Dominant color of the prop, or 'uncertain' if color cannot be determined with certainty.",
    )
    state: str = Field(
        default="observed",
        description="Current state or condition of the prop (e.g. 'held', 'on desk', 'open', 'broken', 'empty').",
    )
    holder: str = Field(
        default="none",
        description="Name/identifier of the character holding or using the prop, or 'none' if unheld.",
    )
    hand: str = Field(
        default="none",
        description="Which hand holds or interacts with the prop: 'right', 'left', 'both', 'none', or 'not_visible'.",
    )


class EnvironmentState(BaseModel):
    """Environmental, lighting, and temporal context of the scene."""

    location: str = Field(
        default="uncertain",
        description="Setting or location type (e.g. 'office', 'alleyway', 'car interior', 'warehouse').",
    )
    time_of_day: str = Field(
        default="uncertain",
        description="Estimated time of day (e.g. 'night', 'day', 'dawn', 'dusk', 'uncertain'). Only state if visually supported.",
    )
    weather: str = Field(
        default="uncertain",
        description="Observed weather condition (e.g. 'rain', 'fog', 'clear', 'uncertain', 'interior').",
    )
    lighting: str = Field(
        default="uncertain",
        description="Lighting quality and mood (e.g. 'dim low-key', 'bright daylight', 'harsh neon', 'fluorescent overhead').",
    )


class SceneState(BaseModel):
    """Complete structured scene state extracted from a film frame."""

    scene_id: str = Field(
        default="scene_01",
        description="Identifier for the scene, shot, or frame (e.g. 'scene_01', 'shot_03', 'frame_01').",
    )
    characters: List[CharacterState] = Field(
        default_factory=list,
        description="List of characters visibly present in the frame.",
    )
    props: List[PropState] = Field(
        default_factory=list,
        description="List of significant props or objects visible or interacted with in the frame.",
    )
    environment: EnvironmentState = Field(
        default_factory=EnvironmentState,
        description="Environmental, spatial, and lighting conditions.",
    )
    observations: List[str] = Field(
        default_factory=list,
        description="Factual, verifiable visual observations supporting the analysis without speculative conclusions.",
    )
