import numpy as np
import itertools as it

def rtg(num_edges, num_chars, beta, q, num_timeticks,
                         bipartite=False, self_loop=False):

    # TODO: check all inputs
    if num_chars > 26:
        raise Error('Number of characters cannot be greater than 26')

    all_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
                 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    all_chars2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                  'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    chars = all_chars[:num_chars] + ['#']
    if bipartite:
        chars2 = all_chars2[:num_chars] + ['$']
    else:
        chars2 = all_chars[:num_chars] + ['#']  

    keyboard = create_2d_keyboard(num_chars, q, beta)
    edges = []
    for _ in range(num_edges):
        edges.append(create_edge(chars, chars2, keyboard,
                        bipartite, self_loop))
    return edges


def create_2d_keyboard(num_chars, q, beta):
    # assign unequal probabilities to the keys
    p = np.zeros(num_chars + 1)
    p_remaining = 1 - q
    for i in range(num_chars - 1):
        p[i] = np.random.rand() * p_remaining
        p_remaining -= p[i]
    p[num_chars - 1] = p_remaining
    # last key is the seperator
    p[num_chars] = q

    # init the keyboard with indipendant cross product probs 
    keyboard = np.outer(p, p)
    # multiply the imbalance factor
    keyboard = keyboard * beta
    # set diagonal to 0
    np.fill_diagonal(keyboard, 0) 
    # calculate remaining probabilities for the diagonal
    # such that each row and column sums up to the 
    # marginal probability
    remaining_diag = p - keyboard.sum(axis=0)
    dia_idx = np.diag_indices_from(keyboard)
    keyboard[dia_idx] = remaining_diag

    return keyboard

    
# TODO: add timestamp
def create_edge(chars, chars2, keyboard, bipartite, self_loop):
    src_finished = False
    dst_finished = False
    src = ''
    dst = ''
    char_combi = np.fromiter(it.product(chars, chars2), 
                                dtype='1str,1str')    
    
    if not self_loop and not bipartite:
        # for the first try the key that produces a selfloop
        # on the delimeter is permitted (to reduce the number 
        # of selfloops)
        first_try_keyboard = np.copy(keyboard)
        first_try_keyboard[-1, -1] = 0
        first_try_keyboard = first_try_keyboard / first_try_keyboard.sum()
        src, dst = np.random.choice(char_combi, p=first_try_keyboard.flatten())
        if src == '#':
            src_finished = True
        if dst == '#' or dst == '$':
            dst_finished = True
    
    
    while not (src_finished and dst_finished):
        s, d = np.random.choice(char_combi, p=keyboard.flatten())
        if not src_finished:
            src += s
        if not dst_finished:
            dst += d
        if s == '#':
            src_finished = True
        if d == '#' or d == '$':
            dst_finished = True

    # if we produced a self loop but they are not allowed
    # we generate a new edge by running the whole function 
    # again
    if ((not self_loop) and (src == dst)):
        return create_edge(chars, chars2, keyboard, bipartite, self_loop)
    else:
        return (src, dst)
