import random
import pymysql

# 👇 Importa tu inicialización de Firebase
from firebase.firebase_init import get_firebase_db

# ==========================
# CONFIG MySQL
# ==========================
mysql_conn = pymysql.connect(
    host="localhost",
    user="root",
    password="JadenKugo2119$&?",
    database="ddbb_antares_project",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

# ==========================
# Datos de ejemplo
# ==========================
fake_users = [
    ("admin_user", "admin1@example.com", "hash_admin", "Administrador Uno", "admin"),
    ("tutor_user1", "tutor1@example.com", "hash_tutor1", "Tutor Uno", "tutor"),
    ("tutor_user2", "tutor2@example.com", "hash_tutor2", "Tutor Dos", "tutor"),
    ("alumno_user1", "alumno1@example.com", "hash_alumno1", "Alumno Uno", "alumno"),
    ("alumno_user2", "alumno2@example.com", "hash_alumno2", "Alumno Dos", "alumno"),
    ("alumno_user3", "alumno3@example.com", "hash_alumno3", "Alumno Tres", "alumno"),
]

fake_courses = [
    ("Curso de Python", "Aprende Python desde cero", 50.0, 30),
    ("Curso de Flask", "Desarrollo web con Flask", 75.0, 45),
    ("Curso de SQL", "Manejo de bases de datos MySQL", 100.0, 60),
    ("Curso de Firebase", "Introducción a Firebase", 80.0, 40),
]

fake_materials = [
    ("guia-python.pdf", "pdf"),
    ("video-intro.mp4", "video"),
    ("imagen-ejemplo.png", "image"),
    ("apuntes.txt", "texto")
]

# ==========================
# Insertar en MySQL
# ==========================
try:
    with mysql_conn.cursor() as cursor:
        # Insertar usuarios
        for u in fake_users:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE email=email
            """, u)
        mysql_conn.commit()

        # Obtener IDs para relaciones
        cursor.execute("SELECT id, role FROM users")
        users_db = cursor.fetchall()
        tutor_ids = [u["id"] for u in users_db if u["role"] == "tutor"]
        admin_ids = [u["id"] for u in users_db if u["role"] == "admin"]
        alumno_ids = [u["id"] for u in users_db if u["role"] == "alumno"]

        # Insertar cursos
        for c in fake_courses:
            tutor_id = random.choice(tutor_ids)
            admin_id = random.choice(admin_ids)
            cursor.execute("""
                INSERT INTO courses (title, description, price, duration, tutor_id, admin_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'publicado')
            """, (c[0], c[1], c[2], c[3], tutor_id, admin_id))
        mysql_conn.commit()

        # Obtener IDs de cursos
        cursor.execute("SELECT id FROM courses")
        courses_db = cursor.fetchall()
        course_ids = [c["id"] for c in courses_db]

        # Insertar materiales
        for cid in course_ids:
            for m in fake_materials:
                cursor.execute("""
                    INSERT INTO materials (course_id, file_name, file_path, file_type)
                    VALUES (%s, %s, %s, %s)
                """, (cid, m[0], f"/path/{m[0]}", m[1]))
        mysql_conn.commit()

        # Relación alumno-curso
        for alumno in alumno_ids:
            for cid in random.sample(course_ids, min(2, len(course_ids))):
                cursor.execute("""
                    INSERT INTO student_courses (student_id, course_id, payment_status)
                    VALUES (%s, %s, 'pendiente')
                """, (alumno, cid))
        mysql_conn.commit()

        # Insertar pagos
        for alumno in alumno_ids:
            cid = random.choice(course_ids)
            cursor.execute("""
                INSERT INTO payments (student_id, course_id, amount, payment_method, receipt_url)
                VALUES (%s, %s, %s, %s, %s)
            """, (alumno, cid, random.randint(20,100), random.choice(["tarjeta","paypal"]), "http://recibo.ejemplo"))
        mysql_conn.commit()

        print("✅ Datos ficticios insertados en MySQL correctamente.")

except Exception as e:
    print("❌ Error MySQL:", e)
finally:
    mysql_conn.close()

# ==========================
# Insertar en Firebase
# ==========================
try:
    # Usa el método expuesto en firebase_init
    db = get_firebase_db()
    ref_users = db.reference("users")
    ref_courses = db.reference("courses")

    # Insertar usuarios ficticios (4 primeros)
    for u in fake_users[:4]:
        uid = u[0]
        ref_users.child(uid).set({
            "username": u[0],
            "email": u[1],
            "password_hash": u[2],
            "full_name": u[3],
            "role": u[4]
        })

    # Insertar cursos ficticios (3 primeros)
    for i, c in enumerate(fake_courses[:3]):
        ref_courses.child(f"curso_{i+1}").set({
            "title": c[0],
            "description": c[1],
            "price": c[2],
            "duration": c[3],
            "tutor_id": "tutor_user1"
        })

    print("✅ Datos ficticios insertados en Firebase correctamente.")

except Exception as e:
    print("❌ Error Firebase:", e)
