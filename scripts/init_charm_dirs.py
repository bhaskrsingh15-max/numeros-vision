import os

dirs = [
    'app/charm',
    'app/charm/intent',
    'app/charm/numerology',
    'app/charm/charts',
    'app/charm/methods',
    'app/charm/rag',
    'app/charm/rules',
    'app/charm/consensus',
    'app/charm/remedies',
    'app/charm/chat',
    'app/charm/outcomes',
    'app/charm/audit'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    init_file = os.path.join(d, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('"""Charm AI Module Package."""\n')

print("Charm AI packages initialized successfully.")
