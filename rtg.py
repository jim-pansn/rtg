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

    chars = all_chars[:num_chars] + ['_']
    if bipartite:
        chars2 = all_chars2[:num_chars] + ['_']
    else:
        chars2 = all_chars[:num_chars] + ['_']  

    keyboard = create_2d_keyboard(num_chars, q, beta)
    edges = []
    for _ in range(num_edges):
        edges.append(draw_edge(chars, chars2, keyboard,
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
def draw_edge(chars, chars2, keyboard, bipartite, self_loop):
    src_finished = False
    dst_finished = False
    src = ''
    dst = ''
    char_combi_without_underscore =  np.fromiter(it.product(chars[:-1], chars2[:-1]), 
                                dtype='1str,1str')
    small_keyboard = keyboard[:-1, :-1]
    small_keyboard = small_keyboard / small_keyboard.sum()
    src, dst = np.random.choice(char_combi_without_underscore, p=small_keyboard.flatten())
    
    char_combi = np.fromiter(it.product(chars, chars2), 
                                dtype='1str,1str')
    while not (src_finished and dst_finished):
        s, d = np.random.choice(char_combi, p=keyboard.flatten())
        if s == '_':
            src_finished = True
        if d == '_':
            dst_finished = True
        if not src_finished:
            src += s
        if not dst_finished:
            dst += d

    # if we produced a self loop but they are not allowed
    # we generate a new edge by running the whole function 
    # again
    #if(src == dst):
    #    print 'produced self loop'
    #if (src == '' or dst == ''):
    #    print 'src or dst empty'
    if ((not self_loop) and (src == dst)) or (src == '' or dst == ''):
        return draw_edge(chars, chars2, keyboard, bipartite, self_loop)
    else:
        return (src, dst)
