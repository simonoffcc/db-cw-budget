import pg8000
from contextlib import contextmanager
import configparser

class DBManager:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        db_config = config['database']
        self.conn = pg8000.connect(
            database=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=int(db_config['port'])
        )

    @contextmanager
    def get_cursor(self):
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
