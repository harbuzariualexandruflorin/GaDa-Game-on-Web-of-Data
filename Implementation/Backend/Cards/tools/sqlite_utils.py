import sqlite3

HIGH_SCORE_DB = "data/users/high_scores.db"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as ex:
        print("SQLITE CONNECTION EXCEPTION: ", ex)
    return conn


def insert_high_score(user_name, score):
    with create_connection(HIGH_SCORE_DB) as conn:
        curs = conn.cursor()
        curs.execute(
            '''
                INSERT INTO high_scores(user_name, score)
                VALUES(?,?)
            ''',
            (user_name, score)
        )
        conn.commit()


def create_table_high_scores():
    with create_connection(HIGH_SCORE_DB) as conn:
        curs = conn.cursor()
        curs.execute(
            '''
                CREATE TABLE IF NOT EXISTS "high_scores" (
                    "user_name"	TEXT NOT NULL UNIQUE,
                    "score"	INTEGER NOT NULL,
                    PRIMARY KEY("user_name"),
                    CONSTRAINT "CHECK_SCORE" CHECK(score >= 0),
                    CONSTRAINT "CHECK_NAME" CHECK(LENGTH(user_name) > 0)
                )
            '''
        )


def clear_table_high_score():
    with create_connection(HIGH_SCORE_DB) as conn:
        curs = conn.cursor()
        curs.execute('DELETE FROM "high_scores"')


def read_table_high_scores(page_offset, page_size):
    scores = []
    with create_connection(HIGH_SCORE_DB) as conn:
        curs = conn.cursor()
        curs.execute(
            '''
                SELECT * FROM high_scores
                ORDER BY score DESC
                LIMIT %s
                OFFSET %s
            ''' % (page_size, page_offset)
        )

        for u, s in curs.fetchall():
            scores.append({"user_name": u, "score": s})
    return scores
