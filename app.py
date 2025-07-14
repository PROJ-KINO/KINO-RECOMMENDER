from flask import Flask

app = Flask(__name__)

@app.route("/")
def recommend():
    return "KINO Recommender API alive!"

if __name__ == "__main__":
    app.run(port=5001)