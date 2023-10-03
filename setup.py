from setuptools import setup


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='bullgon',
  version='0.1.0',
  description='local device management',
  long_description=readme(),
  author='odra',
  author_email='me@lrossetti.com',
  url='https://github.com/odra/bullgon',
  license='MIT',
  package_dir={'': 'src'},
  packages=['bullgon'],
  install_requires=['click>=8.1.7,<=9.0.0'],
  entry_points={
    'console_scripts': ['bullgon=bullgon.cli:run']
  },
)
