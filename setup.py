import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='TC_theme',
    version='1.0',
    packages=['TC_theme'],
    license='MIT',
    description='Custom theme and functions for MMP plots',
    long_description=long_description,
    long_description_content_type="text/markdown",  
    author='Nicolò Iaselli',
    author_email='niaselli@thorcon.us',
    install_requires=['requests'],
    
    download_url="https://github.com/nicolo-iaselli/TC_theme/archive/refs/tags/v1.0.tar.gz"
    
)
