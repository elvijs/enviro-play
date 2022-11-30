"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Elvijs Sarkans",
    author_email='elvijs.sarkans@gmail.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    description="Two small apps. One to store Enviro+ data to a DB and one to visualise it",
    license="MIT license",
    long_description=readme,
    name="Enviro+ App",
    packages=["enviro_app"],
    package_dir={"enviro_app": "src/enviro_app"},
    url='https://github.com/elvijs/enviro-play',
    version='0.1.0',
)
