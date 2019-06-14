import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    name = 'image'
    num_frames = 1

    n = False
    f = False
    v = False

    for command in commands:
        c = command['op']
        args = command['args']
        if c == "basename":
            name = args[0]
            n = True
        if c == "frames":
            num_frames = args[0]
            f = True
        elif c == "vary":
            v = True

    if v and not f:
        exit()

    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [ {} for i in range(int(num_frames)) ]
    for command in commands:
        c = command['op']
        args = command['args']
        if c == "vary":
            knob = command['knob']
            for i in range(int(args[0]),int(args[1])+1):
                frames[i][knob] = (args[3] - args[2]) * (i - args[0]) / (args[1] - args[0]) + args[2]
    return frames

def get_lights(commands):
    lights = {}
    for command in commands:
        c = command['op']
        args = command['args']
        if c == 'light':
            lights[command[c]] = [args[0],args[1],args[2],args[3],args[4],args[5]]
    print lights
    return lights


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    lights = get_lights(commands)
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)

    for i in range(int(num_frames)):
        print i
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []

        for command in commands:
            c = command['op']
            args = command['args']
            knob_value = 1
            if 'knob' in command.keys() and command['knob'] != None:
                try:
                    knob_value = frames[i][command['knob']]
                except:
                    continue
            if c == 'mesh':
                if command["constants"]:
                    reflect = command['constants']
                add_mesh(tmp, args[0])
                matrix_mult(stack[-1],tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'box':
                try:
                    if command['constants']:
                        reflect = command['constants']
                    add_box(tmp,
                            knob_value * args[0], knob_value * args[1], knob_value * args[2],
                            knob_value * args[3], knob_value * args[4], knob_value * args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                    tmp = []
                    reflect = '.white'
                except:
                    continue
            elif c == 'sphere':
                try:
                    if command['constants']:
                        reflect = command['constants']
                    add_sphere(tmp,
                               knob_value * args[0], knob_value * args[1], knob_value * args[2], knob_value * args[3], step_3d)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                    tmp = []
                    reflect = '.white'
                except:
                    continue
            elif c == 'torus':
                try:
                    if command['constants']:
                        reflect = command['constants']
                    add_torus(tmp,
                              knob_value * args[0], knob_value * args[1], knob_value * args[2], knob_value * args[3], knob_value * args[4], step_3d)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                    tmp = []
                    reflect = '.white'
                except:
                    continue
            elif c == 'line':
                try:
                    add_edge(tmp,
                             knob_value * args[0], knob_value * args[1], knob_value * args[2], knob_value * args[3], knob_value * args[4], knob_value * args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_lines(tmp, screen, zbuffer, color)
                    tmp = []
                except:
                    continue
            elif c == 'move':
                try:
                    tmp = make_translate(knob_value * args[0], knob_value * args[1], knob_value * args[2])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                except:
                    continue
            elif c == 'scale':
                try:
                    tmp = make_scale(knob_value * args[0], knob_value * args[1], knob_value * args[2])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                except:
                    continue
            elif c == 'rotate':
                try:
                    theta = knob_value * args[1] * (math.pi/180)
                    if args[0] == 'x':
                        tmp = make_rotX(theta)
                    elif args[0] == 'y':
                        tmp = make_rotY(theta)
                    else:
                        tmp = make_rotZ(theta)
                    matrix_mult( stack[-1], tmp )
                    stack[-1] = [ x[:] for x in tmp]
                    tmp = []
                except:
                    continue
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
        save_extension(screen, "./anim/"+name + ("0000"+str(i))[-4:])
    make_animation(name)
        # end operation loop
