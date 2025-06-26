import requests
from .config import ConfigManager

def get_headers(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return dict(response.headers)
    except requests.RequestException as e:
        print(f"Error fetching headers: {e}")
        return {"Header": "Error fetching headers."}

def interactive_setup():
    print("InteliFuzz Interactive Setup")
    print("=" * 30)
    
    config_manager = ConfigManager()
    
    # Provider selection
    providers = list(config_manager.config['providers'].keys())
    print(f"\nAvailable providers: {', '.join(providers)}")
    provider = input(f"Choose default provider [{config_manager.config['default_provider']}]: ").strip()
    if provider and provider in providers:
        config_manager.config['default_provider'] = provider
    
    selected_provider = config_manager.config['default_provider']
    provider_config = config_manager.config['providers'][selected_provider]
    
    # Configure selected provider
    print(f"\nConfiguring {selected_provider}:")
    
    if selected_provider in ['openai', 'anthropic', 'openrouter']:
        current_key = provider_config.get('api_key', '')
        api_key = input(f"API key [{current_key[:10] + '...' if current_key else 'not set'}]: ").strip()
        if api_key:
            provider_config['api_key'] = api_key
    
    if selected_provider == 'ollama':
        base_url = input(f"Ollama URL [{provider_config['base_url']}]: ").strip()
        if base_url:
            provider_config['base_url'] = base_url
    
    if selected_provider == 'openrouter':
        site_url = input(f"Site URL (optional) [{provider_config.get('site_url', '')}]: ").strip()
        if site_url:
            provider_config['site_url'] = site_url
        site_name = input(f"Site name (optional) [{provider_config.get('site_name', '')}]: ").strip()
        if site_name:
            provider_config['site_name'] = site_name
    
    # Model selection
    current_model = provider_config['model']
    model = input(f"Model [{current_model}]: ").strip()
    if model:
        provider_config['model'] = model
    
    # ffuf settings
    ffuf_path = input(f"ffuf path [{config_manager.config['ffuf']['path']}]: ").strip()
    if ffuf_path:
        config_manager.config['ffuf']['path'] = ffuf_path
    
    max_ext = input(f"Max extensions [{config_manager.config['ffuf']['max_extensions']}]: ").strip()
    if max_ext.isdigit():
        config_manager.config['ffuf']['max_extensions'] = int(max_ext)
    
    config_manager.save_config()
    print("\nConfiguration saved to config.yaml") 