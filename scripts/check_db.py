import pymysql.cursors
import subprocess
from multiprocessing import Process


def check_if_create_db(connection):
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            check_table_sql = "select count(*) from rulemanager.auth_user;"
            try:
                cursor.execute(check_table_sql)
            except Exception as err:
                if err.args[0] == 1146:
                    print("rulemanager not create ,will be init db")
                    create_db = "create database if not exists rulemanager"
                    cursor.execute(create_db)
                    return False
            return True


def init_db():
    makemigrations = "cd /data/server/rulemanager;python manage.py makemigrations"
    migrate = "cd /data/server/rulemanager;python manage.py  migrate"
    subprocess.run(makemigrations, timeout=60, shell=True)
    subprocess.run(migrate, timeout=60, shell=True)


if __name__ == "__main__":
    connection = pymysql.connect(host='mysqldb',
                                 user='root',
                                 password='my-secret-Pw03',
                                 database='',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    check_if_exists = check_if_create_db(connection)
    if check_if_exists is False:
        # init rulemanager table
        init_db()
        print("rulemanager db init success")
    else:
        print("rulemanager db already init")
    # start rulemanager

