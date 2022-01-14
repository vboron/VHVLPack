from enum import Enum, auto
import argparse
import utils

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
    run_find_VHVLres(ds)
    run_encode_4d(ds)
    # TODO more things

def run_compile_angles(ds: Dataset):
    utils.run_cmd(['./compile_angles.py', '--directory', ds.name, '--csv-fil', f'{ds.name}_ang'], args.dry_run)

def run_find_VHVLres(ds: Dataset):
    utils.run_cmd(['./find_VHVLres.py', ds.name, f'{ds.name}_res'], args.dry_run)

def run_encode_4d(ds: Dataset):
    utils.run_cmd([f'{ds.name}_res', f'{ds.name}_ang', '4d.dat', f'{ds.name}_4d', f'{ds.name}'])

def process(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cf: CorrectionFactor):
    unique_name = f"{ds.name}_{nr.name}_{meth.name}_{cf.name}"
    # print(f"Processing {unique_name} case")
    # NR.NR1(costam, costam, args.encoded_4d_cols_file)
    if cf == CorrectionFactor.Yes:
        # zrob ponownie costam
        pass

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--encoded-4d-cols-file', required=True)
args = parser.parse_args()

for ds in Dataset:
    preprocessing(ds)
    for nr in NonRedundantization:
        for meth in MLMethod:
            for cf in CorrectionFactor:
                process(ds, nr, meth, cf)
