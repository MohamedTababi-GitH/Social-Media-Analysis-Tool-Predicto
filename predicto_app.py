from flask import Flask, request,g, jsonify
from TrendAnalyzer import analyze_frequency_modin, get_top_topics
from DataLoader import get_ssh_db_connection, query_posts
from sqlalchemy import create_engine, text
from sshtunnel import SSHTunnelForwarder
from datetime import datetime
from API_Handler import API_Handler
from youtubeAPI import getCommentDataMaster  # Import the function
import pandas as pd


app = Flask(__name__)

app.config['ssh_config'] = {
    'ssh_host': '141.59.26.123',
        'ssh_user': 'tektmu01',
        'ssh_password': 'thu123!',
        'remote_host': '127.0.0.1',
        'remote_port': 3306,
        'mysql_user': 'root',
        'mysql_password': 'socialmedia',
        'mysql_db': 'Predicto'
}

"""
Establish an SSH tunnel and connect to MySQL database through SQLAlchemy.
"""

# API Handler initialization
handler = API_Handler()

def get_ssh_db_connection():
    if 'db_engine' not in g:
        ssh_config = app.config['SSH_CONFIG']

        # Start SSH tunnel
        g.tunnel = SSHTunnelForwarder(
            (ssh_config['ssh_host'], 22),
            ssh_username=ssh_config['ssh_user'],
            ssh_password=ssh_config['ssh_password'],
            remote_bind_address=(ssh_config['remote_host'], ssh_config['remote_port'])
        )
        g.tunnel.start()

        # Create database engine
        g.db_engine = create_engine(
            f"mysql+pymysql://{ssh_config['mysql_user']}:{ssh_config['mysql_password']}@127.0.0.1:{g.tunnel.local_bind_port}/{ssh_config['mysql_db']}"
        )
    return g.tunnel, g.db_engine

# Clean up after each request
@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database connection and SSH tunnel when the app context ends."""
    tunnel = g.pop('tunnel', None)
    db_engine = g.pop('db_engine', None)
    if db_engine:
        db_engine.dispose()
    if tunnel:
        tunnel.stop()

@app.route('/api/reddit_posts', methods=['POST'])
def fetch_reddit_post():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify ("error"), 400
    try:
        post = handler.fetch_reddit_post(url=url)
        return jsonify({
            "title":post.title,
            "selftext": post.selftext,
            "author": str(post.author),
            "score": post.score
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bsky_posts', methods=['POST'])
def fetch_bsky_posts():
    data = request.json
    query = data.get('query', '')
    limit = data.get('limit', 10)
    try:
        posts = handler.fetch_bsky_posts(query=query, limit=limit)
        return jsonify([{"text": post.record.text, "author": post.author.did} for post in posts])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/youtube_comments', methods=['POST'])
def youtube_comments():
    try:
        data = request.json
        topic = data.get('topic')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        number_of_data = data.get('number_of_data', 100)  #to be modified for user input
        
        if not all([topic, start_date_str, end_date_str]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Convert dates to datetime objects
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        
        comments_df = getCommentDataMaster(topic, start_date, end_date, number_of_data)

        # Convert DataFrame to JSON
        comments_json = comments_df.to_dict(orient='records')
        return jsonify(comments_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/trend_analysis', methods=['POST'])
def trend_analysis():
    data = request.json
    try:
        df = pd.DataFrame(data.get('data', []))
        topics = data.get('topics', [])
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        
        monthly_counts, total_counts = analyze_frequency_modin(df, topics, start_date, end_date)
        
        return jsonify({
            "monthly_counts": monthly_counts.to_dict(orient='records'),
            "total_counts": total_counts.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Top Topics
@app.route('/api/top_topics', methods=['POST'])
def top_topics():
    data = request.json
    try:
        df = pd.DataFrame(data.get('data', []))
        column = data.get('column', 'PostContent')
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        top_n = data.get('top_n', 10)

        # Get top topics
        top_topics_df = get_top_topics(df, column, start_date, end_date, top_n)
        
        return jsonify(top_topics_df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
