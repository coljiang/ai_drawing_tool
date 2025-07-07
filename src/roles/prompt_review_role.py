"""Prompt Review Role module for reviewing generated prompts."""
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger


class PromptReviewRole(Role):
    """Role for reviewing prompts and providing feedback."""
    
    name: str = "Charlie"
    profile: str = "PromptReviewRole"

    def __init__(self, **kwargs):
        """Initialize the PromptReviewRole."""
        super().__init__(**kwargs)
        
    async def _act(self) -> Message:
        """Act on the current todo item.
        
        Returns:
            Message: A message with the review feedback.
        """
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        context = self.get_memories()  # use all memories as context
        context_str = "\n".join(["{} : {}".format(msg.role, msg.content) for msg in context])

        code_text = await todo.run(context_str)  # specify arguments
        msg = Message(instruction=code_text, role=self.profile, cause_by=type(todo))

        return msg