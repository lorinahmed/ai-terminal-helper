from setuptools import setup, find_packages

setup(
    name="ai-terminal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'psutil>=5.9.0',
        'PyYAML>=6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'ait=aiterminal.clh:main',  # Updated entry point
        ],
    },
    package_data={
        'aiterminal': ['config.yaml'],  # Updated package data path
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered command-line helper",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-terminal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
) 