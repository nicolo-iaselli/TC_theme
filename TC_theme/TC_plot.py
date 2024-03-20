#########################
## IMPORT DEPENDENCIES ##
#########################
import plotly.express as px
# import plotly.io as pio
from collections import defaultdict
import base64
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go

##############################
## LIST OF INPUT PARAMETERS ##
##############################
input_params = {'data': 'DataFrame with data to be plot. MultiIndex in columns is allowed only if subplots=True.',
                'kind': 'Type of plot. Implemented type are: \'line\', \'scatter\', \'bar\', \'imshow\', \'scatter3d\', \'box\', \'hist\'',
                'x': 'Name of the dataframe column to be used on the x-axis (if None, data.index is used)',
                'y': 'Name of the dataframe column to be used on the y-axis (if None, data.columns is used)',
                'z': 'Name of the dataframe column to be used on the z-axis (only for 3D plots of imshow)',
                'show': 'bool, if True, the plot is shown',
                'main_logo_source': 'str, url or path for main logo',
                'proj_logo_source': 'str, url or path for additional project logo',
                'subplots': 'Bool, if True, columns of data are plotted in a different subplot.',
                '**plot_fun_keywords': 'The function accepts all the allowed plotly express parameters for the plot chosen in \'kind\' (only if subplots=False)',
                '**additional_parameters': 'Hardcoded layout and traces parameters. See dict \'additional_params\''
                }

#################################
## LIST OF ACCEPTED PARAMETERS ##
#################################
additional_params = {'title': 'Plot title (str, optional)',
                     'xlabel': 'Label of x-axis (str, optional)',
                     'ylabel': 'Label of y-axis (str, optional. List of str of len<=nr_subplots, if subplots=True)',
                     'zlabel': 'Label of z-axis (str, optional, only for 3D plots)',
                     'xlim': 'Limits on x-axis (list: [xmin, xmax], optional)',
                     'ylim': 'Limits on y-axis (list: [ymin, ymax], optional)',
                     'legend_title': 'Legend title (str, optional)',
                     'legend_location': 'Legend position (str, optional, \'innerNW\', \'innerNE\', \'innerSW\', \'innerSE\', \'outerW\', default=\'outerE\')',
                     'legend_borders': 'bool, il True, legend border is shown (default=False)',
                     'width': 'Figure width (int, optional, default=1500 px, if \'size\' is used, this parameter is ignored)',
                     'height': 'Figure height (int, optional, default=900 px, if \'size\' is used, this parameter is ignored)',
                     'size': 'Figure size (str, \'large\': w=1600px, h=1000px, \'medium\': w=1100px, h=800px, \'small\': w=900px, h=600px)',
                     'borders': 'Bool, if True, plot border is shown (default=False)',
                     'colorbar_title': 'Colorbar title (str, optional, if applicable)',
                     'mode': 'Sets mode for line plots (str, \'lines\', \'lines+markers\', \'markers\', default=\'lines\', only for kind=\'line\'. List of str of len<=nr_subplots, if subplots=True)',
                     'line_style': 'Sets style of line traces (str, \'solid\', \'dash\', \'dot\', or any accepted by line_dash property of plotly scatter traces, default=\'solid\', only for kind=\'line\'. '
                                   '\nList of str of len<=nr_subplots, if subplots=True)',
                     'line_color': 'Sets color of line traces (str, named CSS color, or any accepted by line_color property of plotly scatter traces, only for kind=\'line\'.'
                                   '\nList of str of len<=nr_subplots, if subplots=True)',
                     'line_width': 'Sets width of line traces (int, default=2 px, only for kind=\'line\'.'
                                   '\nList of str of len<=nr_subplots, if subplots=True)',
                     'line_shape': 'Sets the shape of the line (str, \'spline\': spline interpolation is used, \'steps-pre\', \'steps-post\', \'steps-mid\' correspond to step plots, default=\'linear\'.'
                                   '\nList of str of len<=nr_subplots, if subplots=True)',
                     'marker_color': 'Sets color of markers (str, named CSS color, or any accepted by line_color property of plotly scatter traces, only for kind=\'line\', \'scatter\'.'
                                     '\nList of str of len<=nr_subplots, if subplots=True)',
                     'marker_size': 'Sets size of markers (int, only for kind=\'line\', \'scatter\'.'
                                    '\nList of str of len<=nr_subplots, if subplots=True)',
                     'marker_alpha': 'Sets opacity of markers (int between or equal to 0 and 1, only for kind=\'line\', \'scatter\'.'
                                     '\nList of str of len<=nr_subplots, if subplots=True)',
                     'quartilemethod': 'Method to compute quartiles (str, \'exclusive\', \'inclusive\', \'linear\', only for kind=\'box\')',
                     'barmode': 'Sets how bars at the same location are displayed (str, \'stack\', \'relative\', \'group\', default=\'overlay\')',
                     }


