-- ==========================================
-- MISSIONS APP
-- Database schema v0.0.1
-- ==========================================

PRAGMA foreign_keys = ON;


-- =========================
-- FAMÍLIES
-- =========================

CREATE TABLE families (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    active INTEGER DEFAULT 1
);


-- =========================
-- USUARIS
-- =========================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    family_id INTEGER NOT NULL,

    name TEXT NOT NULL,

    role TEXT NOT NULL CHECK(role IN ('admin','child')),

    avatar TEXT,

    favorite_color TEXT,

    theme TEXT DEFAULT 'default',

    points INTEGER DEFAULT 0,

    level INTEGER DEFAULT 1,

    birthdate DATE,

    active INTEGER DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (family_id) REFERENCES families(id)
);


-- =========================
-- CATEGORIES
-- =========================

CREATE TABLE categories (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    icon TEXT,

    color TEXT,

    sort_order INTEGER DEFAULT 0,

    active INTEGER DEFAULT 1

);


-- =========================
-- TIPUS DE MISSIÓ
-- =========================

CREATE TABLE mission_types (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    description TEXT

);


-- =========================
-- MISSIONS
-- =========================

CREATE TABLE missions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    family_id INTEGER NOT NULL,

    category_id INTEGER NOT NULL,

    title TEXT NOT NULL,

    description TEXT,

    icon TEXT,

    mission_type_id INTEGER,

    difficulty INTEGER DEFAULT 1,

    estimated_minutes INTEGER,

    points INTEGER DEFAULT 10,

    xp INTEGER DEFAULT 0,

    requires_validation INTEGER DEFAULT 0,

    repeat_type TEXT DEFAULT 'none',

    active INTEGER DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (family_id) REFERENCES families(id),

    FOREIGN KEY (category_id) REFERENCES categories(id),

    FOREIGN KEY (mission_type_id) REFERENCES mission_types(id)

);


-- =========================
-- ASSIGNACIÓ DE MISSIONS
-- =========================

CREATE TABLE mission_assignments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    mission_id INTEGER NOT NULL,

    user_id INTEGER NOT NULL,

    assignment_type TEXT DEFAULT 'owner',
    
    assigned_date DATE,

    due_date DATE,

    status TEXT DEFAULT 'pending',

    completed_at DATETIME,

    completed_by INTEGER,

    comment TEXT,
    
    FOREIGN KEY (mission_id) REFERENCES missions(id),

    FOREIGN KEY (user_id) REFERENCES users(id),

    FOREIGN KEY (completed_by) REFERENCES users(id)

);


-- =========================
-- VALIDACIONS PARES
-- =========================

CREATE TABLE validations (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    assignment_id INTEGER NOT NULL,

    validated_by INTEGER NOT NULL,

    approved INTEGER DEFAULT 0,

    comment TEXT,

    validated_at DATETIME DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (assignment_id) REFERENCES mission_assignments(id),

    FOREIGN KEY (validated_by) REFERENCES users(id)

);


-- =========================
-- HISTORIAL DE PUNTS
-- =========================

CREATE TABLE points_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    mission_id INTEGER,

    points INTEGER NOT NULL,

    reason TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (user_id) REFERENCES users(id),

    FOREIGN KEY (mission_id) REFERENCES missions(id)

);


-- =========================
-- RECOMPENSES
-- =========================

CREATE TABLE rewards (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    family_id INTEGER NOT NULL,

    name TEXT NOT NULL,

    description TEXT,

    points_required INTEGER NOT NULL,

    active INTEGER DEFAULT 1,


    FOREIGN KEY (family_id) REFERENCES families(id)

);


-- =========================
-- RECOMPENSES UTILITZADES
-- =========================

CREATE TABLE reward_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reward_id INTEGER NOT NULL,

    user_id INTEGER NOT NULL,

    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    approved INTEGER DEFAULT 0,

    delivered INTEGER DEFAULT 0,


    FOREIGN KEY (reward_id) REFERENCES rewards(id),

    FOREIGN KEY (user_id) REFERENCES users(id)

);


-- =========================
-- ACTIVITATS EXTRAESCOLARS
-- =========================

CREATE TABLE activities (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    family_id INTEGER NOT NULL,

    name TEXT NOT NULL,

    icon TEXT,

    weekday TEXT,

    time TEXT,

    location TEXT,


    FOREIGN KEY (family_id) REFERENCES families(id)

);


-- =========================
-- USUARIS ACTIVITATS
-- =========================

CREATE TABLE activity_users (

    activity_id INTEGER NOT NULL,

    user_id INTEGER NOT NULL,


    PRIMARY KEY(activity_id,user_id),


    FOREIGN KEY(activity_id) REFERENCES activities(id),

    FOREIGN KEY(user_id) REFERENCES users(id)

);


-- =========================
-- PLANTILLES DE CAMPS EXTRA
-- (deures, piscina...)
-- =========================

CREATE TABLE mission_fields (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    mission_id INTEGER NOT NULL,

    field_name TEXT NOT NULL,

    field_type TEXT NOT NULL,


    FOREIGN KEY(mission_id) REFERENCES missions(id)

);