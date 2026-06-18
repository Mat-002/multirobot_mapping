#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction, DeclareLaunchArgument, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace
from launch.substitutions import PythonExpression

def generate_launch_description():
    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    declare_x_pose_arg_robot1 = DeclareLaunchArgument('x_pose_robot1', default_value='-2.0')
    declare_y_pose_arg_robot1 = DeclareLaunchArgument('y_pose_robot1', default_value='-0.5')

    declare_x_pose_arg_robot2 = DeclareLaunchArgument('x_pose_robot2', default_value='0.0')
    declare_y_pose_arg_robot2 = DeclareLaunchArgument('y_pose_robot2', default_value='1.0')

    declare_x_pose_arg_robot3 = DeclareLaunchArgument('x_pose_robot3', default_value='2.0')
    declare_y_pose_arg_robot3 = DeclareLaunchArgument('y_pose_robot3', default_value='-0.5')

    declare_use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='true')
    

    gz_sim_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r ', os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'worlds', 'stanza.world')]}.items()
    )

    clock_bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
    output='screen'
    )

    robot1_group = GroupAction(
        actions=[
            PushRosNamespace(
                PythonExpression(["'", "robot1", "'"])
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_turtlebot3_gazebo, 'launch', 'spawn_turtlebot3.launch.py')),
                launch_arguments={
                    'namespace': 'robot1',
                    'x_pose': LaunchConfiguration('x_pose_robot1'),
                    'y_pose': LaunchConfiguration('y_pose_robot1'),
                    'sdf_file': os.path.join(pkg_turtlebot3_gazebo, 'models', 'turtlebot3_waffle', 'robot1_model.sdf'),
                    # PASSAGGIO STATICO: Calcolato come stringa pura Python!
                    'bridge_params_file': os.path.join(pkg_turtlebot3_gazebo, 'params', 'robot1_bridge.yaml')
                }.items()
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_turtlebot3_gazebo, 'launch', 'robot_state_publisher.launch.py')),
                launch_arguments={
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'frame_prefix': PythonExpression(["'", "robot1", "'"])
                }.items()
            )
        ]
    )

    robot2_group = GroupAction(
        actions=[
            PushRosNamespace(
                PythonExpression(["'", "robot2", "'"])
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_turtlebot3_gazebo, 'launch', 'spawn_turtlebot3.launch.py')),
                launch_arguments={
                    'namespace': 'robot2',
                    'x_pose': LaunchConfiguration('x_pose_robot2'),
                    'y_pose': LaunchConfiguration('y_pose_robot2'),
                    'sdf_file': os.path.join(pkg_turtlebot3_gazebo, 'models', 'turtlebot3_waffle', 'robot2_model.sdf'),
                    'bridge_params_file': os.path.join(pkg_turtlebot3_gazebo, 'params', 'robot2_bridge.yaml')
                }.items()
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_turtlebot3_gazebo, 'launch', 'robot_state_publisher.launch.py')),
                launch_arguments={
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'frame_prefix': PythonExpression(["'", "robot2", "'"])
                }.items()
            )
        ]
    )

    robot3_group = GroupAction(
        actions=[
            PushRosNamespace(
                PythonExpression(["'", "robot3", "'"])
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_turtlebot3_gazebo, 'launch', 'spawn_turtlebot3.launch.py')),
                launch_arguments={
                    'namespace': 'robot3',
                    'x_pose': LaunchConfiguration('x_pose_robot3'),
                    'y_pose': LaunchConfiguration('y_pose_robot3'),
                    'sdf_file': os.path.join(pkg_turtlebot3_gazebo, 'models', 'turtlebot3_waffle', 'robot3_model.sdf'),
                    'bridge_params_file': os.path.join(pkg_turtlebot3_gazebo, 'params', 'robot3_bridge.yaml')
                }.items()
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_turtlebot3_gazebo, 'launch', 'robot_state_publisher.launch.py')),
                launch_arguments={
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'frame_prefix': PythonExpression(["'", "robot3", "'"])
                }.items()
            )
        ]
    )

    set_env_vars_resources = AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'models'))

    return LaunchDescription([
        declare_x_pose_arg_robot1,
        declare_y_pose_arg_robot1,
        declare_x_pose_arg_robot2,
        declare_y_pose_arg_robot2,
        declare_x_pose_arg_robot3,
        declare_y_pose_arg_robot3,
        declare_use_sim_time_arg,
        gz_sim_server,
        clock_bridge,
        robot1_group,
        robot2_group,
        robot3_group
    ])