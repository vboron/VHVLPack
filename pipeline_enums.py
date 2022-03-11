from enum import Enum, auto

class Dataset(Enum):
    PrePAPA = auto()
    PostPAPA = auto()
    PreAF2 = auto()
    PostAF2 = auto()
    # Everything = auto()


class NonRedundantization(Enum):
    NR0 = auto()
    NR1 = auto()
    NR2 = auto()
    NR3 = auto()


class MLMethod(Enum):
    # OrigPAPA = auto()
    # RetrainedPAPA = auto()
    WekaMLP = auto()
    # XvalWeka = auto()
    SklearnMLPReg = auto()
    SklearnGBReg = auto()

class Correction(Enum):
    NotCorrected = auto()
    Corrected = auto()


def unique_name(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cr: Correction):
    return f'{ds.name}_{nr.name}_{meth.name}_{cr.name}'

class TestTrain:
    def __init__(self, training, testing):
        self.training = training
        self.testing = testing

def get_all_testtrain():
    papa = TestTrain(training=Dataset.PrePAPA, testing=Dataset.PostPAPA)
    af2 = TestTrain(training=Dataset.PreAF2, testing=Dataset.PostAF2)
    # everything = TestTrain(training=Dataset.Everything, testing=Dataset.Everything)

    # return [papa]
    # return [af2]
    # return [af2, everything]
    return [papa, af2]
    # return [papa, af2, everything]

def get_training_from_testing(testing: Dataset):
    for tt in get_all_testtrain():
        if tt.testing == testing:
            return tt.training
    raise ValueError(f'Could not get training out of testing={testing}')