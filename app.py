from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Load preprocessed data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                         book_name=list(popular_df['Book-Title'].values),
                         author=list(popular_df['Book-Author'].values),
                         image=list(popular_df['Image-URL-M'].values),
                         votes=list(popular_df['num_ratings'].values),
                         rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        if not user_input:
            return render_template('recommend.html', error="Please enter a book title.")
        
        # Normalize input
        user_input = user_input.strip().lower()
        
        # Create a normalized version of pt.index for comparison
        normalized_index = pt.index.str.strip().str.lower()
        
        # Find exact or partial matches
        matching_titles = [title for title in pt.index 
                         if user_input in title.strip().lower()]
        
        if not matching_titles:
            return render_template('recommend.html', 
                                error="Book not found. Please try another title.")
        
        # Use the first matching title
        book_title = matching_titles[0]
        index = np.where(pt.index == book_title)[0][0]
        
        # Get similar books
        similar_items = sorted(list(enumerate(similarity_scores[index])), 
                             key=lambda x: x[1], reverse=True)[1:5]
        
        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            if not temp_df.empty:
                item = [
                    temp_df.iloc[0]['Book-Title'],
                    temp_df.iloc[0]['Book-Author'],
                    temp_df.iloc[0]['Image-URL-M']
                ]
                data.append(item)
        
        if not data:
            return render_template('recommend.html', 
                                error="Unable to generate recommendations at this time.")
        
        return render_template('recommend.html', data=data)
    
    except Exception as e:
        print(f"Error in recommend: {str(e)}")  # For debugging
        return render_template('recommend.html', 
                             error="An error occurred while processing your request.")

if __name__ == '__main__':
    app.run(debug=True)
