
def create_rings():
    from .private import PrivateRingEntry
    from .public import PublicRingEntry
    from .ring import Ring

    return Ring[PrivateRingEntry](), Ring[PublicRingEntry]()


PrivateRing, PublicRing = create_rings()
