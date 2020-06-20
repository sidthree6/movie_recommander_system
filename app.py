import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://raw.githubusercontent.com/Group-7-Big-Data/Assignment-1/master/ratings.csv')
mv_t = pd.read_csv('https://raw.githubusercontent.com/Group-7-Big-Data/Assignment-1/master/movies.csv')
df = pd.merge(df,mv_t,on='movieId')

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['Ratings Count'] = pd.DataFrame(df.groupby('title')['rating'].count())

mv_matrix = df.pivot_table(index='userId',columns='title',values='rating')

def getRecommendation(name, num= 10, matrix=mv_matrix):
    movie = matrix[name]
    
    #Using corrwith() to get correlations of the following pandas series
    movie_one = matrix.corrwith(movie)
    
    #Clening the data further to remove NaN values
    corr_movie = pd.DataFrame(movie_one, columns=['Correlation'])
    corr_movie.dropna(inplace=True)
    
    #Now we can sort the dataframe by correlation so we can get the similar movies
    #corr_movie.sort_values('Correlation', ascending = False)
    
    # Joining Ratings Count to corr_Forrest_Gump dataframe
    corr_movie = corr_movie.join(ratings['Ratings Count'])
    
    #Filtering out movies that have less than 100 reviews, as it will make a lot more sense
    corr_movie = corr_movie[corr_movie['Ratings Count']>100].sort_values('Correlation',ascending=False).head(num+1)
    
    # Removing first row, because its the movie itself
    corr_movie = corr_movie.iloc[1:]
    
    # Dropping Ratings count column (we dont need it)
    corr_movie = corr_movie.drop('Ratings Count', 1)
    corr_movie = corr_movie.reset_index()
    
    return corr_movie

server = app.server

movieOptions = df.title.unique()

app.layout = html.Div([
    html.H2('Recommending Movies (Select Movies from dropdown)'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in movieOptions],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    recommand = getRecommendation(value, num=10)
    output = []
    output.append(html.P())
    output.append(html.P())
    output.append(html.P('Recommended movie based on : {}\n\n'.format(value)))
    num = 1
    for i in recommand['title']:
        output.append(html.P('{}) {}'.format(num, i)))
        num=num+1
    
    return output

if __name__ == '__main__':
    app.run_server(debug=True)