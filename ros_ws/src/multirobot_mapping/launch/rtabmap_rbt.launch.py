import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    namespace = LaunchConfiguration('namespace', default='robot1')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='robot1'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            namespace=namespace,
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                
                # 1. Sincronizzazione flessibile (Obbligatorio per Gazebo)
                'approx_sync': True,
                'queue_size': 30,

                # 3. Decimazione della PointCloud (Il salvavita)
                'Grid/DepthDecimation': '4', # Prende 1 punto ogni 4, abbattendo il carico del 90%
                'Grid/MaxObstacleHeight': '1.5', # Ignora il soffitto della stanza
                'Grid/MinClusterSize': '20', # Filtra il rumore visivo

                # Sostituite le f-string con PathJoinSubstitution per risolvere l'oggetto LaunchConfiguration
                'frame_id': PathJoinSubstitution([namespace, 'base_footprint']),
                'odom_frame_id': PathJoinSubstitution([namespace, 'odom']),
                'map_frame_id': PathJoinSubstitution([namespace, 'map']),
                
                'subscribe_depth': False,
                'subscribe_rgb': False,
                'subscribe_scan': False,
                'subscribe_rgbd': False,
                'subscribe_stereo' : False,
                
                # Abilitiamo la sottoscrizione diretta alla PointCloud2
                'subscribe_scan_cloud': True,
                
                # Ottimizzazioni per la simulazione (Evita lag eccessivo)
                'RGBD/Enabled': 'false', 
                'Reg/Strategy': '1',
                'Rtabmap/DetectionRate': '1.0', # Aggiorna la mappa 1 volta al secondo (riduce CPU)
                'RGBD/ProximityBySpace': 'true',
                'RGBD/AngularUpdate': '0.0',
                'RGBD/LinearUpdate': '0.0',
                'Mem/IncrementalMemory': 'true', # true = SLAM (mappa e localizza), false = solo localizzazione
            }],
            remappings=[
                ('scan_cloud', 'stereo_camera/pointCloud'),
                ('tf', '/tf'),
                ('tf_static', '/tf_static')
            ],
            arguments=['-d'] # Cancella il database precedente ad ogni avvio (utile nei test)
        )
    ])