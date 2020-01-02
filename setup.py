import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as r:
    requirements = r.read().splitlines()

setuptools.setup(
    name = "registrycleaner",
    version = "0.0.1",
    author = "Ali YILDIZ",
    author_email = "ali.yildiz@alegradigital.com",
    description = "A pip package for deleting tag in private docker registry",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/alegraio/registry-cleaner",
    maintainer = "Ali YILDIZ",
    packages = setuptools.find_packages(),
    entry_points = {
            'console_scripts': [
                'registrycleaner = src.registrycleaner:main'
            ]
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = requirements,
    python_requires='>=3.6',
)
