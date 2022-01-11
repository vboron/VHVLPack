from enum import Enum, auto
import subprocess
import argparse

class Dataset(Enum):
    PrePAPA = auto()
    PostPAPA = auto()
    PreAF2 = auto()
    PostAF2 = auto()
    Everything = auto()

class NonRedundantization(Enum):
    No = auto()
    NR1 = auto()
    NR2 = auto()
    NR3 = auto()

class MLMethod(Enum):
    OrigPAPA = auto()
    RetrainedPAPA = auto()
    WekaMLP = auto()
    XvalWeka = auto()

class CorrectionFactor(Enum):
    Yes = auto()
    No = auto()

def preprocessing(ds: Dataset):
    run_compile_angles(ds)
    # TODO more things

def run_compile_angles(ds: Dataset):
    cmd = ['./compile_angles.py', '--directory', ds.name, '--csv-file', f'{ds.name}_ang']
    print(f"Running {cmd}")
    if not args.dry_run:
        subprocess.run(cmd)

def process(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cf: CorrectionFactor):
    unique_name = f"{ds.name}_{nr.name}_{meth.name}_{cf.name}"
    # print(f"Processing {unique_name} case")

    if cf == CorrectionFactor.Yes:
        # zrob ponownie costam
        pass

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()

for ds in Dataset:
    preprocessing(ds)
    for nr in NonRedundantization:
        for meth in MLMethod:
            for cf in CorrectionFactor:
                process(ds, nr, meth, cf)