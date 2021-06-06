# from distutils.core import setup

# setup(
#     name='olistlib',
#     version='0.1',
#     description='Biblioteca para suporte do projeto Olist',
#     author='Marcelo Shirayama',
#     author_email='caixadecorreiodomarcelo@gmail.com',
#     packages=['olistlib']
# )

from setuptools import setup, find_packages


setup(
    name="olistlib",
    version="0.1.0",
    description="Delivery app",
    packages=find_packages(),
    include_package_data=True,
)
