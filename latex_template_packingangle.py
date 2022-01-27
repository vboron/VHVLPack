import itertools
import numpy as np

from pipeline_enums import Dataset, NonRedundantization, MLMethod, unique_name

import pylatex as pl
import os
import pandas as pd

def _add_data(doc: pl.Document, ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    name = unique_name(ds, nr, meth)
    directory = ds.name

    aVp_graph = f'{name}.jpg'
    angle_dist_graph = f'{name}_angledistribution.jpg'
    error_dist_graph = f'{name}_errordistribution.jpg'
    sqerror_graph = f'{name}_sqerror_vs_actual.jpg'
    stats_csv_all = f'{name}_stats_all.csv'
    stats_csv_out = f'{name}_stats_out.csv'
    stats_cols = 'read_stats_csv.dat'

    actualVpred_file = os.path.join(directory, aVp_graph)
    ang_dist_file = os.path.join(directory, angle_dist_graph)
    error_dist_file = os.path.join(directory, error_dist_graph)
    sqerror_file = os.path.join(directory, sqerror_graph)
    col = [i.strip('\n') for i in open(stats_cols).readlines()]
    df_all = pd.read_csv(os.path.join(directory, stats_csv_all), usecols=col)
    df_out = pd.read_csv(os.path.join(directory, stats_csv_out), usecols=col)

    with doc.create(pl.Section(f'Method ({ds.name}, {nr.name}, {meth.name})')):
        with doc.create(pl.Subsection('Summary of method:')):
            doc.append(f'Datset: {ds.name}')
            doc.append(f'\nNon-redundantization: {nr.name}')
            doc.append(f'\nType of machine learning used: {meth.name}')

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

def output_data(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
    doc = pl.Document(page_numbers=True, geometry_options={"tmargin": "1cm", "lmargin": "1cm"})
    doc.packages.append(pl.Package('booktabs'))
    doc.preamble.append(pl.Command('title', 'VH/VL Packing Angle Pipeline Results'))
    doc.preamble.append(pl.Command('author', 'Veronica A. Boron'))
    doc.append(pl.NoEscape(r'\maketitle'))

    doc.append(
        'This document summerizes the results obtaning by running `packing_angle_pipeline.py` on various datasets.')

    for ds, nr, meth in itertools.product(Dataset, NonRedundantization, MLMethod):
        _add_data(doc, ds, nr, meth)

    doc.generate_pdf('testing', clean_tex=False)
