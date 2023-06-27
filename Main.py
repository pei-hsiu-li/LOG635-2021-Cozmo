import cozmo
from crime_inference import CrimeInference as ci
from cozmo.util import degrees, Pose, Distance, Speed
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes, LightCube, LightCube1Id, LightCube2Id, LightCube3Id
import time
from datetime import datetime
import CreationMurs

keepGoing = True
cube_taps = 0
start_time = time.time()

stop_origine = Pose(0, 0, 0, angle_z=degrees(180))
stop_manger = Pose(250, 80, 0, angle_z=degrees(0))
stop_chambre = Pose(330, 250, 0, angle_z=degrees(0))
stop_salon = Pose(310, 430, 0, angle_z=degrees(90))
stop_bain = Pose(120, 430, 0, angle_z=degrees(90))
stop_cuisine = Pose(70, 300, 0, angle_z=degrees(180))
stop_garage = Pose(80, 160, 0, angle_z=degrees(180))

agent = ci()


def questions_communes():
    """
    Fonction qui sera répétée par le robot dans toutes les chambres où il ne voit pas la victime
    A la fin, le robot sait où il est, qui est avec lui et quelle arme est dans la pièce
    """
    piece = input('Je suis ou? ')
    personne = input('Qui est la? ')
    arme = input('Quelle arme est dans la piece? ')

    personne_piece = "{name} est dans le {piece}".format(name=personne, piece=piece)
    personne_piece_passe = "{name} était dans le {piece}".format(name=personne, piece=piece)
    arme_piece = "le {arme} est dans le {piece}".format(arme=arme, piece=piece)
    personne_vivant = "{name} est vivant".format(name=personne)

    uneHeureApres = agent.get_crime_hour() + 1

    agent.add_clause(ci.to_fol([personne_vivant], 'grammars/personne_vivant.fcfg'))
    agent.add_clause(ci.to_fol([personne_piece], 'grammars/personne_piece.fcfg'))
    agent.add_clause(ci.to_fol([personne_piece_passe + ' à ' + str(uneHeureApres) + 'h'], 'grammars/personne_piece_heure.fcfg'))
    agent.add_clause(ci.to_fol([arme_piece], 'grammars/arme_piece.fcfg'))


def questions_victime():
    """
    Fonction qui sera appeler lorsque le robot voit la victime
    A la fin, le robot sait où il est et quelle arme est dans la pièce
    Le robot va aussi savoir qui est la victime et comment il est mort
    """
    piece = input('Je suis ou? ')
    victime = input('Qui est mort? ')
    indice = input('Indice sur le corps? ')
    arme = input('Quelle arme est dans la piece? ')

    indice = (indice.replace('la personne', victime))
    personne_morte = "{name} est mort".format(name=victime)
    personne_piece = "{name} est dans le {piece}".format(name=victime, piece=piece)
    arme_piece = "le {arme} est dans le {piece}".format(arme=arme, piece=piece)

    agent.add_clause(ci.to_fol([personne_piece], 'grammars/personne_piece.fcfg'))
    agent.add_clause(ci.to_fol([personne_morte], 'grammars/personne_morte.fcfg'))
    agent.add_clause(ci.to_fol([indice], 'grammars/personne_poignarde.fcfg'))
    agent.add_clause(ci.to_fol([arme_piece], 'grammars/arme_piece.fcfg'))


