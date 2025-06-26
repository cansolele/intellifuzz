#!/usr/bin/env python3
"""
InteliFuzz - AI-powered fuzzing tool
Enhanced version of ffufai with multiple AI providers support
"""

import argparse
import subprocess
import sys

from src.config import ConfigManager
from src.providers import AIProvider
from src.utils import get_headers, interactive_setup

def main():
    parser = argparse.ArgumentParser(description="InteliFuzz - AI-powered fuzzing tool")
    parser.add_argument("url", help="Target URL with FUZZ keyword")
    parser.add_argument("--setup", action="store_true", help="Run interactive setup")
    parser.add_argument("--provider", help="AI provider to use", 
                       choices=['openai', 'anthropic', 'ollama', 'openrouter'])
    parser.add_argument("--max-extensions", type=int, help="Maximum number of extensions to suggest")
    parser.add_argument("--ffuf-args", help="Additional arguments to pass to ffuf")
    
    args = parser.parse_args()
    
    if args.setup:
        interactive_setup()
        return
    
    try:
        # Initialize configuration and AI provider
        config_manager = ConfigManager()
        ai_provider = AIProvider(config_manager)
        
        # Set provider if specified
        if args.provider:
            ai_provider.set_provider(args.provider)
        
        # Get headers from the URL
        print(f"Fetching headers from {args.url}...")
        headers = get_headers(args.url)
        
        # Get max extensions setting
        max_extensions = args.max_extensions or config_manager.config['ffuf']['max_extensions']
        
        # Get AI suggestions
        print(f"Getting extension suggestions from {ai_provider.provider}...")
        response = ai_provider.get_extensions(args.url, headers, max_extensions)
        extensions = response.get('extensions', [])
        
        if not extensions:
            print("No extensions suggested. Exiting.")
            return
        
        print(f"Suggested extensions: {', '.join(extensions)}")
        
        # Create wordlist
        wordlist_path = "intellifuzz_extensions.txt"
        with open(wordlist_path, 'w') as f:
            for ext in extensions:
                f.write(f"{ext}\n")
        
        # Prepare ffuf command
        ffuf_path = config_manager.config['ffuf']['path']
        ffuf_cmd = [ffuf_path, "-u", args.url, "-w", wordlist_path]
        
        if args.ffuf_args:
            ffuf_cmd.extend(args.ffuf_args.split())
        
        # Run ffuf
        print(f"Running: {' '.join(ffuf_cmd)}")
        subprocess.run(ffuf_cmd)
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
