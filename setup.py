from setuptools import find_packages
from setuptools import setup

setup(
    name="inferra",
    version="0.1.0",  # You can update this or use dynamic versioning
    packages=find_packages(where="inferra/src"),
    package_dir={"": "inferra/src"},
    install_requires=[
        "keras>=3.5",
        "absl-py",
        "numpy",
        "packaging",
        "regex",
        "rich",
        "kagglehub",
        "tensorflow-text;platform_system != 'Windows'",
    ],
    python_requires=">=3.9",
    description="Pretrained models and tools for Inferra.",
    author="Inferra contributors",
    author_email="ma2736666@gmail.com",
    license="Apache-2.0",
)
