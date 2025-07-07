"""Team Leader role implementation for the AI Drawing Tool."""
from metagpt.roles.di.team_leader import TeamLeader as BaseTeamLeader
from src.prompts.prompt_templates import LEADER_TEMPLATE


class DrawingTeamLeader(BaseTeamLeader):
    """Team leader specific to drawing team coordination."""
    
    def __init__(self, **kwargs):
        """Initialize the DrawingTeamLeader with specific guidance for drawing projects."""
        super().__init__(**kwargs)
        self.thought_guidance = LEADER_TEMPLATE