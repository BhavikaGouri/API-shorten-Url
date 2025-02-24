from flask import Flask, request, jsonify, redirect
import hashlib
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("new2.db", check_same_thread=False)
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS urls(long_url, short_url)')
con.commit()


def generate_code(LongUrl):
    hashed = hashlib.md5()
    hashed.update(LongUrl.encode())
    ShortCode = hashed.hexdigest()[:7]
    return ShortCode


@app.route('/')
def home():
    return '<h2>Pass the url as the endpoint</h2>'


@app.route('/shorten', methods=['GET'])
def shorten():
    long_url = request.args.get('long_url')
    if not long_url:
        return jsonify({'error': 'No arguments provided'})

    short_code = generate_code(long_url)
    cur.execute('INSERT INTO urls (long_url, short_url) VALUES(?, ?)', (long_url, short_code))
    con.commit()
    # con.close()
    return jsonify({'short_url_code': f"{short_code}"})


@app.route('/<shortcode>')
def find(shortcode):
    if not shortcode:
        return jsonify({'error': 'No short code  provided'})
    cur.execute('SELECT long_url from urls WHERE short_url = ?', (shortcode,));
    original_url = cur.fetchone()
    con.commit()
    if original_url:
        con.close()
        return redirect(original_url[0])
    else:
        return jsonify({'error': 'URL not listed in the database'})


if __name__ == '__main__':
    app.run(debug=True)
