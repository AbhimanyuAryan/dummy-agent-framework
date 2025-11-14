from setuptools import setup, find_packages

setup(
    name="gemini-simple-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-genai>=1.27.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0",
        "rich>=14.1.0",
        "nest-asyncio>=1.6.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gemini-agent=gemini_agent.cli:main",
        ],
    },
    author="Your Name",
    description="Simple Gemini agent orchestration framework",
    python_requires=">=3.9",
)
