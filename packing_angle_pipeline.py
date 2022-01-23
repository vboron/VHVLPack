#!/usr/bin/python3
# # *************************************************************************
from enum import Enum, auto
import os
import argparse
import utils
import nonred
import shutil


# *************************************************************************
class Dataset(Enum):
    PrePAPA = auto()
    # PostPAPA = auto()
    # PreAF2 = auto()
    # PostAF2 = auto()
    # Everything = auto()

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


# *************************************************************************
def preprocessing(ds: Dataset):
    def run_compile_angles(ds: Dataset):
        utils.run_cmd(['./compile_angles.py', '--directory', ds.name, '--csv_output', f'{ds.name}_ang'], args.dry_run)
    def run_find_VHVLres(ds: Dataset):
        utils.run_cmd(['./find_VHVLres.py','--directory', ds.name,'--csv_output', f'{ds.name}_res'], args.dry_run)
    def run_encode_4d(ds: Dataset):
        utils.run_cmd(['./encode_4d.py', '--residue_csv', f'{ds.name}_res.csv', '--angle_csv', f'{ds.name}_ang.csv',
                    '--columns', args.cols_4d, '--csv_output', f'{ds.name}_4d', '--directory', f'{ds.name}'], args.dry_run)
    run_compile_angles(ds)
    run_find_VHVLres(ds)
    run_encode_4d(ds)


# *************************************************************************
def run_nr(ds: Dataset, nr: NonRedundantization):
    encoded_csv_path = os.path.join(ds.name, f'{ds.name}_4d.csv')
    new_file = f'{ds.name}_{nr.name}_4d'
    if nr == NonRedundantization.NR0:
        src_path = os.path.join(ds.name, f'{ds.name}_4d.csv')
        dst_path = os.path.join(ds.name, f'{new_file}.csv')
        shutil.copyfile(src_path, dst_path)
    elif nr == NonRedundantization.NR1:
        nonred.NR1(ds.name, args.cols_4d, new_file, encoded_csv_path)
    elif nr == NonRedundantization.NR2:
        nonred.NR2(encoded_csv_path, args.cols_4d, ds.name, new_file)
    elif nr == NonRedundantization.NR3:
        nonred.NR3(encoded_csv_path, args.cols_4d, ds.name, new_file)


# *************************************************************************
def run_papa(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./snns_run_and_compile_data.py', '--directory', ds.name, '--seq_directory', os.path.join(ds.name,
                   'seq_files'), '--angle_csv', f'{ds.name}_ang.csv', '--which_papa', 'papa', '--csv_output',
                   f'{ds.name}_{nr.name}_{meth.name}'], args.dry_run)

