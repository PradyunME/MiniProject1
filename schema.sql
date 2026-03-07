-- CMPUT291 - Winter 2026
-- Mini Project I - Database Schema (DDL)

-- Drop tables if they exist
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS certificates;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS completion;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS modules;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE users (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('Student', 'Instructor', 'Admin')),
    pwd TEXT NOT NULL
);


-- ============================================================================
-- COURSES TABLE
-- ============================================================================
CREATE TABLE courses (
    cid INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    price REAL NOT NULL CHECK(price >= 0),
    pass_grade REAL NOT NULL CHECK(pass_grade >= 0 AND pass_grade <= 100),
    max_students INTEGER NOT NULL CHECK(max_students > 0)
);

-- ============================================================================
-- ENROLLMENTS TABLE
-- ============================================================================
-- A student can have multiple enrollments in the same course over time
-- Active enrollment: current timestamp is between start_ts and end_ts AND role = 'Student'
-- PRIMARY KEY: (cid, uid, start_ts) allows multiple enrollments but ensures uniqueness per enrollment
CREATE TABLE enrollments (
    cid INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    start_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_ts TIMESTAMP NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Student', 'Instructor')),
    PRIMARY KEY (cid, uid, start_ts),
    FOREIGN KEY (cid) REFERENCES courses(cid) ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);

-- ============================================================================
-- MODULES TABLE
-- ============================================================================
CREATE TABLE modules (
    cid INTEGER NOT NULL,
    mid INTEGER NOT NULL,
    name TEXT NOT NULL,
    summary TEXT,
    weight REAL NOT NULL CHECK(weight >= 0),
    PRIMARY KEY (cid, mid),
    FOREIGN KEY (cid) REFERENCES courses(cid) ON DELETE CASCADE
);


-- ============================================================================
-- LESSONS TABLE
-- ============================================================================
CREATE TABLE lessons (
    cid INTEGER NOT NULL,
    mid INTEGER NOT NULL,
    lid INTEGER NOT NULL,
    title TEXT NOT NULL,
    duration INTEGER NOT NULL CHECK(duration >= 0),
    content TEXT,
    PRIMARY KEY (cid, mid, lid),
    FOREIGN KEY (cid, mid) REFERENCES modules(cid, mid) ON DELETE CASCADE
);

-- ============================================================================
-- COMPLETION TABLE
-- ============================================================================
-- A student can complete the same lesson multiple times across different enrollments
-- PRIMARY KEY: (uid, cid, mid, lid, ts) allows tracking completion per enrollment period
CREATE TABLE completion (
    uid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    mid INTEGER NOT NULL,
    lid INTEGER NOT NULL,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (uid, cid, mid, lid, ts),
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (cid, mid, lid) REFERENCES lessons(cid, mid, lid) ON DELETE CASCADE
);


-- ============================================================================
-- GRADES TABLE
-- ============================================================================
-- A student can receive multiple grades for the same module across different enrollments
-- PRIMARY KEY: (uid, cid, mid, received_ts) allows multiple grades per module over time
CREATE TABLE grades (
    uid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    mid INTEGER NOT NULL,
    received_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
    PRIMARY KEY (uid, cid, mid, received_ts),
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (cid, mid) REFERENCES modules(cid, mid) ON DELETE CASCADE
);

-- ============================================================================
-- CERTIFICATES TABLE
-- ============================================================================
-- A student can earn multiple certificates for the same course across different enrollments
-- PRIMARY KEY: (cid, uid, received_ts) allows multiple certificates over time
CREATE TABLE certificates (
    cid INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    received_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    final_grade REAL NOT NULL CHECK(final_grade >= 0 AND final_grade <= 100),
    PRIMARY KEY (cid, uid, received_ts),
    FOREIGN KEY (cid) REFERENCES courses(cid) ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);

-- ============================================================================
-- PAYMENTS TABLE
-- ============================================================================
-- A student can make multiple payments for the same course (multiple enrollments)
-- PRIMARY KEY: (uid, cid, ts) ensures unique payment records
CREATE TABLE payments (
    uid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    credit_card_no TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    PRIMARY KEY (uid, cid, ts),
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES courses(cid) ON DELETE CASCADE
);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
