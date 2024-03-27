from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, session
import psycopg2
import psycopg2.extras
from decouple import config

app = Flask(__name__)
app.secret_key = config('secret_key')
# Database connection parameters
DB_HOST = "dpg-co0h3g779t8c73d9qpcg-a.singapore-postgres.render.com"
DB_NAME = "somusic"
DB_USER = "somusic_user"
DB_PASS = config('DB_PASS')

# Connect to your postgres DB

@app.route('/', methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/participant-details', methods=['POST', 'GET'])
def submit_survey():

    if request.method == "POST":
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

        data = request.form
        name = data.get('name')
        age = data.get('age')
        # Music genres could be multiple selections
        music_genres = request.form.getlist('musicGenre')
        # Serialize array data into string; consider using JSON format or similar in a real app
        music_genres_str = ','.join(music_genres)
        # Assume you have a table `survey_responses`
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



        # Insert data into the database
        cur.execute("INSERT INTO registration_details (name, age, music_genres) VALUES (%s, %s, %s) RETURNING id;",
                    (name, age, music_genres_str))
        id_number = int(cur.fetchone()[0])

        print ("id_number is", id_number)
        conn.commit()  # Commit the transaction
        cur.close()
        session['id_in_session'] = id_number
        conn.close()
        return redirect(url_for('music_preference'))
    else:
        return render_template("participant-details.html")

@app.route('/music-preference', methods=['POST', 'GET'])
def music_preference():
    id_number = session.get('id_in_session')
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)



    print("id of music_preference is", id_number)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT music_genres from registration_details WHERE id = %s", (id_number, ))

    music_genre=cur.fetchone()[0]
    print ("music_genre is", music_genre)
    if request.method == "POST":
        data=request.form
        arithmetic1 = data.get("arithmetic1")
        arithmetic2 = data.get("arithmetic2")
        arithmetic3 = data.get("arithmetic3")
        reading1 = data.get("reading1")
        reading2 = data.get("reading2")
        reading3 = data.get("reading3")
        reading4 = data.get("reading4")
        reading5 = data.get("reading5")
        elapsed_time = data.get("elapsed_time")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("INSERT INTO part1_answers (id, ar1, ar2, ar3, r1, r2, r3, r4, r5, elapsed_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    (id_number, arithmetic1, arithmetic2, arithmetic3, reading1, reading2, reading3, reading4, reading5, elapsed_time))
        conn.commit()
        cur.close()

        print ("elapsed_time is", elapsed_time)

        conn.close()
        return redirect(url_for('random_music'))
    else:
        return render_template("music-preference.html", music_genre=music_genre)

@app.route('/random-music', methods = ['POST', 'GET'])
def random_music():
    id_number = session.get('id_in_session')

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT music_genres from registration_details WHERE id = %s", (id_number,))

    music_genre = cur.fetchone()[0]

    if request.method == "POST":
          data = request.form

          arithmetic4 = data.get("arithmetic4")
          arithmetic5 = data.get("arithemtic5")
          reading6 = data.get("reading6")
          reading7 = data.get("reading7")
          reading8 = data.get("reading8")
          reading9 = data.get("reading9")
          reading10 = data.get("reading10")
          elapsed_time = data.get("elapsed_time")

          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          cur=conn.cursor()
          cur.execute(
              "INSERT INTO part2_answers (id, ar4, ar5, r6, r7, r8, r9, r10, elapsed_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
              (id_number, arithmetic4, arithmetic5, reading6, reading7, reading8, reading9, reading10, elapsed_time))
          conn.commit()
          cur.close()
          conn.close()
          return redirect(url_for('close'))

    else:
        return render_template("music-random.html", music_genre=music_genre)

@app.route('/thankyou', methods=['POST', 'GET'])
def close():
    score_user = 0
    id_number = session.get('id_in_session')

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()

    cur.execute("SELECT ar1, ar2, ar3, r1, r2, r3, r4, r5 FROM part1_answers WHERE id = %s", (id_number, ))

    part1_answers_list = cur.fetchall()[0]

    if part1_answers_list[0] == 'B':
        score_user += 1
    if part1_answers_list[1] == 'A':
        score_user += 1
    if part1_answers_list[2] == 'A':
        score_user += 1
    if part1_answers_list[3] == 'A':
        score_user += 1
    if part1_answers_list[4] == 'B':
        score_user += 1
    if part1_answers_list[5] == 'B':
        score_user += 1
    if part1_answers_list[6] == 'A':
        score_user += 1
    if part1_answers_list[7] == 'B':
        score_user += 1

    cur.execute("SELECT ar4, ar5, r6, r7, r8, r9, r10 FROM part2_answers WHERE id = %s", (id_number, ))

    part2_answers_list = cur.fetchall()[0]

    if part2_answers_list[0] == 'A':
        score_user += 1
    if part2_answers_list[1] == 'A':
        score_user += 1
    if part2_answers_list[2] == 'B':
        score_user += 1
    if part2_answers_list[3] == 'C':
        score_user += 1
    if part2_answers_list[4] == 'A':
        score_user += 1
    if part2_answers_list[5] == 'B':
        score_user += 1
    if part2_answers_list[6] == 'A':
        score_user += 1


    if request.method == "POST":

        data = request.form

        feedback = data.get('feedback')

        cur.execute("INSERT INTO feedback (id, feedback_received) VALUES (%s, %s);", (id_number, feedback))

    cur.close()
    conn.close()
    return render_template("thankyou.html", score_user = score_user)

def main():
    app.run(port = 10000)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