def run_newpapa(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    with open(f'{ds.name}/{ds.name}_{nr.name}_{meth.name}.arff', 'w') as f:
        path = os.path.join(ds.name, f'{ds.name}_{nr.name}_4d.csv')
        utils.run_cmd(['csv2arff', '-norm', '-ni', 'in4d.dat', 'angle', path],
                      args.dry_run, stdout=f)
    pat_path = os.path.join('SNNS', 'papa', 'training', 'final.pat')
    with open(pat_path) as f:
        utils.run_cmd(['arff2snns', f'{ds.name}/{ds.name}_{nr.name}_{meth.name}.arff'], args.dry_run, stdout=f)

    utils.run_cmd(['batchman', '-f', 'SNNS/papa/training/final_training.cmd'], args.dry_run)

    install_path = os.path.join('SNNS', 'papa', 'training', 'install.sh')
    home_dir = os.environ['HOME']
    utils.run_cmd([f'./{install_path}', f'{home_dir}/{ds.name}_{nr.name}_{meth.name}'], args.dry_run)

    utils.run_cmd(['./snns_run_and_compile_data.py', '--directory', {ds.name}, '--seq_directory',
                   os.path.join(ds.name, 'seq_files'), '--angle_csv', f'{ds.name}_ang.csv', '--csv_output',
                   f'{ds.name}_{nr.name}_{meth.name}', '--which_papa', f'~/{ds.name}_{nr.name}_{meth.name}/papa'],
                  args.dry_run)

def run_snns(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./pdb2seq.py', ds.name], args.dry_run)
    # distinguish between making a new papa and running the old papa
    if meth == MLMethod.OrigPAPA:
        run_papa(ds, nr, meth)
    elif meth == MLMethod.RetrainedPAPA:
        run_newpapa(ds, nr, meth)
    else:
        raise ValueError(f'Handling of meth={meth} not implemented')

def run_MLP(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./splitlines_csv2arff_MLP.py', '--directory', ds.name, '--columns_4d', args.cols_4d, '--training_csv',
                   f'{ds.name}_{nr.name}_4d.csv', '--testing_csv', f'{ds.name}_{nr.name}_4d.csv', '--input_cols',
                   'in4d.dat', ds.name], args.dry_run)
    utils.run_cmd(['./extract_data_from_logfiles.py', '--directory', os.path.join(ds.name, 'testing_data'),
                   '--columns_postprocessing', 'post_processing.dat', '--output_name',
                   f'{ds.name}_{nr.name}_{meth.name}'], args.dry_run)

# multilayer perceptron cross validation
def run_MLPxval(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./split_10.py', '--input_csv', f'{ds.name}_{nr.name}_4d.csv', '--columns', args.cols_4d,
                   '--directory', ds.name, '--output_tag', f'{nr.name}'], args.dry_run)

    classifier='weka.classifiers.functions.MultilayerPerceptron'
    env = {'WEKA': '/usr/local/apps/weka-3-8-3'}
    env['CLASSPATH'] = f'{env["WEKA"]}/weka.jar'
    for i in range (1, 11):
        # train
        with open(os.path.join(ds.name, f'{nr.name}_{i}_train.log'), 'w') as f:
            cmd = ['java', classifier, '-v', '-x', 10, '-t', os.path.join(ds.name, f'{nr.name}_{i}_train.arff'),
                '-d', os.path.join(ds.name, f'{nr.name}_fold_{i}.model')]
            utils.run_cmd(cmd, args.dry_run, stdout=f, env=env)
        # test
        with open(os.path.join(ds.name, f'{nr.name}_{i}_test.log')) as f:
            cmd = ['java', classifier, '-v', '-o', '-T', os.path.join(ds.name, f'{nr.name}_{i}_test.arff'), '-l',
                   os.path.join(ds.name, f'{nr.name}_fold_{i}.model')]
            utils.run_cmd(cmd, args.dry_run, stdout=f, env=env)

    utils.run_cmd(['./xvallog2csv.py', '--directory', ds.name, '--xval_cols', 'xval_postprocessing.dat',
                   '--out_csv', f'{ds.name}_{nr.name}_{meth.name}', '--input_csv', f'{ds.name}_{nr.name}_4d.csv',
                   '--cols_4d', args.cols_4d], args.dry_run)

def run_method(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    if meth == MLMethod.OrigPAPA or meth == MLMethod.RetrainedPAPA:
        run_snns(ds, nr, meth)
    elif meth == MLMethod.WekaMLP:
        run_MLP(ds, nr, meth)
    elif meth == MLMethod.XvalWeka:
        run_MLPxval(ds, nr, meth)

# *************************************************************************
def postprocessing(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    def correction():
        cmd = ['./add_correction_factor.py',
                '--directory', ds.name, '--csv_input', f'{ds.name}_{nr.name}_{meth.name}.csv', '--cols_input',
                'post_processing.dat','--cols_stats', 'statistics.dat', '--csv_stats',
                f'{ds.name}_{nr.name}_{meth.name}_stats.csv', '--output_name', f'{ds.name}_{nr.name}_{meth.name}_corrected']
        utils.run_cmd(cmd, args.dry_run)

    name = f'{ds.name}_{nr.name}_{meth.name}'
    cmd=['./stats2graph.py',
         '--directory', ds.name, '--csv_input', f'{ds.name}_{nr.name}_{meth.name}.csv', '--cols_input',
         'post_processing.dat', '--name_normal',
         f'{name}_normal', '--name_outliers', f'{name}_normal',
         '--name_stats', f'{name}_stats', '--name_graph', name, '--graph_title',
         f'Graph of predicted vs actual values (Dataset:{ds.name}, Method{meth.name}).']
    utils.run_cmd(cmd, args.dry_run)
    correction()

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--cols-4d', default='4d.dat')
args = parser.parse_args()

for ds in Dataset:
    print(f'Processing dataset {ds}...')
    preprocessing(ds)
    for nr in NonRedundantization:
        run_nr(ds, nr)
        for meth in MLMethod:
            run_method(ds, nr, meth)
            postprocessing(ds, nr, meth)
