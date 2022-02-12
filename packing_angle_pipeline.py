#!/usr/bin/python3
# # *************************************************************************
from pipeline_enums import Correction, Dataset, NonRedundantization, MLMethod, unique_name, TestTrain, get_all_testtrain
import os
import argparse
import utils
import nonred
import shutil
import subprocess
import graphing
import itertools
import latex_template_packingangle as ltp

# *************************************************************************


def preprocessing(ds: Dataset):
    def run_compile_angles(ds: Dataset):
        utils.run_cmd(['./compile_angles.py', '--directory', ds.name,
                      '--csv_output', f'{ds.name}_ang'], args.dry_run)

    def run_find_VHVLres(ds: Dataset):
        utils.run_cmd(['./find_VHVLres.py', '--directory', ds.name,
                      '--csv_output', f'{ds.name}_res'], args.dry_run)

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
def run_papa(nr: NonRedundantization, meth: MLMethod, tt: TestTrain):
    utils.run_cmd(['./snns_run_and_compile_data.py', '--directory', tt.testing.name, '--seq_directory',
                   os.path.join(
                       tt.testing.name, 'seq_files'),
                   '--angle_csv', f'{tt.testing.name}_ang.csv', '--which_papa', 'papa', '--csv_output',
                   f'{tt.testing.name}_{nr.name}_{meth.name}'], args.dry_run)


def run_newpapa(nr: NonRedundantization, meth: MLMethod, tt: TestTrain):
    with open(f'{tt.training.name}/{tt.training.name}_{nr.name}_{meth.name}.arff', 'w') as f:
        path = os.path.join(
            tt.training.name, f'{tt.training.name}_{nr.name}_4d.csv')
        utils.run_cmd(['csv2arff', '-norm', '-ni', 'in4d.dat', 'angle', path],
                      args.dry_run, stdout=f)
    pat_path = os.path.join('SNNS', 'papa', 'training', 'final.pat')
    with open(pat_path) as f:
        utils.run_cmd(
            ['arff2snns', f'{tt.training.name}/{tt.training.name}_{nr.name}_{meth.name}.arff'], args.dry_run, stdout=f)

    utils.run_cmd(['batchman', '-f', 'final_training.cmd'], args.dry_run,
                  cwd=os.path.join(os.getcwd(), 'SNNS/papa/training'))

    home_dir = os.environ['HOME']
    utils.run_cmd(['./install.sh', f'{home_dir}/{tt.training.name}_{nr.name}_{meth.name}'],
                  args.dry_run,
                  cwd='SNNS/papa')

    utils.run_cmd(['./snns_run_and_compile_data.py', '--directory', tt.testing.name, '--seq_directory',
                   os.path.join(
                       tt.testing.name, 'seq_files'), '--angle_csv', f'{tt.testing.name}_ang.csv', '--csv_output',
                   f'{tt.testing.name}_{nr.name}_{meth.name}',
                   '--which_papa', os.path.join(os.environ['HOME'], f'{tt.training.name}_{nr.name}_{meth.name}', 'papa')],
                  args.dry_run)


def run_snns(nr: NonRedundantization, meth: MLMethod, tt: TestTrain):
    utils.run_cmd(['./pdb2seq.py', '--directory',
                  tt.training.name], args.dry_run)
    utils.run_cmd(['./pdb2seq.py', '--directory',
                  tt.testing.name], args.dry_run)
    # distinguish between making a new papa and running the old papa
    if meth == MLMethod.OrigPAPA:
        run_papa(nr, meth, tt)
    elif meth == MLMethod.RetrainedPAPA:
        run_newpapa(nr, meth, tt)
    else:
        raise ValueError(f'Handling of meth={meth} not implemented')


def run_MLP(nr: NonRedundantization, meth: MLMethod, tt: TestTrain):
    utils.run_cmd(['./splitlines_csv2arff_MLP.py', '--train_dir', tt.training.name, '--test_dir', tt.testing.name,
                   '--columns_4d', args.cols_4d, '--training_csv', f'{tt.training.name}_{nr.name}_4d.csv',
                   '--testing_csv', f'{tt.testing.name}_{nr.name}_4d.csv', '--input_cols', 'in4d.dat', '--train_set',
                   f'{tt.training.name}_{nr.name}', '--test_set', f'{tt.testing.name}_{nr.name}'], args.dry_run)
    utils.run_cmd(['./extract_data_from_logfiles.py', '--directory',
                   os.path.join(tt.testing.name,
                                f'{tt.testing.name}_{nr.name}_testing_data'),
                   '--columns_postprocessing', args.postprocessing_cols, '--output_name',
                   f'{tt.testing.name}/{tt.testing.name}_{nr.name}_{meth.name}'], args.dry_run)

# multilayer perceptron cross validation


