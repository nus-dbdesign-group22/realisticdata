CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100),
  graduation_year INTEGER
);

CREATE TABLE courses (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100),
  instructor_id INTEGER,
  department_id INTEGER,
  description TEXT,
  credits INTEGER,
  FOREIGN KEY (instructor_id) REFERENCES instructors(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE instructors (
  id INTEGER PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100),
  hire_date DATE,
  department_id INTEGER,
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE departments (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE enrollments (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  course_id INTEGER,
  semester VARCHAR(50),
  year INTEGER,
  grade VARCHAR(2),
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE prerequisites (
  id INTEGER PRIMARY KEY,
  course_id INTEGER,
  prerequisite_course_id INTEGER,
  FOREIGN KEY (course_id) REFERENCES courses(id),
  FOREIGN KEY (prerequisite_course_id) REFERENCES courses(id)
);