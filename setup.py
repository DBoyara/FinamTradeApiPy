from setuptools import find_packages, setup

setup(
    name="finam-trade-api",
    maintainer="DBoyara",
    maintainer_email="boyarshin.den@yandex.ru",
    packages=find_packages(),
    version="0.4.1",
    install_requires=["aiohttp >= 3.8.3, < 4.0.0", "pydantic >= 1.10.2, < 2.0.0"],
    python_requires=">3.7.0, <4",
    license="GNU GPL v.3.0",
    description="Асинхронный клиент для API Finam",
    long_description="Примеры и описание здесь https://github.com/DBoyara/FinamTradeApiPy ",
    url="https://github.com/DBoyara/FinamTradeApiPy",
)
