from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('freedom')

    config_file = PathJoinSubstitution([pkg_share, 'config', 'indoor_stairs.yaml'])
    rviz_config_file = PathJoinSubstitution([pkg_share, 'config', 'rviz_indoor.rviz'])

    pcd_save_path = PathJoinSubstitution([pkg_share, 'generated_pcd/'])
    fov_mask_path = PathJoinSubstitution([pkg_share, 'config/'])

    freedom_node = Node(
        package='freedom',
        executable='freedom_node',
        name='freedom',
        output='screen',
        parameters=[
            config_file,
            {
                'pointcloud_topic': '/unilidar/cloud',
                'map_tf_frame': 'unilidar_lidar',
                'sensor_tf_frame': 'unilidar_lidar',
                'save_map_topic': '/save_map',
                'save_map_path': pcd_save_path,
                'fov_mask_path': fov_mask_path,
                'learn_fov': False,
                'enable_visualization': True,
            }
        ],
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', rviz_config_file],
    )

    return LaunchDescription([
        freedom_node,
        #rviz_node,
    ])
