from setuptools import setup, find_packages

setup(
    name="qos_api",
    version="0.1.9",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "websockets>=10.0",
        "pydantic>=1.8.0"
    ],
    python_requires=">=3.7",
    author="QOS",
    author_email="quoteos88@gmail.com",
    description="Official Python SDK for QOS Market Data API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/qos-max/qos-quote-api-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
