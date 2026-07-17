import sqlite3
from pathlib import Path
from config import Config
from datetime import datetime


DB_PATH = Path(Config.DATABASE)


def init_database():
    """
    Comprova que existeix la carpeta data.
    La BD la crea automàticament SQLite quan cal.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """
    Retorna una connexió SQLite.
    """
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def query(sql, params=()):
    """
    SELECT que retorna una llista de diccionaris.
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def query_one(sql, params=()):
    """
    SELECT que retorna un únic registre.
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        row = cursor.fetchone()

    return dict(row) if row else None


def execute(sql, params=()):
    """
    INSERT / UPDATE / DELETE
    Retorna el lastrowid.
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.lastrowid


def execute_script(filename):
    """
    Executa un fitxer SQL complet.
    """
    filename = Path(filename)

    if not filename.is_absolute():
        filename = Path(Config.BASE_DIR) / filename

    with open(filename, "r", encoding="utf-8") as f:
        script = f.read()

    with get_connection() as conn:
        conn.executescript(script)
        conn.commit()


def table_exists(table_name):
    """
    Comprova si existeix una taula.
    """
    sql = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name=?
    """

    return query_one(sql, (table_name,)) is not None


def count(table_name):
    """
    Nombre de registres d'una taula.
    """
    sql = f"SELECT COUNT(*) AS total FROM {table_name}"

    row = query_one(sql)

    return row["total"]


def get_user(user_id):
    """
    Retorna un usuari.
    """
    return query_one(
        """
        SELECT *
        FROM users
        WHERE id=?
        """,
        (user_id,)
    )


def get_all_users():
    """
    Llista d'usuaris.
    """
    return query(
        """
        SELECT *
        FROM users
        ORDER BY role,name
        """
    )

def get_user_missions(user_id):

    return query(
        """
        SELECT

            ma.id AS assignment_id,

            ma.status,

            ma.assignment_type,

            ma.completed_by,

            ma.due_date,

            ma.assigned_date,

            m.id AS mission_id,

            m.title,

            m.description,

            m.icon,

            m.points,

            m.requires_validation,

            c.name AS category,

            c.color,

            c.icon AS category_icon,

            u.name AS completed_by_name


        FROM mission_assignments ma


        INNER JOIN missions m
            ON m.id = ma.mission_id


        INNER JOIN categories c
            ON c.id = m.category_id


        LEFT JOIN users u
            ON u.id = ma.completed_by


        WHERE ma.user_id = ?

          AND m.active = 1
          AND ma.status <> 'cancelled'


        ORDER BY
            CASE ma.status
                WHEN 'pending' THEN 1
                WHEN 'waiting_validation' THEN 2
                WHEN 'completed' THEN 3
                ELSE 4
            END,

            c.sort_order,

            m.title

        """,

        (user_id,)
    )

def complete_mission(assignment_id, user_id):
     print("ASSIGNMENT:", assignment_id)
     print("USER:", user_id)
     execute(
        """
        UPDATE mission_assignments
        SET
            status=?,
            completed_at=?,
            completed_by=?
        WHERE id=?
          AND user_id=?
          AND status='pending'
        """,
        (
            "waiting_validation",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            assignment_id,
            user_id
        )
    )
     
def get_waiting_validations():

    return query(
        """
        SELECT

            ma.id AS assignment_id,

            ma.status,

            ma.assignment_type,

            ma.completed_at,

            m.title as title,

            m.description,

            m.icon,

            m.points,

            c.name AS category,

            u.name AS gamer_name

        FROM mission_assignments ma

        INNER JOIN missions m
            ON m.id = ma.mission_id

        INNER JOIN categories c
            ON c.id = m.category_id

        INNER JOIN users u
            ON u.id = ma.user_id

        WHERE ma.status='waiting_validation'

        ORDER BY ma.completed_at
        """
    )
def approve_mission(assignment_id, admin_id):

    data = query_one(
        """
        SELECT
            ma.user_id,
            m.points
        FROM mission_assignments ma
        JOIN missions m
            ON m.id = ma.mission_id
        WHERE ma.id = ?
          AND ma.status = 'waiting_validation'
        """,
        (assignment_id,)
    )

    if not data:
        return False

    execute(
        """
        UPDATE mission_assignments
        SET
            status='completed',
            validated_at=?,
            validated_by=?
        WHERE id=?
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            admin_id,
            assignment_id
        )
    )

    execute(
        """
        UPDATE users
        SET points = points + ?
        WHERE id = ?
        """,
        (
            data["points"],
            data["user_id"]
        )
    )

    execute(
        """
        INSERT INTO points_history(
            user_id,
            mission_id,
            points,
            reason
        )
        VALUES(
            ?,
            (
                SELECT mission_id
                FROM mission_assignments
                WHERE id=?
            ),
            ?,
            'Mission completed'
        )
        """,
        (
            data["user_id"],
            assignment_id,
            data["points"]
        )
    )

    return True


def reject_mission(assignment_id):
    # Tornem la missió a 'pending' perquè el nen ho pugui tornar a intentar
    execute(
        """
        UPDATE mission_assignments
        SET status='pending', completed_at=NULL, completed_by=NULL
        WHERE id=?
        """,
        (assignment_id,)
    )

def count_waiting_validations():

    row = query_one(
        """
        SELECT COUNT(*) AS total
        FROM mission_assignments
        WHERE status='waiting_validation'
        """
    )

    return row["total"]

# ==========================
# MISSIONS
# ==========================

def get_all_missions():
   
    return query(
        """
        SELECT

            m.*,

            c.name AS category_name,

            c.icon AS category_icon,

            c.color AS category_color,

            mt.name AS mission_type

        FROM missions m

        INNER JOIN categories c
            ON c.id = m.category_id

        LEFT JOIN mission_types mt
            ON mt.id = m.mission_type_id

        ORDER BY

            c.sort_order,

            m.title
        """
    )

def get_mission(mission_id):

    return query_one("""
        SELECT *
        FROM missions
        WHERE id = ?
    """, (mission_id,))

def get_categories():

    return query("""
        SELECT *
        FROM categories
        ORDER BY name
    """)


def get_family_users(family_id=1):

    return query("""
        SELECT *
        FROM users
        WHERE family_id = ?
        ORDER BY role DESC, name
    """, (family_id,))