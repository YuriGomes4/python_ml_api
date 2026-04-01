from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='py_ml',
    version='0.9.1',
    license='MIT License',
    author='Yuri Gomes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='yurialdegomes@gmail.com',
    keywords='mercado livre',
    description=u'Wrapper não oficial do Mercado Livre',
    packages=['py_ml'],
    install_requires=['requests'],)