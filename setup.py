from setuptools import setup, find_packages

setup(
    name="handbook_llm_wrapper",
    version="0.1.0",
    description="An assistant package",
    packages=find_packages(include=['handbook_llm_wrapper', 'handbook_llm_wrapper.*']),
    install_requires=[
        "langchain_community",
        "pickle-mixin",
        "faiss-cpu",
        "langchain",
        "llama-cpp-python",
        "unstructured[md]",
        "sentence-transformers",
    ],
    entry_points={
        "console_scripts": [
            "assistant=handbook_llm_wrapper.main:main",
        ],
    },
    python_requires=">=3.12",
)

