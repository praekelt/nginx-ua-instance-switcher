from setuptools import setup, find_packages

setup(
    name='example-mapper',
    version='0.0.1',
    description='',
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/nginx-ua-instance-switcher',
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
        'wsgi-ua-mapper'
    ],
    zip_safe=False,
)
