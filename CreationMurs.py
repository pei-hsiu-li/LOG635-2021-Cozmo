import cozmo
from cozmo.util import degrees, Pose

WALL_HEIGHT = 50
WALL_WIDTH = 10


# exemple de comment créer des murs virtuels
def create_walls(robot: cozmo.robot.Robot):
    """
    Fonction de création des murs selon l'environement désiré
    @param robot: le robot cozmo
    """
    # --- HORIZONTAL ---
    wall1 = Pose(450, 295, 0, angle_z=degrees(0))
    wall1 = robot.world.create_custom_fixed_object(
        wall1, WALL_WIDTH, 590, WALL_HEIGHT, relative_to_robot=False)
    # wall2 = Pose(270, 150, 0, angle_z=degrees(0))
    # wall2 = robot.world.create_custom_fixed_object(
    #     wall2, WALL_WIDTH, 40, WALL_HEIGHT, relative_to_robot=False)
    wall3 = Pose(180, 510, 0, angle_z=degrees(0))
    wall3 = robot.world.create_custom_fixed_object(
        wall3, WALL_WIDTH, 160, WALL_HEIGHT, relative_to_robot=False)
    wall4 = Pose(0, 295, 0, angle_z=degrees(0))
    wall4 = robot.world.create_custom_fixed_object(
        wall4, WALL_WIDTH, 590, WALL_HEIGHT, relative_to_robot=False)

    # --- VERTICAL ---
    wall5 = Pose(370, 0, 0, angle_z=degrees(0))
    wall5 = robot.world.create_custom_fixed_object(
        wall5, 160, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
    wall6 = Pose(390, 170, 0, angle_z=degrees(0))
    wall6 = robot.world.create_custom_fixed_object(
        wall6, 120, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
    wall7 = Pose(400, 330, 0, angle_z=degrees(0))
    wall7 = robot.world.create_custom_fixed_object(
        wall7, 100, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
    wall8 = Pose(225, 590, 0, angle_z=degrees(0))
    wall8 = robot.world.create_custom_fixed_object(
        wall8, 450, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
    wall9 = Pose(35, 360, 0, angle_z=degrees(0))
    wall9 = robot.world.create_custom_fixed_object(
        wall9, 70, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
    wall10 = Pose(50, 230, 0, angle_z=degrees(0))
    wall10 = robot.world.create_custom_fixed_object(
        wall10, 100, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
    wall11 = Pose(60, 100, 0, angle_z=degrees(0))
    wall11 = robot.world.create_custom_fixed_object(
        wall11, 120, WALL_WIDTH, WALL_HEIGHT, relative_to_robot=False)
