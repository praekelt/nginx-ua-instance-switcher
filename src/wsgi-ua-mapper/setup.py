from setuptools import setup, find_packages

setup(
    name='wsgi-ua-mapper',
    version='0.0.1',
    description='WSGI app mapping requesting User Agent to arbitrary value through user defined module. Utilizes Wurfl to deliver requesting device info.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/wsgi-ua-mapper',
    packages = find_packages(),
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires = [
        'pywurfl',
    ],
    zip_safe=False,
)
