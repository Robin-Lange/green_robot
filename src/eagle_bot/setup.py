from setuptools import setup
from glob import glob
import os
package_name = 'eagle_bot'


setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    (os.path.join('share', package_name, 'description'), glob(os.path.join('description', '*.xacro'))),
    (os.path.join('share', package_name, 'config'), glob('config/*')),
    (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
    (os.path.join('share', package_name, 'map'), glob(os.path.join('map', '*.yaml')) + glob(os.path.join('map', '*.pgm'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tim',
    maintainer_email='tim@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',    
    entry_points={
        'console_scripts': [
        'vid = eagle_bot.RGBVideoSaver:main',
        'datascrub = eagle_bot.datascrub:main',
        ],
    },
)
