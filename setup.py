from setuptools import setup


VERSION = "0.1.0a3"
GITHUB = "https://github.com/izxxr/luster"
DOCUMENTATION = "https://luster.readthedocs.io"
LICENSE = "MIT"
PACKAGES = [
    "luster",
    "luster.internal",
    "luster.types",
]

with open("README.MD", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()

    while "\n" in REQUIREMENTS:
        REQUIREMENTS.remove("\n")

EXTRA_REQUIREMENTS = {
    'speed': [
        'msgpack',
        'orjson>=5.4.0',
        'aiodns>=1.1',
        'cchardet',
        'Brotli',
    ],
}

setup(
    name="luster",
    author="izxxr",
    version=VERSION,
    license=LICENSE,
    url=GITHUB,
    project_urls={
        "Documentation": DOCUMENTATION,
        "Issue tracker": GITHUB + "/issues",
    },
    description='[Pre-Alpha] Python library for Revolt.chat.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extra_requires=EXTRA_REQUIREMENTS,
    packages=PACKAGES,
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)