###########################
## FNC: PARAM PREPROCESS ##
###########################
def process_params(param, kind):
    param = param.copy()  # Creates a copy

    traces, layouts = defaultdict(dict), defaultdict(dict)  # Default properties dictionaries

    # TRACES DEFINITION
    if kind == 'line':
        traces['mode'] = param.pop('mode', None)
        traces['line'].update(dash=param.pop('line_style', 'solid'))
        traces['line'].update(color=param.pop('line_color', None))
        traces['line'].update(width=param.pop('line_width', None))
    if kind == 'line' or kind == 'scatter':
        traces['marker'].update(color=param.pop('marker_color', None))
        traces['marker'].update(size=param.pop('marker_size', None))
        traces['marker'].update(opacity=param.pop('marker_alpha', None))
    if kind == 'box':
        traces['quartilemethod'] = param.pop('quartilemethod', 'linear')

    # LAYOUT DEFINITION
    layouts['title'].update(text=param.pop('title', None))
    if kind != 'scatter3d':
        layouts['xaxis'].update(title=param.pop('xlabel', None))
        layouts['yaxis'].update(title=param.pop('ylabel', None))
    else:
        layouts['scene'].update(xaxis=dict(title=param.pop('xlabel', None)),
                                yaxis=dict(title=param.pop('ylabel', None)),
                                zaxis=dict(title=param.pop('zlabel', None)))

    layouts['xaxis'].update(range=param.pop('xlim', None))
    layouts['yaxis'].update(range=param.pop('ylim', None))

    layouts['xaxis'].update(exponentformat=param.pop('exponent_format', 'power'))
    layouts['yaxis'].update(exponentformat=param.pop('exponent_format', 'power'))

    if 'borders' in param:
        layouts['xaxis'].update(showline=param['borders'], linecolor='#06476a', linewidth=1, mirror=True)
        layouts['yaxis'].update(showline=param['borders'], linecolor='#06476a', linewidth=1, mirror=True)
        param.pop('borders')

    layouts['width'] = param.pop('width', None)
    layouts['height'] = param.pop('height', None)
    if 'size' in param:
        if param['size'] == 'large':
            layouts['width'] = 1600
            layouts['height'] = 1000
        elif param['size'] == 'medium':
            layouts['width'] = 1100
            layouts['height'] = 800
        elif param['size'] == 'small':
            layouts['width'] = 900
            layouts['height'] = 600
        param.pop('size')
    layouts['coloraxis'].update(colorbar=dict(title=param.pop('colorbar_title', None)))
    layouts['barmode'] = param.pop('barmode', 'overlay')

    layouts['legend'].update(title=param.pop('legend_title', None))
    if 'legend_location' in param:
        if param['legend_location'] == 'innerNW':
            layouts['legend'].update(yanchor="top", y=0.99, xanchor="left", x=0.01)
        elif param['legend_location'] == 'innerNE':
            layouts['legend'].update(yanchor="top", y=0.99, xanchor="right", x=0.99)
        elif param['legend_location'] == 'innerSW':
            layouts['legend'].update(yanchor="bottom", y=0.01, xanchor="left", x=0.01)
        elif param['legend_location'] == 'innerSE':
            layouts['legend'].update(yanchor="bottom", y=0.01, xanchor="right", x=0.99)
        elif param['legend_location'] == 'outerE':
            layouts['legend'].update(yanchor="top", y=1, xanchor="left", x=1.02)
        elif param['legend_location'] == 'outerW':
            layouts['legend'].update(yanchor="top", y=1, xanchor="right", x=-0.1)
        param.pop('legend_location')

    if 'legend_borders' in param:
        if param['legend_borders']:
            layouts['legend'].update(bordercolor='#06476a', borderwidth=1)
        else:
            layouts['legend'].update(bordercolor=None, borderwidth=0)
        param.pop('legend_borders')

    # PLOT PARAMETERS DEFINITION
    if ('line_shape' in param) & (kind == 'line'):
        if param['line_shape'] == 'steps-pre':
            param['line_shape'] = 'vh'
        elif param['line_shape'] == 'steps-post':
            param['line_shape'] = 'hv'
        elif param['line_shape'] == 'steps-mid':
            param['line_shape'] = 'hvh'
        else:
            pass
    return param, traces, layouts


