import os
import json
import requests
from openai import OpenAI
import anthropic
import ollama

class AIProvider:
    def __init__(self, config_manager):
        self.config = config_manager.config
        self.provider = self.config['default_provider']
        
    def set_provider(self, provider):
        if provider in self.config['providers']:
            self.provider = provider
        else:
            raise ValueError(f"Provider {provider} not configured")
    
    def get_extensions(self, url, headers, max_extensions):
        prompt = self.create_prompt(url, headers, max_extensions)
        
        if self.provider == 'openai':
            return self._openai_request(prompt)
        elif self.provider == 'anthropic':
            return self._anthropic_request(prompt)
        elif self.provider == 'ollama':
            return self._ollama_request(prompt)
        elif self.provider == 'openrouter':
            return self._openrouter_request(prompt)
    
    def create_prompt(self, url, headers, max_extensions):
        return f"""
Given the following URL and HTTP headers, suggest the most likely file extensions for fuzzing this endpoint.
Respond with a JSON object containing a list of extensions. The response will be parsed with json.loads(),
so it must be valid JSON. No preamble or yapping. Use the format: {{"extensions": [".ext1", ".ext2", ...]}}.
Do not suggest more than {max_extensions}, but only suggest extensions that make sense. For example, if the path is 
/js/ then don't suggest .css as the extension. Also, if limited, prefer the extensions which are more interesting.
The URL path is great to look at for ideas. For example, if it says presentations, then it's likely there 
are powerpoints or pdfs in there. If the path is /js/ then it's good to use js as an extension.

Examples:
1. URL: https://example.com/presentations/FUZZ
   Headers: {{"Content-Type": "application/pdf", "Content-Length": "1234567"}}
   JSON Response: {{"extensions": [".pdf", ".ppt", ".pptx"]}}

2. URL: https://example.com/FUZZ
   Headers: {{"Server": "Microsoft-IIS/10.0", "X-Powered-By": "ASP.NET"}}
   JSON Response: {{"extensions": [".aspx", ".asp", ".exe", ".dll"]}}

URL: {url}
Headers: {headers}

JSON Response:
"""
    
    def _openai_request(self, prompt):
        provider_config = self.config['providers']['openai']
        ai_config = self.config['ai']
        
        if not provider_config['api_key'] and not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API key not configured")
            
        client = OpenAI(
            api_key=provider_config['api_key'] or os.getenv('OPENAI_API_KEY'),
            base_url=provider_config['base_url']
        )
        
        response = client.chat.completions.create(
            model=provider_config['model'],
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests file extensions for fuzzing based on URL and headers."},
                {"role": "user", "content": prompt}
            ],
            temperature=ai_config['temperature'],
            max_tokens=ai_config['max_tokens']
        )
        return json.loads(response.choices[0].message.content.strip())
    
    def _anthropic_request(self, prompt):
        provider_config = self.config['providers']['anthropic']
        ai_config = self.config['ai']
        
        if not provider_config['api_key'] and not os.getenv('ANTHROPIC_API_KEY'):
            raise ValueError("Anthropic API key not configured")
            
        client = anthropic.Anthropic(
            api_key=provider_config['api_key'] or os.getenv('ANTHROPIC_API_KEY')
        )
        
        message = client.messages.create(
            model=provider_config['model'],
            max_tokens=ai_config['max_tokens'],
            temperature=ai_config['temperature'],
            system="You are a helpful assistant that suggests file extensions for fuzzing based on URL and headers.",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(message.content[0].text)
    
    def _ollama_request(self, prompt):
        provider_config = self.config['providers']['ollama']
        
        try:
            response = ollama.chat(
                model=provider_config['model'],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that suggests file extensions for fuzzing based on URL and headers."},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(response['message']['content'])
        except Exception as e:
            print(f"Error connecting to Ollama at {provider_config['base_url']}: {e}")
            raise
    
    def _openrouter_request(self, prompt):
        provider_config = self.config['providers']['openrouter']
        ai_config = self.config['ai']
        
        if not provider_config['api_key'] and not os.getenv('OPENROUTER_API_KEY'):
            raise ValueError("OpenRouter API key not configured")
            
        headers = {
            'Authorization': f"Bearer {provider_config['api_key'] or os.getenv('OPENROUTER_API_KEY')}",
            'Content-Type': 'application/json'
        }
        
        if provider_config.get('site_url'):
            headers['HTTP-Referer'] = provider_config['site_url']
        if provider_config.get('site_name'):
            headers['X-Title'] = provider_config['site_name']
            
        data = {
            'model': provider_config['model'],
            'messages': [
                {"role": "system", "content": "You are a helpful assistant that suggests file extensions for fuzzing based on URL and headers."},
                {"role": "user", "content": prompt}
            ],
            'temperature': ai_config['temperature'],
            'max_tokens': ai_config['max_tokens']
        }
        
        response = requests.post(
            f"{provider_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=ai_config['timeout']
        )
        response.raise_for_status()
        return json.loads(response.json()['choices'][0]['message']['content'].strip()) 