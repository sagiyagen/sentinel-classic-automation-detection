from setuptools import setup, find_packages

setup(
    name="sentinel-classic-automation-detection",
    version="1.0.0",
    description="Tool to detect Microsoft Sentinel analytic rules using classic automation that need migration",
    author="Sentinel Automation Team",
    packages=find_packages(),
    install_requires=[
        "azure-identity>=1.15.0",
        "azure-mgmt-securityinsight>=3.0.0",
        "azure-mgmt-resource>=23.0.0",
    ],
    entry_points={
        'console_scripts': [
            'sentinel-detect=sentinel_detector.cli:main',
        ],
    },
    python_requires='>=3.8',
)