def clauses_debut():
    """
    Fonction qui lit le fichier facts.txt qui contient les clauses de départ
    """
    file1 = open('facts.txt', 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        print("Line{}: {}".format(count, line.strip()))
        if 'mort' in line:
            agent.add_clause(ci.to_fol([line], 'grammars/personne_morte_heure.fcfg'))
        else:
            agent.add_clause(ci.to_fol([line], 'grammars/personne_piece_heure.fcfg'))


def handle_object_tapped(evt, **kw):
    """
    Fonction handle qui détecte lorsqu'on tape sur un cube
    @param evt: event
    @param kw: kwargs
    """
    global keepGoing
    global cube_taps
    global start_time

    print('in handle')
    # This will be called whenever an EvtObjectMovingStarted event is dispatched -
    # whenever we detect a cube starts moving (via an accelerometer in the cube)
    i = evt.obj.object_id
    print(i)
    if i == 2:
        if cube_taps == 0:
            start_time = time.time()
        cube_taps = cube_taps + 1


def cozmo_lights(robot: cozmo.robot.Robot):
    """
    focntion d'initialisation des cubes en leurs assigants une couleur respective
    @param robot: robot cozmo
    @return: return les 3 cubes
    """
    # looks like a paperclip
    cube1 = robot.world.get_light_cube(LightCube1Id)

    # looks like a lamp / heart
    cube2 = robot.world.get_light_cube(LightCube2Id)

    # looks like the letters 'ab' over 'T'
    cube3 = robot.world.get_light_cube(LightCube3Id)
    if cube1 is not None:
        cube1.set_lights(cozmo.lights.red_light)
    else:
        cozmo.logger.warning("LightCube1Id cube is not connected - check the battery.")

    if cube2 is not None:
        cube2.set_lights(cozmo.lights.green_light)
    else:
        cozmo.logger.warning("LightCube2Id cube is not connected - check the battery.")

    if cube3 is not None:
        cube3.set_lights(cozmo.lights.blue_light)
    else:
        cozmo.logger.warning("LightCube3Id cube is not connected - check the battery.")
    return cube1, cube2, cube3


def answer_with_tap():
    """
    Fonction qui détecte une réponse oui ou non avec le nombre de tap sur le cube
    @return: True  ou False selon la réponse
    """
    global keepGoing
    global start_time
    global cube_taps
    while keepGoing:
        if(time.time() - start_time >= 3 and cube_taps > 0):
            if cube_taps == 1:
                print("Oui")
                return True
            elif cube_taps == 2:
                print("Non")
                return False
            else:
                print("Peut-etre")
                return False
            cube_taps = 0

        time.sleep(0.1)


# Petit programme qui visite toutes les pièces de l'exemple
def cozmo_program(robot: cozmo.robot.Robot):
    """
    Fonction principale du programme qui execute une série d'actions et arrive à une conclusion
    sur le meurtrier
    @param robot: robot cozmo
    """
    robot.world.delete_all_custom_objects()
    print(robot.pose.position)
    CreationMurs.create_walls(robot)
    cube1, cube2, cube3 = cozmo_lights(robot)

    global keepGoing
    global start_time
    global cube_taps
    # Add event handlers that will be called for the corresponding event
    robot.add_event_handler(cozmo.objects.EvtObjectTapped, handle_object_tapped)

    robot.set_lift_height(0).wait_for_completed()
    time.sleep(1)

    obj1Cube = robot.world.define_custom_cube(CustomObjectTypes.CustomType00, CustomObjectMarkers.Circles2, 40, 40, 40, is_unique=True)

    obj2Cube = robot.world.define_custom_cube(CustomObjectTypes.CustomType01, CustomObjectMarkers.Diamonds3, 40, 40, 40, is_unique=True)

    obj3Cube = robot.world.define_custom_cube(CustomObjectTypes.CustomType02, CustomObjectMarkers.Circles3, 40, 40, 40, is_unique=True)

    obj4Cube = robot.world.define_custom_cube(CustomObjectTypes.CustomType03, CustomObjectMarkers.Triangles5, 40, 40, 40, is_unique=True)

    obj5Cube = robot.world.define_custom_cube(CustomObjectTypes.CustomType04, CustomObjectMarkers.Circles5, 40, 40, 40, is_unique=True)

    obj6Cube = robot.world.define_custom_cube(CustomObjectTypes.CustomType05, CustomObjectMarkers.Triangles2, 40, 40, 40, is_unique=True)

    if (obj1Cube is not None):
        print("All objects defined successfully!")
    else:
        print("One or more object definitions failed!")
        return
    
    robot.say_text('Do I start?').wait_for_completed()
    print(start_time)
    start_time = time.time()
    print(start_time)
    if answer_with_tap():
        print("starting")
        robot.say_text('starting').wait_for_completed()
    else:
        robot.say_text('goodbye').wait_for_completed()
        exit()

    batt = robot.battery_voltage
    print( "COZMO BATTERY: " + str(batt) )

    clauses_debut()
    uneHeureApres = agent.get_crime_hour() + 1
    agent.add_clause('UneHeureApresCrime({})'.format(uneHeureApres))
    
    robot.go_to_pose(stop_manger, relative_to_robot=False).wait_for_completed()
    obj = robot.world.wait_until_observe_num_objects(1, object_type=LightCube)
    print(obj)
    questions_communes()

    robot.go_to_pose(stop_chambre, relative_to_robot=False).wait_for_completed()
    obj = robot.world.wait_until_observe_num_objects(1, object_type=CustomObject)
    print(obj)
    questions_communes()

    robot.go_to_pose(stop_salon, relative_to_robot=False).wait_for_completed()
    time.sleep(1)
    obj = robot.world.wait_until_observe_num_objects(1, object_type=LightCube)
    print(obj)
    # robot.run_timed_behavior(cozmo.behavior.BehaviorTypes.RollBlock, active_time=15)
    robot.roll_cube(cube3).wait_for_completed()
    robot.set_lift_height(0).wait_for_completed()
    questions_victime()

    robot.go_to_pose(stop_bain, relative_to_robot=False).wait_for_completed()
    obj = robot.world.wait_until_observe_num_objects(1, object_type=CustomObject)
    print(obj)
    questions_communes()

    robot.go_to_pose(stop_cuisine, relative_to_robot=False).wait_for_completed()
    obj = robot.world.wait_until_observe_num_objects(1, object_type=CustomObject)
    print(obj)
    questions_communes()

    robot.go_to_pose(stop_garage, relative_to_robot=False).wait_for_completed()
    obj = robot.world.wait_until_observe_num_objects(1, object_type=CustomObject)
    print(obj)
    questions_communes()

    batt = robot.battery_voltage
    print( "COZMO BATTERY: " + str(batt) )

    # Conclusions
    print("Pièce du crime : ", agent.get_crime_room())
    print("Arme du crime : ", agent.get_crime_weapon())
    print("Personne victime : ", agent.get_victim())
    print("Heure du crime : ", agent.get_crime_hour())
    meurtrier = agent.get_suspect()
    print("Meurtrier : ", meurtrier)
    print("Personnes innocentes : ", agent.get_innocent())

    dist = Distance(distance_mm=20)
    time.sleep(3)
    robot.set_lift_height(1).wait_for_completed()
    robot.go_to_object(cube1, dist).wait_for_completed()
    robot.say_text('Do I bring him in?').wait_for_completed()
    keepGoing = True
    cube_taps = 0
    start_time = time.time()
    if answer_with_tap():
        print("tapping")
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTapCube).wait_for_completed()
        robot.drive_straight(Distance(distance_mm=-100), Speed(speed_mmps=50)).wait_for_completed()
        robot.pickup_object(cube1, num_retries=3).wait_for_completed()
        robot.go_to_pose(stop_origine, relative_to_robot=False).wait_for_completed()
    else:
        robot.say_text('Failed').wait_for_completed()
    


cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)