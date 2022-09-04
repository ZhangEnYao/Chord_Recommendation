if __name__=='__main__':
    from base.data_structure import Guitar
else:
    from .base.data_structure import Guitar


normal_guitar = Guitar()
ShowFingerBoard = normal_guitar.show_fingerboard