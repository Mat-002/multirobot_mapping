import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace

from launch_ros.actions import Node


def generate_launch_description():
    launch_file_dir = os.path.join(get_package_share_directory('multirobot_mapping'), 'launch')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose_r1 = LaunchConfiguration('x_pose_r1', default='-2.0')
    y_pose_r1 = LaunchConfiguration('y_pose_r1', default='-0.5')
    ns_r1 = LaunchConfiguration('ns_r1', default='robot1')

    world = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'stanza.world'
    )

    gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world]}.items()
    )

    set_env_vars_resources = AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'models'))


                                # ROBOT1
    # ROBOT1 (Avvolto nel Namespace)
    robot1_group = GroupAction([
        # Questa è la magia: tutti i nodi lanciati dentro questo gruppo 
        # verranno automaticamente inseriti nel namespace 'robot1'
        PushRosNamespace(ns_r1),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(launch_file_dir, 'publisher_tb3.launch.py')
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'frame_prefix': ns_r1
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(launch_file_dir, 'spawn_tb3.launch.py')
            ),
            launch_arguments={
                'x_pose': x_pose_r1,
                'y_pose': y_pose_r1,
                'namespace': ns_r1
            }.items()
        )
    ])

    # robot_state_publisher1_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(launch_file_dir, 'publisher_tb3.launch.py')
    #     ),
    #     launch_arguments={
    #         'use_sim_time': use_sim_time,
    #         'frame_prefix' : ns_r1
    #         }.items()
    # )

    # spawn_turtlebot1_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(launch_file_dir, 'spawn_tb3.launch.py')
    #     ),
    #     launch_arguments={
    #         'x_pose': x_pose_r1,
    #         'y_pose': y_pose_r1,
    #         'namespace' :ns_r1
    #     }.items()
    # )



    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(set_env_vars_resources)
    ld.add_action(gazebo_cmd)
    # ld.add_action(spawn_turtlebot1_cmd)
    # ld.add_action(robot_state_publisher1_cmd)
    ld.add_action(robot1_group)

    return ld
