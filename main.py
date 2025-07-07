"""Main module for the AI Drawing Tool."""
import asyncio
import time
import typer

from metagpt.logs import logger, define_log_level
from metagpt.schema import Message
from metagpt.environment.mgx.mgx_env import MGXEnv
import metagpt.const
from src.roles import (
    DrawingTeamLeader,
    RequirementRole,
    ComfyPromptWriterRole,
    ComfyDrawRole,
)
from src.config.config import Config


app = typer.Typer()


async def agent_draw_prompt(
    idea="", 
    user_defined_recipient="", 
    enable_human_input=False, 
    allow_idle_time=300
):
    """
    Run the AI drawing agent to process the drawing prompt.
    
    Args:
        idea (str): The drawing idea/prompt.
        user_defined_recipient (str): Specific role to send the message to.
        enable_human_input (bool): Whether to enable human input during the process.
        allow_idle_time (int): Maximum idle time before considering the process complete.
    """
    # Set up logging
    define_log_level(print_level="DEBUG", logfile_level="DEBUG")

    # Initialize environment
    env = MGXEnv()
    team_leader = DrawingTeamLeader()

    # Add roles to environment
    env.add_roles([
        team_leader,
        RequirementRole(),
        ComfyPromptWriterRole(),
        ComfyDrawRole()
    ])
    
    # Create and publish message
    msg = Message(content=idea)
    env.attach_images(msg)  # attach image content if applicable

    if user_defined_recipient:
        msg.send_to = {user_defined_recipient}
        env.publish_message(msg, user_defined_recipient=user_defined_recipient)
    else:
        env.publish_message(msg)

    # Run the environment
    allow_idle_time = allow_idle_time if enable_human_input else 1
    start_time = time.time()
    while time.time() - start_time < allow_idle_time:
        if not env.is_idle:
            await env.run()
            start_time = time.time()  # reset start time


@app.command()
def main(
    idea: str = typer.Argument(..., help="Drawing idea or prompt to process"),
    config_path: str = typer.Option(None, "--config", "-c", help="Path to config yaml", exists=True)
):
    """
    Main entry point for the AI Drawing Tool.
    
    Args:
        idea (str): The drawing idea/prompt to process.
    """
    Config.CONFIG_YAML = config_path
    workflow_path = Config.get_workflow_path()
    idea = str(idea)
    logger.info(f"Processing drawing idea: {idea}")
    asyncio.run(
        agent_draw_prompt(
            idea=idea, 
            enable_human_input=True, 
            user_defined_recipient=metagpt.const.TEAMLEADER_NAME
        )
    )


if __name__ == "__main__":



    app()