import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="dyndns_server-TheTimmoth",
    version="0.1.0a1",
    author="Tim Schlottmann",
    author_email="tschlottmann@gmail.com",
    description=
    "The server component of a python based tls encrypted ddns serivce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheTimmoth/dyndns-server",
    packages=setuptools.find_packages(),
    keywords=["ddns", "dnydns"],
    license_file="./LICENSE",
    platforms="Linux",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha", "Environment :: Console"
    ],
    python_requires='>=3.6',
)
