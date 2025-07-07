"""ComfyUI Drawing Role module for generating images."""
import os
import json
from pydantic import Field

from metagpt.roles.di.role_zero import RoleZero
from metagpt.tools.tool_registry import register_tool
from metagpt.tools.libs.terminal import Terminal

from src.config.config import Config


@register_tool(include_functions=["draw_comfyUI_prompt"])
class ComfyDrawRole(RoleZero):
    """Role for generating images using ComfyUI prompts."""
    
    name: str = "Dennis"
    profile: str = "ComfyUI 画图专家"
    goal: str = "将输入的ComfyUI prompt转化为图片"
    instruction: str = "你是一个 ComfyUI 画图专家，负责根据用户提供的 ComfyUI prompt 生成对应的图片"

    terminal: Terminal = Field(default_factory=Terminal, exclude=True)
    tools: list[str] = [
        "Plan",
        "Editor",
        "RoleZero",
        "Terminal:run_command",
        "ComfyDrawRole",
    ]
    
    def _update_tool_execution(self):
        """Update tool execution mapping."""
        self.tool_execution_map.update({
            "ComfyDrawRole.draw_comfyUI_prompt": self.draw_comfyUI_prompt,
            "Terminal.run_command": self.terminal.run_command,
        })

    async def draw_comfyUI_prompt(self, prompt_path: str = "") -> str:
        """Use given prompt file to call ComfyUI for drawing.

        Args:
            prompt_path (str): Path to prompt file in JSON format with positive_prompt and negative_prompt fields
        """
        try:
            from src.api.comfy_api import queue_prompt
        except ImportError:
            return "Error: comfy_api module not found. Please install it with 'pip install comfy-api'."
            
        # Load prompt from file
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file {prompt_path} does not exist.")
            
        with open(prompt_path, 'r', encoding='utf-8') as file:
            draw_prompt_info = json.load(file)
            
        positive_prompt = draw_prompt_info.get("positive_prompt", "")
        negative_prompt = draw_prompt_info.get("negative_prompt", "")
        
        if positive_prompt == "":
            raise ValueError("The positive_prompt field is required in the prompt file.")
        
        # Load workflow from configuration
        workflow_path = Config.get_workflow_path()
        
        with open(workflow_path, "r") as file:
            prompt = json.load(file)
            
        # Update prompt with positive and negative prompts
        prompt['6']['inputs']['text'] = positive_prompt
        prompt['7']['inputs']['text'] = negative_prompt
        
        # Queue the prompt and get response
        response = queue_prompt(prompt)
        
        return f"The drawing with positive_prompt: {positive_prompt} and negative_prompt: {negative_prompt} has been successfully created, with response:\n{response}"