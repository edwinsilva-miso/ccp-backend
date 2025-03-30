import os
from pathlib import Path
from dotenv import load_dotenv

os.environ['ENV'] = 'test'


def pytest_configure(config):
    root = Path(__file__).parent.parent
    env_path = root / '.env.test'
    load_dotenv(str(env_path))
    return config
