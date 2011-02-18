from setuptools import setup, find_packages

setup(
    name='django-ua-mapper',
    version='0.0.9',
    description='Django management command mapping User-Agent header strings to user defined values. Resulting User-Agent:value set is stored in cache.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-ua-mapper',
    packages = find_packages(),
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires = [
        'pywurfl',
        'djanginxed'
    ],
    zip_safe=False,
)
