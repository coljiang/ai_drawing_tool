"""Requirement Role module for analyzing drawing requirements."""
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
    DRAW_REQ_PROMPT_SYSTEM_TEMPLATE, 
    DRAW_REQ_PROMPT_TEMPLATE
)


@register_tool(include_functions=["write_new_requirement"])
class RequirementRole(RoleZero):
    """Role for analyzing and structuring drawing requirements."""
    
    name: str = "AliceV1"
    profile: str = "画图需求分析专家"
    goal: str = "将用户的自然语言描述转为结构化的画图需求"
    instruction: str = """
    1. **需求结构化转换**：将用户自然语言描述转换为标准化的画图需求说明文档
    2. **信息补全优化**：对不完整的输入进行智能补充，确保需求可执行
    3. **风格规范管理**：维护风格标准库，推荐最适合的艺术表现形式
    """
    terminal: Terminal = Field(default_factory=Terminal, exclude=True)
    tools: list[str] = [
        "Plan",
        "Editor",
        "RoleZero",
        "Terminal:run_command",
        "Browser:goto,scroll",
        "RequirementRole",
    ]
    
    def _update_tool_execution(self):
        """Update tool execution mapping."""
        self.tool_execution_map.update({
            "RequirementRole.write_new_requirement": self.write_new_requirement,
            "Terminal.run_command": self.terminal.run_command,
        })
    
    async def write_new_requirement(self, path: str, file_description: str = "") -> str:
        """Write a new requirement file.

        Args:
            path (str): The absolute path of the file to be created.
            file_description (optional, str): Brief description of the file content. Defaults to "".
        """
        path = self.editor._try_fix_path(path)
        plan_status, _ = self._get_plan_status()
        prompt = DRAW_REQ_PROMPT_TEMPLATE.format(
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
            rsp = await self.llm.aask(context, system_msgs=[DRAW_REQ_PROMPT_SYSTEM_TEMPLATE])
            await awrite(path, rsp)
            await reporter.async_report(path, "path")

        return f"The file {path} has been successfully created, with content:\n{rsp}"