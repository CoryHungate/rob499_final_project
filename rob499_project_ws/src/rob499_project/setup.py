from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rob499_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
		(os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hungatec',
    maintainer_email='hungatec@oregonstate.edu',
    description='package the can read serial data and uses it to control variables in turtlesim',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
			'serial_data = rob499_project.serial_data_publisher:main',
			'knob1 = rob499_project.knob1_node:main',
			'knob2 = rob499_project.knob2_node:main',
			'turtle_movement = rob499_project.turtle_movement:main',
			'kill_turtle = rob499_project.turtle_killer:main',
			'clear = rob499_project.clear_path:main',
			'change_pen = rob499_project.change_pen:main',
        ],
    },
)
