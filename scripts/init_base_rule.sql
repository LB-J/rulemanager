import pymysql.cursors


connection = pymysql.connect(host='mysqldb',
                             user='root',
                             password='my-secret-Pw03',
                             database='rulemanager',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new rule group
        new_group = "insert into rule_rulegroup "
        try:
            cursor.execute(check_table_sql)
        except Exception as err:
            if err.args[0] == 1146:
                print("rulemanager not create ,will be init db")
                create_db = "create database if not exists rulemanager"
                cursor.execute(create_db)
                return False
        return True