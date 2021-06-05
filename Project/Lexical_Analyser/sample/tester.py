import sys
from TransitionTable import TransitionTable
from TransitionTable import TransitionPd

x = TransitionTable()
y = TransitionPd()
print(x.transition(0, '>'))
print(y.transition(0, '>'))
