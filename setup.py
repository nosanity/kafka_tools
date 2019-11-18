from setuptools import setup, find_packages

setup(
    name='kafka_tools',
    version='0.1',
    packages=find_packages(),
    description='kafka producer and consumer',
    url='http://example.com',
    author='author',
    install_requires=['aiokafka==0.5.2', 'jsonschema']
)
