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
    formatted_ratings = [round(rating, 2) for rating in popular_df['avg_rating'].values]

    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=formatted_ratings)


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        if not user_input:
            return render_template('recommend.html',
                                   error="Please enter a book title, author, or publisher.")

        # Normalize input
        user_input = user_input.strip().lower()

        # Search across multiple fields
        matching_books = books[
            (books['Book-Title'].str.lower().str.contains(user_input, na=False)) |
            (books['Book-Author'].str.lower().str.contains(user_input, na=False)) |
            (books['Publisher'].str.lower().str.contains(user_input, na=False))
            ]

        if matching_books.empty:
            return render_template('recommend.html',
                                   error="No matches found. Please try another search term.")

        # Get unique book titles from matches that exist in pt index
        valid_titles = [title for title in matching_books['Book-Title'].unique()
                        if title in pt.index]

        if not valid_titles:
            return render_template('recommend.html',
                                   error="No recommendations available for these matches.")

        # Store original match details
        original_match = {
            'title': matching_books.iloc[0]['Book-Title'],
            'author': matching_books.iloc[0]['Book-Author'],
            'image': matching_books.iloc[0]['Image-URL-M']
        }

        # Get recommendations for each matching book
        all_recommendations = []
        seen_titles = set([original_match['title']])  # Avoid recommending the search match

        for book_title in valid_titles[:3]:  # Limit to first 3 matching books
            try:
                index = np.where(pt.index == book_title)[0][0]

                # Get similar books
                similar_items = sorted(list(enumerate(similarity_scores[index])),
                                       key=lambda x: x[1], reverse=True)[1:5]

                for i in similar_items:
                    temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                    if not temp_df.empty:
                        book_title = temp_df.iloc[0]['Book-Title']

                        # Skip if we've already seen this book
                        if book_title in seen_titles:
                            continue

                        item = [
                            book_title,
                            temp_df.iloc[0]['Book-Author'],
                            temp_df.iloc[0]['Image-URL-M']
                        ]
                        all_recommendations.append(item)
                        seen_titles.add(book_title)
            except Exception as e:
                print(f"Error processing book {book_title}: {str(e)}")
                continue

        if not all_recommendations:
            return render_template('recommend.html',
                                   error="Unable to generate recommendations at this time.")

        # Return both the matched book and recommendations
        return render_template('recommend.html',
                               match=original_match,
                               data=all_recommendations[:8],
                               search_term=user_input)

    except Exception as e:
        print(f"Error in recommend: {str(e)}")  # For debugging
        return render_template('recommend.html',
                               error="An error occurred while processing your request.")


if __name__ == '__main__':
    app.run(debug=True)
