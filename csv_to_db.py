import pandas as pd
from sqlalchemy import create_engine, text
from sshtunnel import SSHTunnelForwarder
from IPython.display import display


def get_ssh_db_connection(ssh_config):
    """
    Establish an SSH tunnel and connect to MySQL database through SQLAlchemy.
    """
    try:
        tunnel = SSHTunnelForwarder(
            (ssh_config['ssh_host'], 22),
            ssh_username=ssh_config['ssh_user'],
            ssh_password=ssh_config['ssh_password'],
            remote_bind_address=(ssh_config['remote_host'], ssh_config['remote_port'])
        )
        tunnel.start()

        engine = create_engine(
            f"mysql+pymysql://{ssh_config['mysql_user']}:{ssh_config['mysql_password']}@127.0.0.1:{tunnel.local_bind_port}/{ssh_config['mysql_db']}"
        )

        return tunnel, engine
    except Exception as e:
        print(f"Error establishing SSH tunnel or database connection: {e}")
        return None, None


def clean_and_validate_timestamps(df):
    """
    Clean and validate the Timestamp column in the DataFrame.
    Replace invalid or missing timestamps with the current datetime.
    """
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['Timestamp'].fillna(pd.Timestamp.now(), inplace=True)
    return df


def get_or_create_platform_id(connection, platform_name):
    """
    Retrieve the PlatformID for a platform name. Insert it if it doesn't exist.
    """
    platform_query = text("SELECT PlatformID FROM Platform WHERE PlatformName = :platform_name")
    platform_result = connection.execute(platform_query, {"platform_name": platform_name}).fetchone()

    if platform_result is None:
        insert_platform_query = text("INSERT INTO Platform (PlatformName) VALUES (:platform_name)")
        connection.execute(insert_platform_query, {"platform_name": platform_name})
        platform_result = connection.execute(platform_query, {"platform_name": platform_name}).fetchone()

    return platform_result[0]


def insert_post_data(connection, df, platform_id):
    """
    Insert post data into Hub_Post, Sat_PostDetails, and Link_PostPlatform tables.
    """
    for _, row in df.iterrows():
        # Insert into Hub_Post
        hub_post_query = text("INSERT INTO Hub_Post (PlatformID, Timestamp) VALUES (:platform_id, :timestamp)")
        connection.execute(hub_post_query, {"platform_id": platform_id, "timestamp": row['Timestamp']})

        # Get the generated PostID
        post_id = connection.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]

        # Insert into Sat_PostDetails
        post_details_query = text("""
            INSERT INTO Sat_PostDetails (PostID, Username, PostContent, NumberOfLikes)
            VALUES (:post_id, :username, :post_content, :number_of_likes)
        """)
        connection.execute(post_details_query, {
            "post_id": post_id,
            "username": row['Username'],
            "post_content": row['PostContent'],
            "number_of_likes": row['NumberOfLikes']
        })

        # Insert into Link_PostPlatform
        link_query = text("INSERT INTO Link_PostPlatform (PostID, PlatformID) VALUES (:post_id, :platform_id)")
        connection.execute(link_query, {"post_id": post_id, "platform_id": platform_id})


def csv_to_database(engine, csv_file_path, column_mapping):
    """
    Read data from a CSV file and upload it to the database tables.
    """
    try:
        df = pd.read_csv(csv_file_path)
        df.columns = [column_mapping.get(col, col) for col in df.columns]
        df['post_id'] = range(1, len(df) + 1)
        df = df.sample(n=10, random_state=42)
        print(df)
        # Print the DataFrame column names
        print(df.columns)
        #print(df.head())
        df = clean_and_validate_timestamps(df)

        # Prompt for platform selection
        platforms = ['reddit', 'bluesky', 'twitter', 'youtube']
        print("Select the platform for this CSV file:")
        for i, platform in enumerate(platforms, start=1):
            print(f"{i}: {platform}")

        while True:
            try:
                choice = int(input("Enter the number for the platform: "))
                if 1 <= choice <= len(platforms):
                    selected_platform = platforms[choice - 1]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid choice. Please enter a number from the list.")

        with engine.connect() as connection:
            with connection.begin() as transaction:
                platform_id = get_or_create_platform_id(connection, selected_platform)
                insert_post_data(connection, df, platform_id)

    except Exception as e:
        print(f"Error processing CSV file: {e}")


if __name__ == "__main__":
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

    csv_file_path = 'CSV_data/fulldata.csv'
    column_mapping = {
        "post_id": "PostID",
      
        "username": "Username",
        "comment": "PostContent",
        "time": "Timestamp",
        "likes": "NumberOfLikes",
        
        "Platform Name": "PlatformName"
    }

    tunnel, engine = get_ssh_db_connection(ssh_config)

    if engine:
        try:
            csv_to_database(engine, csv_file_path, column_mapping)
        finally:
            engine.dispose()

    if tunnel:
        tunnel.stop()