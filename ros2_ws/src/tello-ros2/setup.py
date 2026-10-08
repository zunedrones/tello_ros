from setuptools import find_packages, setup

package_name = 'tello-ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zune Drones',
    maintainer_email='dev@todo.todo',
    description='Publish DJI Tello camera frames as ROS 2 images.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_pub = tello_ros2.camera_pub:main',
        ],
    },
)
