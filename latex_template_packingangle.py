import numpy as np

from pylatex.basic import NewPage
import pylatex as pl
from pylatex.utils import italic
import os
import argparse
import pandas as pd


def output_data(directory, dataset, nr, ml, aVp_graph, angle_dist_graph, error_dist_graph, sqerror_graph,
                stats_csv_all, stats_csv_out, stats_cols):

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = pl.Document(page_numbers=True, geometry_options=geometry_options)

    actualVpred_file = os.path.join(directory, aVp_graph)
    ang_dist_file = os.path.join(directory, angle_dist_graph)
    error_dist_file = os.path.join(directory, error_dist_graph)
    sqerror_file = os.path.join(directory, sqerror_graph)
    col = [i.strip('\n') for i in open(stats_cols).readlines()]
    df_all = pd.read_csv(os.path.join(directory, stats_csv_all), usecols=col)
    df_out = pd.read_csv(os.path.join(directory, stats_csv_out), usecols=col)
    doc.packages.append(pl.Package('booktabs'))

    with doc.create(pl.Section('VH/VL Packing Angle Pipeline Results')):
        doc.append(
            'This document summerizes the results obtaning by running `packing_angle_pipeline.py` on various datasets.')
        with doc.create(pl.Subsection('Summary of method:')):
            doc.append(f'Datset: {dataset}')
            doc.append(f'\nNon-redundantization: {nr}')
            doc.append(f'\nType of machine learning used: {ml}')

        with doc.create(pl.Subsection('Summary of the data:')):
            with doc.create(pl.Figure(position='h!')) as actualVpred:
                actualVpred.add_image(actualVpred_file, width='120px')
                actualVpred.add_caption(
                    'Graph showing the predicted packing angle against the actual packing angle, when using the above specified methods of non-redundetization and machine learning.')

            with doc.create(pl.Table(position='htbp')) as table:
                table.add_caption('Summary of results for all data')
                table.append(pl.Command('centering'))
                table.append(pl.NoEscape(df_all.to_latex(escape=False)))

            with doc.create(pl.Table(position='htbp')) as table:
                table.add_caption('Summary of results for outliers.')
                table.append(pl.Command('centering'))
                table.append(pl.NoEscape(df_out.to_latex(escape=False)))

            with doc.create(pl.Figure(position='h!')) as graphs:
                with doc.create(pl.SubFigure(
                        position='b',
                        width=pl.NoEscape(r'0.30\linewidth'))) as ang_dist_graph:

                    ang_dist_graph.add_image(ang_dist_file,
                                             width=pl.NoEscape(r'\linewidth'))
                    ang_dist_graph.add_caption(
                        'Frequency distribution of the packing angle.')
                with doc.create(pl.SubFigure(
                        position='b',
                        width=pl.NoEscape(r'0.33\linewidth'))) as error_dist_graph:

                    error_dist_graph.add_image(error_dist_file,
                                               width=pl.NoEscape(r'\linewidth'))
                    error_dist_graph.add_caption(
                        'Distribution of errors calculated as the difference between the predicted and actual interface angle.')
                with doc.create(pl.SubFigure(
                        position='b',
                        width=pl.NoEscape(r'0.33\linewidth'))) as sqerror_graph:

                    sqerror_graph.add_image(sqerror_file,
                                            width=pl.NoEscape(r'0.33\linewidth'))
                    sqerror_graph.add_caption(
                        'Squared error in predicted packing angle against actual packing angle.')
                graphs.add_caption('Graphs for further metrics.')
    doc.generate_pdf('testing', clean_tex=False)
