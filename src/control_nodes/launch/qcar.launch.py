from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='qcar_nodes',
            node_executable='qcar_node',
            name='qcar_node'
        ),
        Node(
            package='qcar_nodes',
            node_executable='command_node',
            name='command'
        ),

        # Node(package='qcar_nodes',
        #      node_executable='lidar_node',
        #      name='lidar_node'),

        # Node(
        #     package='qcar_nodes',
        #     node_executable='rgbd_node',
        #     name='rgbd_node'
        # ),

        Node(
            package='qcar_nodes',
            node_executable='csi_node',
            name='csi_node'
        ),


        # Node(package='control_nodes',
        #      node_executable='wall_follow',
        #      name='wall_follow')
    ])
