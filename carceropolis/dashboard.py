import base64
import threading
from urllib.parse import parse_qs

import pandas as pd
from tornado.ioloop import IOLoop
from bokeh.core.properties import value
from bokeh import palettes
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import HoverTool
from bokeh.server.server import Server
from bokeh.layouts import widgetbox, row
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.models.widgets.inputs import Select, MultiSelect
from bokeh.models import ColumnDataSource, RangeSlider, CustomJS


def update_querystring(window=None, cb_obj=None):
    '''
    This callback should be converted to JS! It updates
    the url querystring when chart options change.
    '''
    params = []
    for c in cb_obj.document.roots()[0].children[0].children:
        value = c.value
        params.append(
            window.encodeURIComponent(c.name) + '=' +
            window.encodeURIComponent(value)
        )
    query = '?' + '&'.join(params)
    window.history.pushState({}, '', query)


def load_db():
    '''
    Loads test data for development.
    '''
    df = pd.read_csv('test.csv')
    df.ano = df.ano.astype(str)
    return df


def hide_widget(widget):
    '''
    Hides a widget.
    '''
    if not widget.css_classes:
        widget.css_classes = []
    if 'hidden' not in widget.css_classes:
        widget.css_classes.append('hidden')


def show_widget(widget):
    '''
    Shows a widget.
    '''
    if widget.css_classes and 'hidden' in widget.css_classes:
        widget.css_classes.remove('hidden')


def get_legend(y, ys):
    '''
    Return a legend string for a column.
    A `value` is used to avoid Bokeh behavior of replacing
    the string with the column data when the name matches.
    If only one column will be plotted, uses empty legend.
    '''
    return value(y) if len(ys) > 1 else None


def create_source(df, x, y, color):
    '''
    Creates a datasource in the format needed for tooltips.
    '''
    return ColumnDataSource(data={
        x: df[x],
        'value': df[y],
        'value_name': [y]*len(df),
        'color': [color]*len(df),
    })
    return ColumnDataSource(data=df)


def plot_bar_iterator(ys, outer_width, palette):
    '''
    Helper function that generates values used to plot bars.
    '''
    l = len(ys)
    for y, color, i in zip(ys, palette, range(0, l)):
        # Spreads bars based on the number of bars and their
        # width, so they don't overlap
        offset = round(-outer_width*l/2 + outer_width/2 + outer_width*i, 2)
        yield y, offset, color


def plot_lines(fig, x, ys, df, palette):
    '''
    Plot a line chart.
    '''
    for y, color in zip(ys, palette):
        source = create_source(df, x, y, color)
        fig.line(
            x, 'value', source=source, line_width=3, color=color,
            legend=get_legend(y, ys))


def plot_vbar(fig, x, ys, df, palette):
    '''
    Plot a vertical bar chart.
    '''
    width = 0.2
    for y, offset, color in plot_bar_iterator(ys, width+.03, palette):
        source = create_source(df, x, y, color)
        fig.vbar(
            x=dodge(x, offset, range=fig.x_range), width=width+.03, top='value',
            source=source, color=color, legend=get_legend(y, ys))


def plot_hbar(fig, x, ys, df, palette):
    '''
    Plot a horizontal bar chart.
    '''
    width = 0.2
    for y, offset, color in plot_bar_iterator(ys, width+.03, palette):
        source = create_source(df, x, y, color)
        fig.hbar(
            y=dodge(x, offset, range=fig.y_range), height=width, right='value',
            source=source, color=color, legend=get_legend(y, ys))


def plot_circles(fig, x, ys, df, palette):
    '''
    Plot a scatter chart.
    '''
    for y, color in zip(ys, palette):
        source = create_source(df, x, y, color)
        fig.circle(
            x, 'value', size=10, source=source, color=color,
            legend=get_legend(y, ys))


