import setuptools

with open('README.md') as f:
    long_description = f.read()

with open('VERSION') as f:
    version = f.read().strip()

setup_info = {
    'name': 'dominion_ai',
    'version': version,
    'author': 'Daniel Wiesenthal',
    'author_email': 'noone@bugmenot.com',
    'description': 'Simple Dominion bot',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'packages': setuptools.find_packages(),
    'python_requires': '>=3.7',
    'install_requires': ['fire'],
    'entry_points':{
        'console_scripts': [
            'dominion_bot=dominion_ai.dominion_bot:main',
        ]
    },
}

setuptools.setup(**setup_info)