###########################
## FNC: PARAM PREPROCESS ##
###########################
def process_params_subplot(param, n_sp, kind):
    param = param.copy()
    traces, layouts, axes = defaultdict(dict), defaultdict(dict), defaultdict(dict)  # Default properties dictionaries

    # Set param for each subplot
    figure_param = ['width', 'height', 'size', 'title', 'xlabel', 'xlim',
                    'legend_title', 'legend_location', 'legend_borders', 'borders']
    for pp in param.keys():
        if pp not in figure_param:
            if len(param[pp]) == 1:
                param[pp] = param[pp] * n_sp
            elif (len(param[pp]) > 1) & (len(param[pp]) < n_sp):
                param[pp] = param[pp] * (n_sp // len(param[pp])) + param[pp][:n_sp % len(param[pp])]

    # Traces param
    for sp in range(n_sp):
        if 'mode' in param:
            traces[sp]['mode'] = param['mode'][sp]
        if 'line_color' in param:
            traces[sp]['line_color'] = param['line_color'][sp]
        if 'line_style' in param:
            traces[sp]['line_dash'] = param['line_style'][sp]
        if 'line_width' in param:
            traces[sp]['line_width'] = param['line_width'][sp]
        if 'marker_color' in param:
            traces[sp]['marker_color'] = param['marker_color'][sp]
        if 'marker_size' in param:
            traces[sp]['marker_size'] = param['marker_size'][sp]
        if 'marker_alpha' in param:
            traces[sp]['marker_opacity'] = param['marker_alpha'][sp]
        if 'line_shape' in param:
            if param['line_shape'][sp] == 'steps-pre':
                traces[sp]['line_shape'] = 'vh'
            elif param['line_shape'][sp] == 'steps-post':
                traces[sp]['line_shape'] = 'hv'
            elif param['line_shape'][sp] == 'steps-mid':
                traces[sp]['line_shape'] = 'hvh'
            else:
                traces[sp]['line_shape'] = param['line_shape'][sp]

    param.pop('mode', None)
    param.pop('line_color', None)
    param.pop('line_style', None)
    param.pop('line_width', None)
    param.pop('marker_color', None)
    param.pop('marker_size', None)
    param.pop('marker_alpha', None)
    param.pop('line_shape', None)

    # Layout param
    layouts['width'] = param.pop('width', None)
    layouts['height'] = param.pop('height', None)
    if 'size' in param:
        if param['size'] == 'large':
            layouts['width'] = 1600
            layouts['height'] = 1000
        elif param['size'] == 'medium':
            layouts['width'] = 1100
            layouts['height'] = 800
        elif param['size'] == 'small':
            layouts['width'] = 900
            layouts['height'] = 600
        param.pop('size')
    layouts['title'].update(text=param.pop('title', None))

    layouts['legend'].update(title=param.pop('legend_title', None))
    if 'legend_location' in param:
        if param['legend_location'] == 'innerNW':
            layouts['legend'].update(yanchor="top", y=0.99, xanchor="left", x=0.01)
        elif param['legend_location'] == 'innerNE':
            layouts['legend'].update(yanchor="top", y=0.99, xanchor="right", x=0.99)
        elif param['legend_location'] == 'innerSW':
            layouts['legend'].update(yanchor="bottom", y=0.01, xanchor="left", x=0.01)
        elif param['legend_location'] == 'innerSE':
            layouts['legend'].update(yanchor="bottom", y=0.01, xanchor="right", x=0.99)
        elif param['legend_location'] == 'outerE':
            layouts['legend'].update(yanchor="top", y=1, xanchor="left", x=1.02)
        elif param['legend_location'] == 'outerW':
            layouts['legend'].update(yanchor="top", y=1, xanchor="right", x=-0.1)
        param.pop('legend_location')

    if 'legend_borders' in param:
        if param['legend_borders']:
            layouts['legend'].update(bordercolor='#06476a', borderwidth=1)
        else:
            layouts['legend'].update(bordercolor=None, borderwidth=0)
        param.pop('legend_borders')

    # Axes param
    axes['X'].update(title_text=param.pop('xlabel', None))
    axes['X'].update(range=param.pop('xlim', None))
    if 'borders' in param:
        axes['X'].update(showline=param['borders'], linecolor='#06476a', linewidth=1, mirror=True)

    axes['Y'] = defaultdict(dict)
    for sp in range(n_sp):
        if 'ylabel' in param:
            axes['Y'][sp]['title_text'] = param['ylabel'][sp]
        if 'ylim' in param:
            axes['Y'][sp]['range'] = param['ylim'][sp]
        if 'borders' in param:
            axes['Y'][sp].update(showline=param['borders'], linecolor='#06476a', linewidth=1, mirror=True)

    param.pop('ylabel', None)
    param.pop('ylim', None)
    if 'borders' in param:
        param.pop('borders')

    return param, traces, layouts, axes


###########################
## FNC: LOGOS DEFINITION ##
###########################
def set_logos(main_logo_source, proj_logo_source):
    # Set logos
    img_list = []
    if main_logo_source is not None:
        if 'https' in main_logo_source:
            main_logo = main_logo_source
        else:
            main_file_logo = base64.b64encode(open(main_logo_source, 'rb').read())
            main_logo = 'data:image/png;base64,{}'.format(main_file_logo.decode())
        main_img_dict = dict(name="mainlogo",
                             source=main_logo,
                             xref="paper", yref="paper",
                             x=1, y=1.01, sizex=1, sizey=0.12,
                             xanchor="right", yanchor="bottom",
                             opacity=1, visible=True)
        img_list.append(main_img_dict)
    if proj_logo_source is not None:
        if 'https' in proj_logo_source:
            proj_logo = proj_logo_source
        else:
            file_logo = base64.b64encode(open(proj_logo_source, 'rb').read())
            proj_logo = 'data:image/png;base64,{}'.format(file_logo.decode())
        proj_img_dict = dict(name="projlogo",
                             source=proj_logo,
                             xref="paper", yref="paper",
                             x=0.75, y=1.01, sizex=1, sizey=0.12,
                             xanchor="right", yanchor="bottom",
                             opacity=1, visible=True)
        img_list.append(proj_img_dict)

    return img_list


#####################
## FNC: INNER PLOT ##
#####################
def inner_plot(plot_fun, data, x, y, z, main_logo_source, proj_logo_source, fun_params, traces_params,
                   layout_params):

    if z is not None:  # 3D
        if plot_fun == px.imshow:
            inner_data = data.set_index([x, y])[z].unstack()
            fig = plot_fun(inner_data, **fun_params)
        elif (plot_fun == px.scatter_3d) or (plot_fun == px.line_3d):
            fig = plot_fun(data, x=x, y=y, z=z, **fun_params).update_traces(**traces_params)
        else:
            raise ValueError('Function not yet implemented')
    else:  # 2D
        fig = plot_fun(data, x=x, y=y, **fun_params).update_traces(**traces_params)

    fig.update_layout(**layout_params)

    fig.update_layout(images=set_logos(main_logo_source, proj_logo_source))

    # # Set logos
    # img_list = []
    # if main_logo_source is not None:
    #     if 'https' in main_logo_source:
    #         main_logo = main_logo_source
    #     else:
    #         main_file_logo = base64.b64encode(open(main_logo_source, 'rb').read())
    #         main_logo = 'data:image/png;base64,{}'.format(main_file_logo.decode())
    #     main_img_dict = dict(name="mainlogo",
    #                          source=main_logo,
    #                          xref="paper", yref="paper",
    #                          x=1, y=1.01, sizex=1, sizey=0.12,
    #                          xanchor="right", yanchor="bottom",
    #                          opacity=1, visible=True)
    #     img_list.append(main_img_dict)
    # if proj_logo_source is not None:
    #     if 'https' in proj_logo_source:
    #         proj_logo = proj_logo_source
    #     else:
    #         file_logo = base64.b64encode(open(proj_logo_source, 'rb').read())
    #         proj_logo = 'data:image/png;base64,{}'.format(file_logo.decode())
    #     proj_img_dict = dict(name="projlogo",
    #                          source=proj_logo,
    #                          xref="paper", yref="paper",
    #                          x=0.75, y=1.01, sizex=1, sizey=0.12,
    #                          xanchor="right", yanchor="bottom",
    #                          opacity=1, visible=True)
    #     img_list.append(proj_img_dict)
    # fig.update_layout(images=img_list)


    return fig



############################
## FNC: "PANDAS" SUBPLOTS ##
############################
def calc_subplots(data):
    if data.columns.nlevels > 1:
        data = data.sort_index(axis=1, level=list(range(data.columns.nlevels)))
        # level_list = []
        # for ll in range(df.columns.nlevels-1):
        #     level_list.append(df.columns.get_level_values(ll).unique())
        level_list = data.columns.levels[:-1]
        idx_subplots_temp = pd.MultiIndex.from_product(level_list)  #
        idx_subplots = list(set(idx_subplots_temp) & set([T[:-1] for T in data.columns]))
        idx_subplots.sort()
    else:
        idx_subplots = data.columns
    n_sp = len(idx_subplots)
    return idx_subplots, n_sp


############################
## FNC: "PANDAS" SUBPLOTS ##
############################
def inner_subplot(data, x, main_logo_source, proj_logo_source, traces_params, layout_params, axes_params):
    idx_subplots, n_sp = calc_subplots(data)
    fig = make_subplots(rows=n_sp, cols=1, shared_xaxes=True, subplot_titles=[str(T) for T in idx_subplots])

    for subplot in range(n_sp):
        for dd in pd.DataFrame(data[idx_subplots[subplot]]).sort_index().columns:

            if data.columns.nlevels > 1:
                leg_name = str(idx_subplots[subplot] + (dd,))
                leg_showlegend = True
            else:
                leg_name = dd
                leg_showlegend = False
            leg_legendgroup = None

            fig.add_trace(go.Scatter(x=x, y=pd.DataFrame(data[idx_subplots[subplot]])[dd],
                                     name=leg_name,
                                     showlegend=leg_showlegend,
                                     legendgroup=leg_legendgroup,
                                     **traces_params[subplot]
                                     ), row=subplot + 1, col=1)

        fig.update_yaxes(axes_params['Y'][subplot], row=subplot+1, col=1)

    fig.update_xaxes(axes_params['X'], row=n_sp, col=1)
    try:
        fig.update_xaxes(showline=axes_params['X']['showline'], linecolor=axes_params['X']['linecolor'],
                         linewidth=axes_params['X']['linewidth'], mirror=axes_params['X']['mirror'])
    except:
        pass

    fig.update_layout(layout_params)

    fig.update_layout(images=set_logos(main_logo_source, proj_logo_source))

    return fig


#######################
## FNC: FUN SELECTOR ##
#######################
def fun_selector(kind):
    if kind == 'line':
        plot_fun = px.line
    elif kind == 'scatter':
        plot_fun = px.scatter
    elif kind == 'bar':
        plot_fun = px.bar
    # elif kind =='density_heatmap':
    #    plot_fun = px.density_heatmap
    elif kind == 'imshow':
        plot_fun = px.imshow
    elif kind == 'scatter3d':
        plot_fun = px.scatter_3d
    elif kind == 'box':
        plot_fun = px.box
    elif kind == 'hist':
        plot_fun = px.histogram
    else:
        raise ValueError('Function not yet implemented')

    return plot_fun


#############################
## MAIN FUNCTION: TC_plot ##
#############################
def TC_plot(data=None, kind='line', x=None, y=None, z=None, show=True, main_logo_source=None, proj_logo_source=None,
             subplots=False, **param):
    # Assess input data
    if data is not None:
        if (x is None) and (kind != 'hist'):
            x = data.index
        if (y is None) and (kind != 'hist'):
            y = data.columns
    else:
        NoneType = type(None)
        if isinstance(x, NoneType) or isinstance(y, NoneType):
            raise TypeError('Both x and y must be specified if data is None')

    plot_fun = fun_selector(kind)  # Select type of plot

    if subplots:
        _, n_sp = calc_subplots(data)
        fun_params, traces_params, layout_params, axes_params = process_params_subplot(param, n_sp,
                                                                                       kind)  # Param preprocess

        fig = inner_subplot(data, x, main_logo_source, proj_logo_source, traces_params, layout_params, axes_params)
    else:
        if data is not None:
            if isinstance(data.columns, pd.MultiIndex):
                raise TypeError('MultiIndex only supported in subplots')
        # else:
        fun_params, traces_params, layout_params = process_params(param, kind)  # Param preprocess

        fig = inner_plot(plot_fun, data, x, y, z, main_logo_source, proj_logo_source, fun_params, traces_params,
                             layout_params)  # Plot function

    if show:
        fig.show()

    return fig
