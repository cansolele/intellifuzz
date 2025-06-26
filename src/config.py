import os
import yaml

class ConfigManager:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return self.create_default_config()
    
    def create_default_config(self):
        default_config = {
            'providers': {
                'openai': {'api_key': '', 'model': 'gpt-4o', 'base_url': 'https://api.openai.com/v1'},
                'anthropic': {'api_key': '', 'model': 'claude-3-5-sonnet-20241022'},
                'ollama': {'base_url': 'http://localhost:11434', 'model': 'llama3.2'},
                'openrouter': {'api_key': '', 'model': 'openai/gpt-4o', 'base_url': 'https://openrouter.ai/api/v1', 'site_url': '', 'site_name': ''}
            },
            'default_provider': 'openai',
            'ffuf': {'path': 'ffuf', 'max_extensions': 4},
            'ai': {'temperature': 0, 'max_tokens': 1000, 'timeout': 30}
        }
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False) 