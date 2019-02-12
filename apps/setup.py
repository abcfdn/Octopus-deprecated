import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abc-apps",
    version="0.0.1",
    author="shudong",
    author_email="shu@abcer.world",
    description="Applications of ABC events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abcfdn/Octopus/apps",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
