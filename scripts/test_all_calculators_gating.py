import os
import re

tools_dir = os.path.join('app', 'static', 'tools')
tools = [f for f in os.listdir(tools_dir) if f.endswith('.html')]

print(f"Checking {len(tools)} calculator tools for gate integrity:")
for tool in tools:
    tool_path = os.path.join(tools_dir, tool)
    with open(tool_path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_sync = 'requireConsentToReveal' in content
    has_script = 'nv_profile_sync.js' in content
    
    print(f"  [{'OK' if has_sync and has_script else 'FAIL'}] {tool}: requireConsentToReveal={has_sync}, nv_profile_sync={has_script}")

