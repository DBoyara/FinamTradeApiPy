from setuptools import find_packages, setup

setup(
    name="finam-trade-api",
    maintainer="DBoyara",
    maintainer_email="boyarshin.den@yandex.ru",
    packages=find_packages(),
    version="3.1.2",
    install_requires=["aiohttp >= 3.10.11, < 4.0.0", "pydantic >= 2.8.0, < 3.0.0"],
    python_requires=">3.11.0, <4",
    license="GNU GPL v.3.0",
    description="Асинхронный REST-клиент для API Finam",
    long_description="Примеры и описание здесь https://github.com/DBoyara/FinamTradeApiPy ",
    url="https://github.com/DBoyara/FinamTradeApiPy",
)
