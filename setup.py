from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='abhishek kurade',
    author_email='jollyrancher1409@gmail.com',
    install_requires=[
        "groq",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)