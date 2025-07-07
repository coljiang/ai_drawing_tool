"""Configuration module for the AI Drawing Tool."""
import os
from pathlib import Path
import yaml

class Config:
    """Configuration class supporting environment variables and YAML config."""
    # BASE_DIR = Path(__file__).parent.parent.parent.absolute()
    # WORKFLOW_DIR = BASE_DIR / "workflow"
    CONFIG_YAML = ""
    _cached_yaml = None  # 内部缓存，避免多次打开文件

    @classmethod
    def _load_yaml(cls):
        if cls._cached_yaml is None:
            try:
                with open(cls.CONFIG_YAML, 'r', encoding='utf-8') as f:
                    cls._cached_yaml = yaml.safe_load(f)
            except Exception:
                cls._cached_yaml = {}
        return cls._cached_yaml

    @classmethod
    def _get_draw_config(cls, key, default=None):
        yaml_conf = cls._load_yaml()
        val = yaml_conf
        for k in key.split('.'):
            if not isinstance(val, dict) or k not in val:
                return default
            val = val[k]
        return val

    # 支持三选一顺序：环境变量 > YAML > 代码默认
    @classmethod
    def get_workflow_path(cls):
        return  cls._get_draw_config('comfy.json_path', "/tmp/draw_test_v2")

    @classmethod
    def get_comfy_api_url(cls):
        return os.environ.get(
            "COMFY_API_URL",
            cls._get_draw_config('comfy.api', "http://127.0.0.1:8188")
        )

    @classmethod
    def get_log_level(cls):
        return os.environ.get("LOG_LEVEL", "DEBUG")
    @classmethod
    def comfy_client_id(cls):
        return 'test_client'
    @classmethod
    def get_proxy(cls):
        return cls._get_draw_config('comfy.proxy', "http://127.0.0.1:8188")