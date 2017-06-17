#!/usr/bin/env python

import datetime

from .minmax import min_max, US
start = datetime.datetime.now()
print start
a = min_max(debug=False)
# print "State"
# print a.get_state()
# print "Is Complete"
# print a.is_complete(a.get_state())
# print "Utility"
# print a.get_utility(a.get_state())
# print "Get Successors"
#
# print [a.get_successors(a.get_state(), x, None, None)
#        for x in a.get_state().items() if 'you' in x[1]]
#
# print "Get Path"
#
# for y in [a.get_successors(a.get_state(), x, None, None)
#           for x in a.get_state().items() if 'you' in x[1]]:
#     for z in y:
#         if z:
#             print z
#             print z.path
#             print z.utility
#             print z.board
print "Build tree"
tree = a.build_tree(a.get_state(), target=US, parent=None, levels=2)
sec_start = datetime.datetime.now()
print sec_start
print tree


def dump_children(move, count):
    print "Next level", count
    print move
    print move.board
    print move.parent
    print move.get_root()
    print move.path
    print move.utility
    new_count = count + 1
    for child in move.children:
        for sec_move in child:
            dump_children(sec_move, new_count)

for child in tree.children:
    print "#########################"
    print "##        CHILD        ##"
    print "#########################"
    for move in child:
        dump_children(move, 1)
finish = datetime.datetime.now()
print finish
print finish - start
print "Test ends"
