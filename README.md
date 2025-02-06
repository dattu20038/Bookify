#  Bookify

**Bookify** is a **Machine Learning-based web application** that recommends books based on **popularity** and **collaborative filtering**. Users can view popular books and get personalized book recommendations by entering their favorite book titles.

##  Features
* **Home Page**: Displays the most popular books with details such as title, author, cover image, number of votes, and average rating.
* **Recommendation Page**: Accepts user input and recommends similar books based on collaborative filtering.

##  Tech Stack
* **Frontend**: HTML, CSS, Bootstrap
* **Backend**: Flask (Python)
* **Database**: Pickle files for pre-processed data
* **Libraries Used**:
  * `Flask`
  * `NumPy`
  * `Pandas`

##  Project Structure
```bash
📁 Bookify
├── 📄 README.md        # Project documentation
├── 📄 app.py          # Main Flask application
├── 📄 book.ipynb      # Data processing notebook
├── 📄 index.html      # Home page template
└── 📄 recommend.html  # Recommendation page template
```

##  How to Run the Project
1. Clone this repository:
```bash
git clone https://github.com/your-username/bookify.git
cd bookify
```

2. Install the required libraries:
```bash
pip install flask pandas numpy
```

3. Run the Flask app:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

##  Requirements
* Python 3.x
* Flask
* Pandas
* NumPy
