from enum import Enum, auto

class Dataset(Enum):
    PrePAPA = auto()
    # PostPAPA = auto()
    # PreAF2 = auto()
    PostAF2 = auto()
    # Everything = auto()


class NonRedundantization(Enum):
    NR0 = auto()
    NR1 = auto()
    NR2 = auto()
    NR3 = auto()


class MLMethod(Enum):
    OrigPAPA = auto()
    # RetrainedPAPA = auto()
    # WekaMLP = auto()
    # XvalWeka = auto()

def unique_name(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    return f'{ds.name}_{nr.name}_{meth.name}'