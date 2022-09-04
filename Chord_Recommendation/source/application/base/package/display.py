from ..configuration import NUMBER_OF_FLATS, EMPTY_FLAT
from .tools import InvertableMapping

class Display():

    @classmethod
    def for_fingerboard(cls, __strings, compositions, mode):
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

        for index in mode:
            string = __strings[index]

            flats = tuple(map(get_flat, string.nodes))
            notes = tuple(map(get_note, string.nodes))

            flat_note_mapping = InvertableMapping(flats, notes)
            
            print(f'[{index}]', end = '\t')
            for flat in range(NUMBER_OF_FLATS + 1):
                note = flat_note_mapping.map(flat)
                if flat in flats and note in compositions:
                    print(note, end = '\t')
                else:
                    print(EMPTY_FLAT, end = '\t')
            print()