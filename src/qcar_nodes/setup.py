from setuptools import setup

package_name = 'qcar_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nvidia',
    maintainer_email='nvidia@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ "command_node=qcar_nodes.commandnode:main","csi_node=qcar_nodes.csinode:main","img_node=qcar_nodes.Imageviewer:main","lidar_node=qcar_nodes.lidarnode:main","qcar_node=qcar_nodes.qcarnode:main","rgbd_node=qcar_nodes.rgbdnode:main","image_recorder=qcar_nodes.ImageRecorder:main","test_node=qcar_nodes.lidar_test:main"
        ],
    },
)
