from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'perception_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='感知组入门示例：最小发布者与订阅者',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'talker = perception_demo.talker:main',
            'listener = perception_demo.listener:main',
        ],
    },
)
