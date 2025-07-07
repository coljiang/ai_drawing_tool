"""Roles package initialization."""
from src.roles.requirement_role import RequirementRole
from src.roles.comfyprompt_writer_role import ComfyPromptWriterRole
from src.roles.comfy_draw_role import ComfyDrawRole
from src.roles.prompt_review_role import PromptReviewRole
from src.roles.team_leader import DrawingTeamLeader

__all__ = [
    "RequirementRole",
    "ComfyPromptWriterRole",
    "ComfyDrawRole",
    "PromptReviewRole",
    "DrawingTeamLeader",
]