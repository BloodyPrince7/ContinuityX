"""Unit and integration tests for Continuity Analyst Agent."""

import asyncio
import json
import os
import unittest
from dotenv import load_dotenv

load_dotenv()

from schemas.scene_state import SceneState, CharacterState, PropState, EnvironmentState
from agents.continuity_agent.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai import types


class TestSceneStateSchema(unittest.TestCase):
    """Test SceneState Pydantic model validation and serialization."""

    def test_schema_instantiation_and_defaults(self):
        state = SceneState(
            scene_id="scene_01",
            characters=[
                CharacterState(
                    name="Detective",
                    clothing=["black jacket"],
                    accessories=[],
                    injuries=[],
                    position="standing",
                    state="observed",
                )
            ],
            props=[
                PropState(
                    name="pistol",
                    appearance="handgun",
                    color="silver",
                    state="held",
                    holder="Detective",
                    hand="right",
                )
            ],
            environment=EnvironmentState(
                location="office",
                time_of_day="night",
                weather="uncertain",
                lighting="dim",
            ),
            observations=["Character holding silver weapon in right hand"],
        )

        self.assertEqual(state.scene_id, "scene_01")
        self.assertEqual(len(state.characters), 1)
        self.assertEqual(state.characters[0].name, "Detective")
        self.assertEqual(state.props[0].hand, "right")
        self.assertEqual(state.environment.time_of_day, "night")
        self.assertEqual(state.environment.weather, "uncertain")

    def test_uncertainty_values(self):
        """Verify uncertain/not_visible values parse correctly."""
        raw = {
            "scene_id": "scene_02",
            "characters": [
                {
                    "name": "Unknown Person",
                    "clothing": ["not_visible"],
                    "accessories": [],
                    "injuries": [],
                    "position": "uncertain",
                    "state": "uncertain",
                }
            ],
            "props": [
                {
                    "name": "unclear object",
                    "appearance": "uncertain",
                    "color": "uncertain",
                    "state": "uncertain",
                    "holder": "none",
                    "hand": "not_visible",
                }
            ],
            "environment": {
                "location": "uncertain",
                "time_of_day": "uncertain",
                "weather": "uncertain",
                "lighting": "uncertain",
            },
            "observations": ["Occluded subject with uncertain props"],
        }
        state = SceneState.model_validate(raw)
        self.assertEqual(state.characters[0].clothing, ["not_visible"])
        self.assertEqual(state.props[0].color, "uncertain")
        self.assertEqual(state.environment.time_of_day, "uncertain")


class TestMultimodalContinuityAgent(unittest.TestCase):
    """Integration test verifying multimodal image analysis with Gemini and ADK."""

    def test_multimodal_image_analysis(self):
        frame_path = os.path.join("test_data", "scene_01", "frame_01.jpg")
        if not os.path.exists(frame_path):
            self.skipTest(f"Test frame {frame_path} not found.")

        if not os.getenv("GOOGLE_API_KEY"):
            self.skipTest("GOOGLE_API_KEY environment variable not set.")

        async def _run():
            with open(frame_path, "rb") as f:
                image_bytes = f.read()

            runner = InMemoryRunner(agent=root_agent)
            session = await runner.session_service.create_session(
                user_id="test_runner",
                app_name=runner.app_name,
            )

            content = types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    types.Part.from_text(
                        text="Analyze this film frame for continuity and output SceneState."
                    ),
                ],
            )

            raw_response = ""
            async for event in runner.run_async(
                user_id="test_runner",
                session_id=session.id,
                new_message=content,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            raw_response += part.text

            return raw_response

        raw_response = asyncio.run(_run())
        self.assertTrue(len(raw_response) > 0, "Expected non-empty response from agent")

        # Parse into SceneState model
        scene_state = SceneState.model_validate_json(raw_response)
        self.assertIsInstance(scene_state, SceneState)
        self.assertTrue(len(scene_state.characters) >= 1)
        self.assertTrue(len(scene_state.props) >= 1)
        self.assertIsNotNone(scene_state.environment)


if __name__ == "__main__":
    unittest.main()
