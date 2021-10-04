import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bf2mesh", # Replace with your own username
    version="0.0.1",
    author="Nikita Gotsko",
    author_email="irpoxotaujio@gmail.com",
    description="Library for reading and writing Battlefield 2 mesh files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rPoXoTauJIo/bf2mesh",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)