def run_MLPxval(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    utils.run_cmd(['./split_10.py',
                   '--input_csv', f'{ds.name}_{nr.name}_4d.csv',
                   '--columns', args.cols_4d,
                   '--directory', ds.name,
                   '--output_tag', f'{nr.name}',
                   '--csv2arff_cols', 'in4d.dat'],
                  args.dry_run)

    classifier = 'weka.classifiers.functions.MultilayerPerceptron'
    env = {'WEKA': '/usr/local/apps/weka-3-8-3'}
    env['CLASSPATH'] = f'{env["WEKA"]}/weka.jar'
    for i in range(1, 11):
        # train
        file_name = os.path.join(ds.name, f'{nr.name}_{i}_train.log')
        with open(file_name, 'w') as f:
            cmd = ['java', classifier, '-v', '-x', '3', '-H', '20',
                   '-t', os.path.join(ds.name, f'{nr.name}_{i}_train.arff'),
                   '-d', os.path.join(ds.name, f'{nr.name}_fold_{i}.model')]
            utils.run_cmd(cmd, args.dry_run, stdout=f,
                          env=env, stderr=subprocess.DEVNULL)
            assert(os.stat(file_name).st_size != 0)

        # test
        path = os.path.join(ds.name, f'test_files_{i}')
        for file in os.listdir(path):
            arff_files = []
            if file.endswith('.arff'):
                arff_files.append(file)
            for _file in arff_files:
                name = os.path.splitext(_file)[0]
                file_path = os.path.join(path, f'{name}.log')
                with open(file_path, 'w') as f:
                    cmd = ['java', classifier, '-v', '-T', os.path.join(path, file), '-p', '0', '-l',
                           os.path.join(ds.name, f'{nr.name}_fold_{i}.model')]
                    utils.run_cmd(cmd, args.dry_run, stdout=f,
                                  env=env, stderr=subprocess.DEVNULL)
                    assert(os.stat(file_path).st_size != 0)

    utils.run_cmd(['./xvallog2csv.py', '--directory', ds.name, '--columns_postprocessing', args.postprocessing_cols,
                   '--output_name', f'{ds.name}/{ds.name}_{nr.name}_{meth.name}'], args.dry_run)


def run_method(ds: Dataset, nr: NonRedundantization, meth: MLMethod, tt: TestTrain):
    # if meth == MLMethod.OrigPAPA or meth == MLMethod.RetrainedPAPA:
    #     run_snns(nr, meth, tt)
    if meth == MLMethod.WekaMLP:
        run_MLP(nr, meth, tt)
    if meth == MLMethod.XvalWeka:
        run_MLPxval(ds, nr, meth)

# *************************************************************************


def correction(ds: Dataset, nr: NonRedundantization, meth: MLMethod, name):
    cmd = ['./add_correction_factor.py',
           '--directory', ds.name, '--csv_input', f'{ds.name}_{nr.name}_{meth.name}.csv', '--cols_input',
           args.postprocessing_cols, '--cols_stats', 'read_stats_csv.dat', '--csv_stats',
           f'{ds.name}_{nr.name}_{meth.name}_NotCorrected_stats_all.csv', '--output_name', f'{name}']
    utils.run_cmd(cmd, args.dry_run)


def run_graphs(ds: Dataset, name):
    cmd = ['./stats2graph.py',
           '--directory', ds.name, '--csv_input', f'{name}.csv', '--cols_input',
           args.postprocessing_cols, '--name_normal',
           f'{name}_normal', '--name_outliers', f'{name}_normal',
           '--name_stats', f'{name}_stats', '--name_graph', name]
    utils.run_cmd(cmd, args.dry_run)
    graphing.sq_error_vs_actual_angle(ds.name, f'{name}.csv', args.postprocessing_cols,
                                      f'{name}_sqerror_vs_actual')
    graphing.angle_distribution(
        ds.name, f'{ds.name}_ang.csv', f'{name}_angledistribution')
    graphing.error_distribution(ds.name, f'{name}.csv', args.postprocessing_cols,
                                f'{name}_errordistribution')
    graphing.sq_error_vs_actual_angle(ds.name, f'{name}.csv', args.postprocessing_cols,
                                      f'{name}_sqerror_vs_actual')


def postprocessing(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cr: Correction, tt: TestTrain):
    name = unique_name(ds, nr, meth, cr)
    if cr == Correction.NotCorrected:
        src_path = os.path.join(
            ds.name, f'{ds.name}_{nr.name}_{meth.name}.csv')
        dst_path = os.path.join(ds.name, f'{name}.csv')
        shutil.copyfile(src_path, dst_path)
        run_graphs(ds, name)
    else:
        correction(ds, nr, meth, name)
        run_graphs(ds, name)


parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--cols-4d', default='4d.dat')
parser.add_argument('--postprocessing_cols', default='post_processing.dat')
parser.add_argument('--preprocess', action='store_true', default=False)
parser.add_argument('--process', action='store_true', default=False)
parser.add_argument('--postprocess', action='store_true', default=False)
parser.add_argument('--latex', action='store_true', default=False)

args = parser.parse_args()

if not args.preprocess and not args.process and not args.postprocess and not args.latex:
    print('Neither --preprocess nor --process nor --postprocess nor --latex has been specified. Enabling all of them.')
    args.process = args.postprocess = args.latex = True

if args.preprocess:
    print('Pre-processing...')
    for ds in Dataset:
        print(f'Dataset={ds.name}...')
        preprocessing(ds)
        for nr in NonRedundantization:
            print(f"Non-redundantizing (Dataset={ds.name}: nr={nr.name})")
            run_nr(ds, nr)

if args.process:
    print('Processing...')
    for ds, nr, meth, tt in itertools.product(Dataset, NonRedundantization, MLMethod, get_all_testtrain()):
        print(f"Training={tt.training.name}, Testing={tt.testing.name}, nr={nr.name}: processing meth={meth.name}")
        run_method(ds, nr, meth, tt)

if args.postprocess:
    print('Postprocessing...')
    for ds, nr, meth, cr, tt in itertools.product(Dataset, NonRedundantization, MLMethod, Correction, get_all_testtrain()):
        postprocessing(ds, nr, meth, cr, tt)

if args.latex:
    print('Generating LaTeX...')
    ltp.generate_latex()

print('Goodbye!')
