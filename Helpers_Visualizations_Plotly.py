# =============================================================================
# HELPERS FOR PLOTTING WITH PLOTLY START
# =============================================================================

# Plotly
import plotly.io as pio
pio.renderers.default='browser'
##pio.renderers.default='svg'
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px

## WRAPPERS
def udf_univariate_count_plotly_plot_wrapper(s_variable,df):
    udf_univariate_count_plotly_plot(df,s_variable)


def udf_bivariate_count_plotly_plot_wrapper(s_variable,df):
    udf_bivariate_count_plotly_plot(s_variable,'TARGET',df)


def udf_univariate_scatter_plotly_wrapper(s_variable,df,sort_switch = True):
    udf_univariate_scatter_plotly_plot(df,s_variable,sort_switch = True)

def udf_univariate_hist_plotly_wrapper(s_variable,df):
    udf_univariate_hist_plotly_plot(df,s_variable)
    
    
''' November 14 2021 , plot a run chart r temporal line chart
    x is datetime and y is variable '''
def udf_univariate_line_plotly_plot(df,x_variable,y_variable,s_title):
    fig = px.line(df, x=x_variable, y=y_variable)
    fig.update_layout(title_text=s_title)
    fig.show()


def udf_bivariate_line_plotly_plot(df,x_variable,y_variable_from, y_variable_to,s_title):
    fig = px.line(df, x=x_variable, y=df.columns[y_variable_from:y_variable_to])
    fig.update_layout(title_text=s_title)
    fig.show()
        
    
    

def udf_univariate_hist_plotly_plot(df,s_variable):
    x = z = df[s_variable].values
    fig = go.Figure(data=[go.Histogram(x=x)])
    fig.update_layout(title_text=s_variable)
    fig.show()



def udf_univariate_dist_plotly_plot(df,s_variable):
    group_labels= [s_variable]
    ll = [df[s_variable].values.tolist()]
    fig = ff.create_distplot(ll,group_labels)
    fig.show()


def udf_univariate_scatter_plotly_plot(df,s_variable,sort_switch = True):   
    '''Use this function to plot unique value scatter plot'''
    #pio.renderers.default = 'svg'
    pio.renderers.default = 'browser'
    
    '''Choose to sort or not '''
    '''Sorting makes it easier to identify outliers especially with big data sets'''
    
    
    if sort_switch ==True:
        ##z = df[s_variable].value_counts().sort_index()
        z = df.sort_values(by=s_variable, ascending=True)[s_variable]
        x = np.arange((z.shape[0]) -1)
        ##x = z.index[::1]
        y = z.values[::1]
    else:     
       z = df[s_variable]
       x = z.index[::1]
       y = z.values[::1]
    
    n = df[s_variable].unique()

    num_colors = len(n)
    colors = udf_random_color_generator(num_colors)


    fig = go.Figure(data=[
        go.Scatter(x=x,  y=y,mode='markers')])
    # Change the bar mode
    fig.update_layout(title_text=s_variable)
    fig.show()



def udf_bivariate_hist_plotly_plot(df,s_variable,s_target,aggr_func):
    pio.renderers.default = 'browser'
    fig = px.histogram(df, x=s_variable, 
                       y=s_target, 
                       color=s_target,marginal="box", # or violin, rug,box
                       ##color_discrete_map={1: "red", 0: "green"},
                       title=s_target  + " by " +  s_variable,
                       histfunc=aggr_func, 
                       hover_data=df.columns)
    fig.show()


def udf_bivariate_hist_go_plotly_plot(df,s_variable,s_target):
    
    
    x1 = df[df[s_target] == 1][s_variable].values.tolist()
    x2 = df[df[s_target] == 0][s_variable].values.tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x1,
        name='Not Repaid', # name used in legend and hover labels
        ##marker_color='darkred', 
        marker_color='darkmagenta',
        ##marker=dict(color='rgba(171, 50, 96, 0.6)'),
        opacity=1.0
    ))
    

    fig.add_trace(go.Histogram(
        x=x2,
        name='Repaid', # name used in legend and hover labels
        ##marker_color='black',
        marker_color='darkmagenta',
        ##marker=dict(color='rgba(12, 50, 196, 0.6)'),
        opacity=0.65
    ))
    

    fig.update_layout(
        title_text=s_target + " by " + s_variable, # title of plot
        xaxis=dict(title=s_variable),
        yaxis=dict( title='Count')
    )
    
    fig.show()



def udf_bivariate_dist_plotly_plot(df,s_variable,s_target):
    pio.renderers.default = 'browser'

    x1 = df[df[s_target] == 1][s_variable].values.tolist()
    print (x1)
    x2 = df[df[s_target] == 0][s_variable].values.tolist()
    group_labels = ['Not Repaid', 'Repaid']
    
    colors = ['magenta','black']
    
    
    hist_data = [x1, x2]
    fig = ff.create_distplot(hist_data, group_labels,colors=colors,histnorm = 'probability')
    fig.update_layout(title_text=s_variable)
    fig.show()



def udf_bivariate_count_plotly_plot(s_variable,s_target,df):
    '''Use this function to plot unique value counts for two categorical features'''
    #pio.renderers.default = 'svg'
    pio.renderers.default = 'browser'
    
    n = df[s_variable].unique()
    print(len(n))
    num_colors = len(n)
    colors = udf_random_color_generator(num_colors)


    z = df[[s_variable, s_target]].groupby([s_variable], as_index=False).mean().sort_values(by=s_variable)
    x = z[s_variable].values[::1]
    y = z[s_target].values*100
    y = np.round(y,2)
    
    fig = go.Figure(data=[
        go.Bar(x = x, y = y,
                marker_color=colors,
                )])
    # Change the bar mode
    fig['layout']['yaxis1'].update(range=[0, 100])
    fig.update_layout(title_text=s_variable + ' Percentage')
    fig.show()
    
    
    
    

    
def udf_univariate_count_plotly_plot(df,s_variable):   
    '''Use this function to plot unique value counts for one categorical features'''
    #pio.renderers.default = 'svg'
    pio.renderers.default = 'browser'
    ## Sorting is very important , otherwise there is inconsistencies between x and y values
    z = df[s_variable].value_counts().sort_index()
    x = z.index[::1]
    y = z.values[::1]
    
    n = df[s_variable].unique()

    num_colors = len(n)
    colors = udf_random_color_generator(num_colors)

    # colors = ['lightslategray',] * 5
    # colors[1] = 'green'
    # print(colors)

    
    fig = go.Figure(data=[
        go.Bar(x=x,  y=y,
                marker_color=colors
                ##,hovertext=[a0, a1 ]
                )])
    # Change the bar mode
    fig.update_layout(title_text=s_variable)
    fig.show()
        



## Random color generator
def udf_random_color_generator(number_of_colors):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
    return color

# =============================================================================
# HELPERS FOR PLOTTING WITH PLOTLY END
# =============================================================================
    


