from ..configuration import NUMBER_OF_FLATS

class Display():

    @classmethod
    def for_fingerboard(cls, __strings):
        '''
        ---Sample----------------------------------------------------------------------------------------
        E       F               G               A               B       C               D               E
        A               B       C               D               E       F               G               A
        D               E       F               G               A               B       C               D
        G               A               B       C               D               E       F               G
        B       C               D               E       F               G               A               B
        E       F               G               A               B       C               D               E
        -------------------------------------------------------------------------------------------------
        '''
        def get_flat(node): return node.flat
        def get_note(node): return node.note

        for string in __strings:

            flats = tuple(map(get_flat, string.nodes))
            notes = tuple(map(get_note, string.nodes))

            mapping = {flat: note for flat, note in zip(flats,
                                                        notes)}

            for flat in range(NUMBER_OF_FLATS + 1):
                if flat in flats: print(mapping[flat], end = '\t')
                else: print(' ', end = '\t')
            print()