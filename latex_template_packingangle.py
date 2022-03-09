import itertools

from pipeline_enums import *

import pylatex as pl
import os
import pandas as pd


def _add_data(doc: pl.Document, ds: Dataset, nr: NonRedundantization, meth: MLMethod, cr: Correction):
    name = f'{ds.name}_{nr.name}_{meth.name}_{cr.name}'
    directory = ds.name

    aVp_graph = f'{name}.jpg'
    angle_dist_graph = f'{name}_angledistribution.jpg'
    error_dist_graph = f'{name}_errordistribution.jpg'
    sqerror_graph = f'{name}_sqerror_vs_actual.jpg'
    stats_csv_all = f'{name}_stats_all.csv'
    stats_csv_out = f'{name}_stats_out.csv'

    actualVpred_file = os.path.join(directory, aVp_graph)
    ang_dist_file = os.path.join(directory, angle_dist_graph)
    error_dist_file = os.path.join(directory, error_dist_graph)
    sqerror_file = os.path.join(directory, sqerror_graph)

    df_all = pd.read_csv(os.path.join(
        directory, stats_csv_all))
    df_out = pd.read_csv(os.path.join(
        directory, stats_csv_out))

    if meth != MLMethod.XvalWeka:
        tt = TestTrain(get_training_from_testing(ds), ds)
        with doc.create(pl.Section(f'Method: {tt.training.name}, {tt.testing.name}, {nr.name}, {meth.name}, {cr.name}')):
            with doc.create(pl.Subsection('Summary of method:')):
                doc.append(f'Train set: {tt.training.name}')
                doc.append(f'\nTest set: {tt.testing.name}')
                doc.append(f'\nNon-redundantization: {nr.name}')
                doc.append(f'\nType of machine learning used: {meth.name}')
                doc.append(f'\nCorrection: {cr.name}')
    else:
        with doc.create(pl.Section(f'Method: {ds.name}, {nr.name}, {meth.name}, {cr.name}')):
            with doc.create(pl.Subsection('Summary of method:')):
                doc.append(f'Dataset: {ds.name}')
                doc.append(f'\nNon-redundantization: {nr.name}')
                doc.append(f'\nType of machine learning used: {meth.name}')
                doc.append(f'\nCorrection: {cr.name}')

    with doc.create(pl.Subsection('Summary of the data:')):
        with doc.create(pl.Figure(position='!htbp')) as actualVpred:
            actualVpred.add_image(actualVpred_file, width='300px')
            actualVpred.add_caption(
                'Graph showing the predicted packing angle against the actual packing angle, when using the above specified methods of non-redundetization and machine learning.')

        with doc.create(pl.Table(position='!htbp')) as table:
            table.add_caption('Summary of results for all data')
            table.append(pl.Command('centering'))
            table.append(pl.NoEscape(df_all.to_latex(escape=False)))

        with doc.create(pl.Table(position='!htbp')) as table:
            table.add_caption('Summary of results for outliers.')
            table.append(pl.Command('centering'))
            table.append(pl.NoEscape(df_out.to_latex(escape=False)))

        with doc.create(pl.Figure(position='!htbp')) as graphs:
            with doc.create(pl.SubFigure(
                    position='!htbp',
                    width=pl.NoEscape(r'0.30\linewidth'))) as ang_dist_graph:
                ang_dist_graph.add_image(ang_dist_file,
                                            width=pl.NoEscape(r'\linewidth'))
                ang_dist_graph.add_caption(
                    'Frequency distribution of the packing angle.')
            with doc.create(pl.SubFigure(
                    position='!htbp',
                    width=pl.NoEscape(r'0.33\linewidth'))) as error_dist_graph:
                error_dist_graph.add_image(error_dist_file,
                                            width=pl.NoEscape(r'\linewidth'))
                error_dist_graph.add_caption(
                    'Distribution of errors calculated as the difference between the predicted and actual interface angle.')
            with doc.create(pl.SubFigure(
                    position='!htbp',
                    width=pl.NoEscape(r'0.33\linewidth'))) as sqerror_graph:
                sqerror_graph.add_image(sqerror_file,
                                        width=pl.NoEscape(r'\linewidth'))
                sqerror_graph.add_caption(
                    'Squared error in predicted packing angle against actual packing angle.')
            graphs.add_caption('Graphs for further metrics.')


def generate_latex():
    top10 = 'top10.csv'
    top10_df = pd.read_csv(top10)
    top10_o = 'top10_out.csv'
    top10_o_df = pd.read_csv(top10_o)

    doc = pl.Document(page_numbers=True, geometry_options={
                      "tmargin": "1cm", "lmargin": "1cm"})

    doc.packages.append(pl.Package('booktabs'))
    doc.preamble.append(pl.Command(
        'title', 'VH/VL Packing Angle Pipeline Results'))
    doc.preamble.append(pl.Command('author', 'Veronica A. Boron'))

    doc.append(pl.NoEscape(r'\maketitle'))
    doc.append(
        'This document summarizes the results obtained by running `packing_angle_pipeline.py` on various datasets.')
    # TODO table of contents is broken and doesn't show all sections
    # doc.append(pl.NoEscape(r'\tableofcontents'))
    doc.append(pl.NoEscape(r'\newpage'))
    with doc.create(pl.Section(f'Summary of Results')):
        with doc.create(pl.Table(position='!htbp')) as table:
            table.add_caption('Rakings of the top 20 combinations of methods, datasets, non-redundatizing, \
            and correction factors. They were ranked according to a combination parameter which was calcuated \
            in the following way: Combined-parameter = |(1/Pearsons coefficient)| + |mean-error| + |RMSE| + \
            |RELRMSE|. The smallest combined-para value indicates a combination of low errors and \
            high correlation coefficient.')
            table.append(pl.Command('centering'))
            table.append(pl.NoEscape(r'\resizebox{\textwidth}{!}{'))
            table.append(pl.NoEscape(top10_df.to_latex(escape=False)))
            table.append(pl.NoEscape(r'}'))

        with doc.create(pl.Table(position='!htbp')) as table:
            table.add_caption('Rakings of the top 20 combinations of methods, datasets, non-redundatizing, \
            and correction factors for outlier prediction. They were ranked in according to a combination parameter.')
            table.append(pl.Command('centering'))
            table.append(pl.NoEscape(r'\resizebox{\textwidth}{!}{'))
            table.append(pl.NoEscape(top10_o_df.to_latex(escape=False)))
            table.append(pl.NoEscape(r'}'))

    for ds, nr, cr in itertools.product(Dataset, NonRedundantization, Correction):
        _add_data(doc, ds, nr, MLMethod.XvalWeka, cr)
        doc.append(pl.NoEscape(r'\newpage'))

    for tt, nr, meth, cr in itertools.product(get_all_testtrain(), NonRedundantization, MLMethod, Correction):
        if meth is not MLMethod.XvalWeka:
            _add_data(doc, tt.testing, nr, meth, cr)
        doc.append(pl.NoEscape(r'\newpage'))

    print('Generating PDF...')
    doc.generate_pdf('PipelineTest', clean_tex=False)
