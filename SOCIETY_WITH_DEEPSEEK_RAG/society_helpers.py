import textwrap
from camel.societies import RolePlaying
from camel.types import ModelType, ModelPlatformType
from camel.configs import ChatGPTConfig
from camel.models import ModelFactory

def create_gpt4o_model():
    """
    Create and return the GPT‑4O mini model.
    """
    return ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
        model_config_dict=ChatGPTConfig(temperature=0.0).as_dict()
    )

def create_society(task_prompt, user_role_name, assistant_role_name, model):
    """
    Dynamically configure and return a RolePlaying Society session.
    """
    task_kwargs = {
        'task_prompt': task_prompt,
        'with_task_specify': True,
        'task_specify_agent_kwargs': {'model': model}
    }
    user_role_kwargs = {
        'user_role_name': user_role_name,
        'user_agent_kwargs': {'model': model}
    }
    assistant_role_kwargs = {
        'assistant_role_name': assistant_role_name,
        'assistant_agent_kwargs': {'model': model}
    }
    society = RolePlaying(
        **task_kwargs,
        **user_role_kwargs,
        **assistant_role_kwargs,
    )
    return society
