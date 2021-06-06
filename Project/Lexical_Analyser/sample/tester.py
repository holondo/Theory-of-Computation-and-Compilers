from TransitionTable import TransitionTable

x = TransitionTable('symbols.csv')
y = TransitionTable('TTable.csv')
print(y.transition(0, '>'))
print(y.transition(2, '<'))
print(y.transition(3, 'alpha'))

print(x.transition(0, 'Retorno'))
