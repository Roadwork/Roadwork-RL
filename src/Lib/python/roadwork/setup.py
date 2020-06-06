import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='roadwork',  
     version='0.0.1',
     author="Xavier Geerinck",
     author_email="xavier.geerinck@gmail.com",
     description="Roadwork-RL - A RL Environment Wrapper",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/roadwork/roadwork-rl",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.6'
 )