from setuptools import setup, find_packages


setup(
    name='osn2osm',
    version='0.0.2',
    description='Transform OpenStreetMap notes (*.osn) to (*.osm) file.',
    author='Pavel Tyslacki',
    author_email='pavel.tyslacki@gmail.com',
    license='The MIT License: http://opensource.org/licenses/MIT',
    packages=find_packages(),
    scripts=['osn2osm.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=open('requirements.txt').read().strip().splitlines(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)
