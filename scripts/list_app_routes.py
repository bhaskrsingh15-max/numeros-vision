import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import FastAPI app without starting TestClient
from app.main import app

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    routes = []
    for route in app.routes:
        path = getattr(route, 'path', None)
        methods = getattr(route, 'methods', None)
        name = getattr(route, 'name', None)
        routes.append((path, methods, name))
    
    print(f"Total routes on app: {len(routes)}")
    # Print routes that match about or other pages
    for path, methods, name in sorted(routes, key=lambda x: str(x[0])):
        if any(term in str(path) for term in ['about', 'tools', 'blog', 'privacy', 'terms', 'contact', 'disclaimer']):
            print(f"{str(path):40} {methods} ({name})")

if __name__ == '__main__':
    main()
