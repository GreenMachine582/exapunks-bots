import os

from setuptools import setup, find_packages


dir_name = os.path.abspath(os.path.dirname(__file__))

version_contents = {}
with open(os.path.join(dir_name, "src", "exapunks_bots", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

with open(os.path.join(dir_name, "README.md"), "r", encoding="utf-8") as file:
    long_description = file.read()


install_requires = [
    "Pillow",
]


setup(
    name="exapunks_bots",
    version=version_contents["VERSION"],
    author="Matthew Johnson",
    author_email="greenchicken1902@gmail.com",
    maintainer='Matthew Johnson',
    maintainer_email='greenchicken1902@gmail.com',
    description="Exapunks-Bots: Applied CV and AI to play Exapunks minigames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GreenMachine582/exapunks-bots",
    packages_dir={"": "src"},
    packages=find_packages(where="exapunks_bots"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="computer-vision, ml, machine-learning, python, exapunks-minigames",
    python_requires=">=3.9.0",
    install_requires=install_requires,
)
