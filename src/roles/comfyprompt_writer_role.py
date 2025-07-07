"""ComfyUI Prompt Writer Role module for generating detailed prompts."""
import os
from pathlib import Path
from pydantic import Field

from metagpt.roles.di.role_zero import RoleZero
from metagpt.tools.tool_registry import register_tool
from metagpt.tools.libs.terminal import Terminal
from metagpt.schema import UserMessage
from metagpt.utils.report import EditorReporter
from metagpt.utils.common import awrite

from src.prompts.prompt_templates import (
    DRAW_COMPYUI_PROMPT_SYSTEM_TEMPLATE, 
    DRAW_COMPYUI_PROMPT_TEMPLATE
)


@register_tool(include_functions=["write_new_comfyUI_prompt"])
class ComfyPromptWriterRole(RoleZero):
    """Role for generating ComfyUI prompts from structured requirements."""
    
    name: str = "Bob"
    profile: str = "ComfyUI prompt专家"
    goal: str = "将结构化的画图需求转为ComfyUI prompt"
    instruction: str = "You are a professional ComfyUI prompt engineer specialized in generating highly detailed and structured image generation prompts."

    terminal: Terminal = Field(default_factory=Terminal, exclude=True)
    tools: list[str] = [
        "Plan",
        "Editor",
        "RoleZero",
        "Terminal:run_command",
        "ComfyPromptWriterRole",
    ]
    
    def _update_tool_execution(self):
        """Update tool execution mapping."""
        self.tool_execution_map.update({
            "ComfyPromptWriterRole.write_new_comfyUI_prompt": self.write_new_comfyUI_prompt,
            "Terminal.run_command": self.terminal.run_command,
        })

    async def write_new_comfyUI_prompt(self, path: str, file_description: str = "") -> str:
        """Write a new comfyUI prompt file.

        Args:
            path (str): The absolute path of the file to be created.
            file_description (optional, str): Brief description of the file content. Defaults to "".
        """
        path = self.editor._try_fix_path(path)
        plan_status, _ = self._get_plan_status()
        prompt = DRAW_COMPYUI_PROMPT_TEMPLATE.format(
            user_requirement=self.planner.plan.goal,
            plan_status=plan_status,
            file_path=path,
            file_description=file_description,
            file_name=os.path.basename(path),
        )
        
        memory = self.rc.memory.get(self.memory_k)[:-1]
        context = self.llm.format_msg(memory + [UserMessage(content=prompt)])

        async with EditorReporter(enable_llm_stream=True) as reporter:
            await reporter.async_report(
                {"type": "draw_design", "filename": Path(path).name, "src_path": path}, 
                "meta"
            )
            rsp = await self.llm.aask(context, system_msgs=[DRAW_COMPYUI_PROMPT_SYSTEM_TEMPLATE])
            await awrite(path, rsp)
            await reporter.async_report(path, "path")

        return f"The file {path} has been successfully created, with content:\n{rsp}"