class Dashboard(object):
    '''
    This class represents a dashboard and should be instanciated
    for each user.
    The `generate` static method is used by the Bokeh server to
    instanciate dashboards.
    '''

    # TODO: maybe remove this?
    df = load_db()

    @staticmethod
    def generate(doc):
        '''
        Generate a new dashboard. This function should be passed
        to the Bokeh FunctionHandler.
        '''
        return Dashboard(Dashboard.df.copy(), doc)

    def __init__(self, df, doc):
        '''
        Called when a user connects. This dashboard should be used
        while the connection remain, and is used by only one user.
        '''

        state = doc.session_context.request.arguments.get('state')
        if state:
            state = parse_qs(base64.urlsafe_b64decode(state[0]).decode())
        else:
            state = {}

        self.chart_types = {
            'linha': {
                'fn': plot_lines
            },
            'barras horizontais': {
                'fn': plot_hbar,
                'invert_axies': True
            },
            'barras verticais': {
                'fn': plot_vbar
            },
            'círculos': {
                'fn': plot_circles
            },
        }
        charts_names = list(self.chart_types)
        none_value = 'Nenhum'

        self.df = df
        self.doc = doc
        self.columns = sorted(df.columns)
        self.palette = palettes.Dark2_8
        self.discrete = [x for x in self.columns if self.df[x].dtype == object]
        # continuous = [x for x in columns if x not in discrete]
        # discrete.append(continuous.pop(continuous.index('ano')))
        self.filter_options = [none_value]+self.columns

        gui_data = {
            'x_sel': {
                'name': 'x',
                'title': 'Eixo X',
                'value': 'ano',
                'options': self.columns,
                'class': Select,
            },
            'y_sel': {
                'name': 'y',
                'title': 'Eixo Y',
                'value': ['pop_masc'],
                'options': self.columns,
                'class': MultiSelect,
                'querystring_extract_fn':
                    lambda s: s.split(','),
            },
            'chart_type_sel': {
                'name': 'type',
                'title': 'Tipo de Gráfico',
                'value': charts_names[2],
                'options': charts_names,
                'class': Select,
            },
            'filter_sel': {
                'name': 'filter',
                'title': 'Filtro',
                'value': self.filter_options[0],
                'options': self.filter_options,
                'class': Select,
            },
            'filter_value_sel': {
                'name': 'f_value',
                'title': 'Valor',
                'value': none_value,
                'options': [none_value],
                'class': Select,
            },
            # TODO: this widget is bugged, but it seems they are improving it.
            'filter_range_sel': {
                'name': 'f_range',
                'title': 'Intervalo',
                'start': 0,
                'end': 10,
                'step': 1,
                'value': [1, 9],
                'class': RangeSlider,
                'querystring_extract_fn':
                    lambda s: tuple(float(i) for i in s.split(',')),
            },
        }

        # If has a previous state (passed throught querystring)
        # restore it.
        # TODO: validate state? Dangerous?
        if state:
            for gui, data in gui_data.items():
                value = state.get(data['name'])
                if value:
                    value = value[0]

                    # If the model as a special function to extract
                    # the querystring data, use it.
                    fn = data.get('querystring_extract_fn')
                    if fn:
                        data['value'] = fn(value)
                    else:
                        data['value'] = value

        self.js_update_querytstring = CustomJS.from_py_func(update_querystring)

        # Create gui inputs
        self.controls = {}
        for k, v in gui_data.items():
            v = v.copy()
            class_ = v.pop('class')
            v.pop('querystring_extract_fn', None)
            control = self.create_control(class_, v)
            self.controls[k] = control

        # TODO: seems to have no effect?
        self.controls['filter_range_sel'].callback_policy = 'mouseup'

        self.layout = row(
            widgetbox(list(self.controls.values()), width=200),
            self.create_figure())
        self.layout.css_classes = ['centered']
        doc.add_root(self.layout)

    def create_control(self, class_, args):
        '''
        Creates an input widget binding needed callbacks.
        '''
        control = class_(**args)
        # Bind callbacks
        control.on_change('value', self.update)
        control.callback = self.js_update_querytstring
        return control

    def update(self, attr, old, new):
        '''
        Called when chart options are modified.
        '''
        # It seems sometimes, when restoring state, self has no layout.
        # This 'try' avoids that error.
        try:
            self.layout.children[1] = self.create_figure(attr, old, new)
        except AttributeError:
            pass

    def handle_filtering(self, df):
        '''
        Update filter selectors widgets and use their values
        to filter `df`.
        '''
        fs = self.controls['filter_sel']
        frs = self.controls['filter_range_sel']
        fvs = self.controls['filter_value_sel']
        if fs.value != self.filter_options[0]:
            filter_column = df[fs.value]
            if fs.value in self.discrete:
                # Discrete filter

                # update selector
                options = sorted(list(filter_column.unique()))
                fvs.options = options
                if fvs.value not in options:
                    fvs.value = options[0]

                show_widget(fvs)
                hide_widget(frs)

                # filter df
                df = df[filter_column == fvs.value]

            else:
                # Continuous filter

                min_val = filter_column.min()
                max_val = filter_column.max()

                # update slider
                frs.start = min_val
                frs.end = max_val
                if frs.value[0] < min_val or frs.value[1] > max_val:
                    frs.value = (min_val, max_val)
                frs.step = (max_val-min_val)/10

                show_widget(frs)
                hide_widget(fvs)

                # filter df
                df = df[filter_column >= frs.value[0]]
                df = df[filter_column <= frs.value[1]]
        else:
            # No filter
            hide_widget(fvs)
            # TODO: hide when RangeSlider css_classes work again
            # hide_widget(frs)

        return df

    def create_figure(self, attr=None, old=None, new=None):
        '''
        Creates the chart.
        '''
        df = self.handle_filtering(self.df)
        df = df.groupby(self.controls['x_sel'].value, as_index=False).sum()

        chart_type_info = self.chart_types[
            self.controls['chart_type_sel'].value]
        x_value = self.controls['x_sel'].value
        y_values = self.controls['y_sel'].value

        x_title = x_value.title()
        y_title = ', '.join(y.title() for y in y_values)

        kw = {}
        if x_value in self.discrete:
            kw['x_range'] = sorted(set(df[x_value]))
        # TODO: os dois eixos podem ter valores discretos?
        # TODO: e múltiplos valores discretos no Y? e misto?
        # if y_value in self.discrete:
        #     kw['y_range'] = sorted(set(ys))

        kw['y_range'] = (0, max([max(df[y].values) for y in y_values]))

        no_color_grid_direction = 'xgrid'
        if chart_type_info.get('invert_axies'):
            x_title, y_title = y_title, x_title
            kw['x_range'], kw['y_range'] = kw['y_range'], kw['x_range']
            no_color_grid_direction = 'ygrid'

        kw['title'] = "%s vs %s" % (x_title, y_title)

        fig = figure(
            plot_height=600, plot_width=800, background_fill_alpha=0,
            border_fill_alpha=0, tools='pan,box_zoom,reset,save', **kw)
        fig.xaxis.axis_label = x_title
        fig.yaxis.axis_label = y_title
        getattr(fig, no_color_grid_direction).grid_line_color = None

        # Rotate category labels so they have more space
        if x_value in self.discrete:
            fig.xaxis.major_label_orientation = pd.np.pi / 4

        # Plot
        chart_type_info['fn'](fig, x_value, y_values, df, self.palette)

        # Tooltips
        tooltips = '''
        <div class="mytooltip" style="color:@color;">
            <ul>
                <li>{xname}: @{xname}</li>
                <li>@value_name: @value</li>
            </ul>
        </div>
        '''.format(xname=x_value)
        hover = HoverTool(tooltips=tooltips)
        fig.add_tools(hover)

        return fig


class BackgroundBokeh(threading.Thread):

    def run(self):
        bokeh_app = Application(FunctionHandler(Dashboard.generate))
        io_loop = IOLoop.current()
        server = Server({'/bkapp': bokeh_app}, io_loop=io_loop,
                        allow_websocket_origin=["localhost:8000"])
        server.start()
        io_loop.start()

    def stop(self):
        IOLoop.current().stop()


bokeh_server = BackgroundBokeh()


def start_server():
    print('> Starting Bokeh server')
    bokeh_server.start()


def stop_server():
    print('> Stopping Bokeh server')
    bokeh_server.stop()
