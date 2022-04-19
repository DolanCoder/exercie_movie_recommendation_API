import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_data():
    '''get_data() is used to fetch the data about the movies and return the dataset with its attributes as the result for further preprocessing.'''
    movie_data = pd.read_csv('data/movie_data.csv.zip')
    movie_data['original_title'] = movie_data['original_title'].str.lower()
    return movie_data

def combine_data(data):
    '''combine_data() drops the columns not required for feature extraction and then combines the cast and genres column, finally returning the combine column as the result of this function.'''
    data_recommend = data.drop(columns=['movie_id', 'original_title','plot'])
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:2]].apply(
                                                                    lambda x: ','.join(x.dropna().astype(str)),axis=1)
    
    data_recommend = data_recommend.drop(columns=[ 'cast','genres'])
    return data_recommend
        
def transform_data(data_combine, data_plot):
    '''transform_data() takes the value returned by combine_data() and the plot column from get_data() and applies CountVectorizer and TfidfVectorizer respectively and calculates the Cosine values.'''
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data_combine['combine'])

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data_plot['plot'])

    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    
    return cosine_sim


def recommend_movies(title, data, combine, transform):
    indices = pd.Series(data.index, index = data['original_title'])
    index = indices[title]



    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]


    movie_indices = [i[0] for i in sim_scores]

    movie_id = data['movie_id'].iloc[movie_indices]
    movie_title = data['original_title'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(columns=['Name', 'Genres'])

    recommendation_data['Name'] = movie_title
    recommendation_data['Genres'] = movie_genres

    return recommendation_data

def results(movie_name):
        movie_name = movie_name.lower()

        find_movie = get_data()
        combine_result = combine_data(find_movie)
        transform_result = transform_data(combine_result,find_movie)

        if movie_name not in find_movie['original_title'].unique():
                return 'Movie not in Database'

        else:
                recommendations = recommend_movies(movie_name, find_movie, combine_result, transform_result)
                return recommendations.to_dict('records')
