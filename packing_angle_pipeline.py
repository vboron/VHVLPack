# *************************************************************************
# Import libraries
from dbm import _Database
from enum import Enum, auto
import os
import argparse
import utils
import NR
import shutil
import stat


# *************************************************************************
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


# *************************************************************************
def preprocessing(ds: Dataset):
    run_compile_angles(ds)
    run_find_VHVLres(ds)
    run_encode_4d(ds)

def run_compile_angles(ds: Dataset):
    utils.run_cmd(['./compile_angles.py', '--directory', ds.name, '--csv-file', f'{ds.name}_ang'], args.dry_run)

def run_find_VHVLres(ds: Dataset):
    utils.run_cmd(['./find_VHVLres.py', ds.name, f'{ds.name}_res'], args.dry_run)

def run_encode_4d(ds: Dataset):
    utils.run_cmd([f'{ds.name}_res.csv', f'{ds.name}_ang.csv', '4d.dat', f'{ds.name}_4d', f'{ds.name}'], args.dry_run)


# *************************************************************************
def run_nr(ds: Dataset, nr: NonRedundantization):
    if nr == NonRedundantization.NR1:
        NR.NR1(ds.name, '4d.dat', f'{ds.name}_{nr.name}', f'{ds.name}_4d.csv')
    elif nr == NonRedundantization.NR2:
        NR.NR2(f'{ds.name}_4d', '4d.dat', f'{ds.name}_{nr.name}')
    elif nr == NonRedundantization.NR3:
        NR.NR3(f'{ds.name}_4d', '4d.dat', f'{ds.name}_{nr.name}')
    else:
        src_path = os.path.join(ds.name, f'{ds.name}_4d.csv')
        dst_path = os.path.join(ds.name, f'{ds.name}_{nr.name}.csv')
        shutil.copyfile(src_path, dst_path)


# *************************************************************************
def run_papa(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./snns_run_and_compile_data.py', os.path.join(ds.name, 'seq_files'), '4d.dat',
                   f'{ds.name}_ang.csv', f'{ds.name}', 'papa'], args.dry_run)

def run_newpapa(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    with open(f'{ds.name}_{nr.name}_{meth.name}.arff', 'w') as f:
        utils.run_cmd(['csv2arff', '-norm', '-ni', 'in4d.dat', 'angle', f'{ds.name}_{nr.name}_4d.csv'],
                      args.dry_run, stdout=f)
    pat_path = os.path.join('SNNS', 'papa', 'training', 'final.pat')
    with open(pat_path) as f:
        utils.run_cmd(['arff2snns', f'{ds.name}_{nr.name}_{meth.name}.arff'], args.dry_run, stdout=f)

    utils.run_cmd(['batchman', '-f', 'final_training.cmd'], args.dry_run)

    install_path = os.path.join('SNNS', 'papa', 'training', 'install.sh')
    home_dir = os.environ['HOME']
    utils.run_cmd([f'./{install_path}', f'{home_dir}/{ds.name}_{nr.name}_{meth.name}'], args.dry_run)

    utils.run_cmd(['./snns_run_and_compile_data.py', os.path.join(ds.name, 'seq_files'), '4d.dat',
                   f'{ds.name}_ang.csv', f'{ds.name}', f'~/{ds.name}_{nr.name}_RetrainedPAPA/papa'],
                  args.dry_run)

def run_snns(ds: Dataset, meth: MLMethod):
    utils.run_cmd(['./pdb2seq.py', ds.name])
    # distinguish between making a new papa and running the old papa
    if meth == MLMethod.OrigPAPA:
        run_papa()
    elif meth == MLMethod.RetrainedPAPA:
        run_newpapa()

def run_MLP(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    # TODO Should we train/test on new/old data?
    utils.run_cmd(['./splitlines_csv2arff_MLP.py', ds.name, '4d.dat', f'{ds.name}_{nr.name}_4d.csv',
                   f'{ds.name}_{nr.name}_4d.csv', 'in4d.dat', ds.name], args.dry_run)
    utils.run_cmd(['./extract_data_from_logfiles.py', os.path.join(ds.name, 'testing_data'), 'graph.dat',
                   f'{ds.name}_{nr.name}'], args.dry_run)

# multilayer perceptron cross validation
def build_MLPxval_script(ds: Dataset, nr: NonRedundantization):
    temp = open('temp', 'wb')
    with open('runWekaMLP10FXval.sh', 'r') as f:
        for line in f:
            if line.startswith('DATA'):
                line = line.strip() + f'{ds.name}\n'
            temp.write(line)
    temp.close()
    name_for_script = f'Xval_{ds.name}_{nr.name}.sh'
    shutil.move('temp', os.path.join(ds.dataset, name_for_script))
    os.chmod(name_for_script, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP | stat.S_IWGRP)
    args = ['bash', name_for_script]
    print(f'Running {" ".join(args)}')
    utils.run_cmd([f'./{name_for_script}'], args.dry_run)

def MLPxval(ds: Dataset, nr: NonRedundantization):
    utils.run_cmd(['./split_10.py', f'{ds.name}_{nr.name}_4d.csv', '4d.dat', f'{ds.name}_{nr.name}_xval'], args.dry_run)
    #  create all of the outputs
    pass

def process(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cf: CorrectionFactor):
    unique_name = f"{ds.name}_{nr.name}_{meth.name}_{cf.name}"
    # print(f"Processing {unique_name} case")
    # NR.NR1(costam, costam, args.encoded_4d_cols_file)
    if cf == CorrectionFactor.Yes:
        # zrob ponownie costam
        pass


def postprocessing(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    # TODO
    pass

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--encoded-4d-cols-file', required=True)
args = parser.parse_args()

for ds in Dataset:
    preprocessing(ds)
    for nr in NonRedundantization:
        run_nr(ds, nr)
    for meth in MLMethod:
        for cf in CorrectionFactor:
            process(ds, nr, meth, cf)
