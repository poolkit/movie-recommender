import numpy as np
import pandas as pd
from flask import Flask, render_template, request, url_for, redirect

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = False

def create_sim():
    data = pd.read_csv('data.csv')
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    sim = cosine_similarity(count_matrix)
    return data,sim

def rcmd(m):
    m = m.lower()
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    if m not in data['movie_title'].unique():
        l=[]
        return l
    else:
        # getting the index of the movie in the dataframe
        i = data.loc[data['movie_title']==m].index[0]

        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

        # taking top 1- movie scores
        # not taking the first index since it is the same movie
        lst = lst[1:11]

        # making an empty list that will containg all 10 movie recommendations
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":
        return redirect(url_for('result', query=request.form['movie']))
    else:
        return render_template("base.html")

@app.route("/result/<query>", methods=['GET'])
def result(query):
    movie_recomm = rcmd(query)
    return render_template("result.html", list=movie_recomm)

if __name__ == "__main__":
    app.run(debug=True)
