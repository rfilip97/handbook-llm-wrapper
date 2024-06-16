from setuptools import setup, find_packages

setup(
    name="af_andbook_assistant",
    version="0.1.0",
    description="An assistant package",
    packages=find_packages(),
    install_requires=[
        "langchain_community"
        "pickle-mixin"
        "faiss-cpu"
        "langchain"
        "llama-cpp-python"
        "unstructured[md]"
        "sentence-transformers"
    ],
    entry_points={
        "console_scripts": [
            "assistant=assistant.__main__:main",
        ],
    },
    python_requires=">=3.12",
)
