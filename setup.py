from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='volatile_dictionary',
      version='0.1',
      description="An extension of python's native dictionary"
                  " class, that implements volatile sets.",
      url='https://github.com/pedrogyrao/volatile_dictionary',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='gyrao',
      author_email='pedrogyrao@hotmail.com',
      license='MIT',
      packages=['volatile_dictionary'],
      install_requires=['apscheduler'],
      classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
      ],
      zip_safe=False)
