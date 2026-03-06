from setuptools import setup

package_name = 'control_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         ('share/' + package_name + '/launch',
            ['launch/qcar.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['qcar_ekf = control_nodes.qcar_ekf:main','wall_follow = control_nodes.wall_follow:main','lane_detect=control_nodes.lane_detect:main',
        ],
    },
)
