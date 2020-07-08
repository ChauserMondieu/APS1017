from .DBFeeder import *


class DataMain:
    ADD_TABLE = False
    host = "192.168.5.12"
    port = 3306
    user = "develop"
    password = "APS1017s"
    database = "aps1017"
    charset = "utf8"

    if __name__ == "__main__":
        # instantiate class DBFeeder
        db = DBFeeder()
        base = os.path.dirname(os.getcwd())
        dat_name = r"dat\APS1017 Order data for Project.csv"
        dir = os.path.join(base, dat_name)
        conn = db.db_connect(host, port, user, password, database, charset)
        if ADD_TABLE is True:
            db.data_feeder(conn, dir)
            db.data_washer(conn)
            db.data_backup(conn)
        db.data_dispatcher(conn)
