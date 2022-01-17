from enum import Enum, auto
import os
import argparse
import utils

class Dataset(Enum):
    PrePAPA = auto()
    PostPAPA = auto()
    PreAF2 = auto()
    PostAF2 = auto()
    Everything = auto()

class NonRedundantization(Enum):
    NR0 = auto()
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

def run_compile_angles(ds: Dataset):
    utils.run_cmd(['./compile_angles.py', '--directory', ds.name, '--csv-fil', f'{ds.name}_ang'], args.dry_run)

def run_find_VHVLres(ds: Dataset):
    utils.run_cmd(['./find_VHVLres.py', ds.name, f'{ds.name}_res'], args.dry_run)

def run_encode_4d(ds: Dataset):
    utils.run_cmd([f'{ds.name}_res.csv', f'{ds.name}_ang.csv', '4d.dat', f'{ds.name}_4d', f'{ds.name}'])

def process(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cf: CorrectionFactor):
    unique_name = f"{ds.name}_{nr.name}_{meth.name}_{cf.name}"
    # print(f"Processing {unique_name} case")
    # NR.NR1(costam, costam, args.encoded_4d_cols_file)
    if cf == CorrectionFactor.Yes:
        # zrob ponownie costam
        pass

def run_papa(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./snns_run_and_compile_data.py', os.path.join(ds.name, 'seq_files'), '4d.dat', 
    f'{ds.name}_ang.csv', f'{ds.name}', 'papa'])

def run_newpapa(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['csv2arff', '-norm', '-ni', 'in4d.dat', 'angle', f'{ds.name}_{nr.name}_4d.csv', 
    f'> {ds.name}_{nr.name}_{meth.name}.arff'])
    pat_path = os.path.join('SNNS', 'papa', 'training', 'final.pat')
    utils.run_cmd(['arff2snns', f'{ds.name}_{nr.name}_{meth.name}.arff', f'> {pat_path}'])
    utils.run_cmd(['batchman', '-f', f'> {pat_path}'])
    install_path = os.path.join('SNNS', 'papa', 'training', 'install.sh')
    utils.run_cmd([f'./{install_path}', f'$HOME/{ds.name}_{nr.name}_{meth.name}'])
    utils.run_cmd(['./snns_run_and_compile_data.py', os.path.join(ds.name, 'seq_files'), '4d.dat', 
    f'{ds.name}_ang.csv', f'{ds.name}', f'~/{ds.name}_{nr.name}_{'RetrainedPAPA'}/papa'])

def run_snns(ds: Dataset):
    utils.run_cmd(['./pdb2seq.py', ds.name])
    if ds.name == 'OrigPAPA':
        run_papa()
    elif ds.name == 'RetrainedPAPA':
        run_newpapa()
    # distinguish between making a new papa and running the old papa

def run_MLP(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./splitlines_csv2arff_MLP.py', ds.name, '4d.dat', f'{ds.name}_{nr.name}_4d.csv',
    -----test-on-the-opposite---, 'in4d.dat', ds.name])
    utils.run_cmd(['./extract_data_from_logfiles.py', os.path.join(ds.name, 'testing_data'), 'graph.dat',
    f'{ds.name}_{nr.name}'])

def MLPxval(ds: Dataset, nr: NonRedundantization):
     
def postprocessing(ds: Dataset, nr: NonRedundantization, meth: MLMethod):

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
