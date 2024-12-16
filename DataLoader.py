# %%

import pandas as pd
from sqlalchemy import create_engine, text
from sshtunnel import SSHTunnelForwarder
from datetime import datetime

def get_ssh_db_connection():

    ssh_config = {
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
    try:
        print("Starting SSH tunnel...")
        tunnel = SSHTunnelForwarder(
            (ssh_config['ssh_host'], 22),
            ssh_username=ssh_config['ssh_user'],
            ssh_password=ssh_config['ssh_password'],
            remote_bind_address=(ssh_config['remote_host'], ssh_config['remote_port'])
        )
        
        tunnel.start()
        print(f"SSH Tunnel established. Local bind port: {tunnel.local_bind_port}")

        engine = create_engine(
            f"mysql+pymysql://{ssh_config['mysql_user']}:{ssh_config['mysql_password']}@127.0.0.1:{tunnel.local_bind_port}/{ssh_config['mysql_db']}"
        )

        print("Database connection established.")
        return tunnel, engine
    except Exception as e:
        print(f"Error establishing SSH tunnel or connecting to MySQL: {e}")
        return None, None


def query_posts(engine, platforms=None, start_date=None, end_date=None, topic=None, limit=None):
    """
        FORMAT OF THE FUNCTION CALL
     posts = query_posts(
                engine,
                platforms=["bluesky", "twitter"],
                start_date="2023-01-01",
                end_date="2023-12-31",
                topic="",
                limit=10000
            )
    """


    """
    Query posts from the database based on platform, date range, topic, and limit.
    """
    """
    try:
        get_ssh_db_connection()    
    except Exception as e:
        print(f"error getting ssh connection: {e}")
        return []
    """

    try:
        query = """
            SELECT 
                hp.PostID, 
                p.PlatformName, 
                hp.Timestamp, 
                spd.Username, 
                spd.PostContent, 
                spd.NumberOfComments, 
                spd.NumberOfLikes, 
                spd.NumberOfReposts, 
                spd.URL, 
                spd.SearchedTopic
            FROM Hub_Post hp
            JOIN Platform p ON hp.PlatformID = p.PlatformID
            JOIN Sat_PostDetails spd ON hp.PostID = spd.PostID
            WHERE 1 = 1
        """

        # Dynamic filtering conditions
        params = {}
        if platforms:
            print(platforms)
            # Generate placeholders for IN clause dynamically
            placeholders = ", ".join([f":platform_{i}" for i in range(len(platforms))])
            query += f" AND p.PlatformName IN ({placeholders})"
            
            # Add platforms to the params dictionary
            for i, platform in enumerate(platforms):
                params[f"platform_{i}"] = platform
        if start_date:
            query += " AND hp.Timestamp >= :start_date"
            params['start_date'] = start_date
        if end_date:
            query += " AND hp.Timestamp <= :end_date"
            params['end_date'] = end_date
        if topic:
            query += " AND spd.SearchedTopic = :topic"
            params['topic'] = topic
        if limit:
            query += " LIMIT :limit"
            params['limit'] = limit
        
        # Execute the query
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            # Convert rows to dictionaries
            df = [row._mapping for row in result]
            df = pd.DataFrame(df)
            return df  # Use _mapping for dictionary-like access

    except Exception as e:
        print(f"Error querying data: {e}")
        return []







# %%



