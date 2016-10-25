from setuptools import setup, find_packages
from pip.req import parse_requirements


def _to_list(requires):
    return [str(ir.req) for ir in requires]

install_requires = _to_list(parse_requirements('requirements.txt', session=False))
scrapely_requires = _to_list(parse_requirements('requirements-scrapely.txt', session=False))
tests_require = _to_list(parse_requirements('requirements-dev.txt', session=False))


setup(
    name='ferret',
    version='1.0',
    install_requires=install_requires + scrapely_requires,
    tests_require=tests_require,
    setup_requires=['pytest-runner==2.7.1'],
    packages=find_packages(),
)
