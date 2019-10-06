import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='firestore_rest',
     version='0.1',
     author="Evan Richard",
     author_email="evan.richard.umd@gmail.com",
     description="A Firestore REST api utility package",
     long_description=long_description,
     long_description_content_type='text/markdown',
     url="https://github.com/evan-richard/firestore_rest",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 2.6",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
