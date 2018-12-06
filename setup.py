from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='bitclone',
      version='0.30',
      description='Clone all your bitbucket repo',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/rytsh/bitclone',
      author='Eray Ates',
      author_email='eates23@gmail.com',
      entry_points={
        'console_scripts': [
            'bitclone=bitclone.__main__:main',
        ],
      },
      packages=find_packages(),
      install_requires=[
          'requests', 'argparse', 'future'
      ],
      zip_safe=False,
      classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Topic :: System :: Software Distribution",
      ),
      keywords='bitbucket clone repo link',
)
