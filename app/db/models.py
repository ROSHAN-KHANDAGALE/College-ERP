import enum
import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


"""
User Roles - Defines the different roles in the system and their permissions.

- Admin: Full access to all features.
- Principal: Can manage teachers, students, and view reports.
- HOD: Can manage courses and subjects within their department.
- Teacher: Can manage their subjects, take attendance, and enter results.
- Student: Can view their profile, attendance, and results.
- Parent: Can view their children's profiles, attendance, and results.

Note: Each user can have only one profile based on their role (One-to-One relationship).
"""
class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    PRINCIPAL = "PRINCIPAL"
    HOD = "HOD"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    PARENT = "PARENT"


"""
User - Central authentication model. Each user has a role that determines their permissions and profile type.

- Admin: Full access to all features.
- Principal: Can manage teachers, students, and view reports.
- HOD: Can manage courses and subjects within their department.
- Teacher: Can manage their subjects, take attendance, and enter results.
- Student: Can view their profile, attendance, and results.
- Parent: Can view their children's profiles, attendance, and results.

Note: Each user can have only one profile based on their role (One-to-One relationship).
"""
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)

    # Account flags
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # One-to-One profile relationships
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_profile = relationship("TeacherProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    parent_profile = relationship("ParentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


"""
Profiles - Each user can have one profile based on their role.

- StudentProfile: Contains student-specific information like roll number, department, etc.
- TeacherProfile: Contains teacher-specific information like designation, department, etc.
- ParentProfile: Contains parent-specific information and links to their children (students).
"""
class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    admission_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="student_profile")
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    results = relationship("Result", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")

    def __repr__(self):
        return f"<StudentProfile(id={self.id}, roll_number={self.roll_number})>"


class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    designation = Column(String, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    user = relationship("User", back_populates="teacher_profile")
    department = relationship("Department", back_populates="teachers")
    subjects = relationship("Subject", back_populates="teacher")

    def __repr__(self):
        return f"<TeacherProfile(id={self.id}, designation={self.designation})>"


class ParentProfile(Base):
    __tablename__ = "parent_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="parent_profile")
    students = relationship("StudentParent", back_populates="parent")

    def __repr__(self):
        return f"<ParentProfile(id={self.id})>"


"""
Departments - A department can have multiple students, teachers, and courses.
"""
class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    students = relationship("StudentProfile", back_populates="department")
    teachers = relationship("TeacherProfile", back_populates="department")
    courses = relationship("Course", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name})>"


"""
Courses & Subjects - A department can have multiple courses, and each course can have multiple subjects.
"""
class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    department = relationship("Department", back_populates="courses")
    subjects = relationship("Subject", back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name})>"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teacher_profiles.id"), nullable=True)

    course = relationship("Course", back_populates="subjects")
    teacher = relationship("TeacherProfile", back_populates="subjects")
    enrollments = relationship("Enrollment", back_populates="subject")
    attendance_records = relationship("Attendance", back_populates="subject")
    exams = relationship("Exam", back_populates="subject")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name})>"


"""
Enrollment - Many-to-Many relationship between students and subjects. A student can enroll in multiple subjects, and a subject can have multiple students.

Note: This is a join table that links StudentProfile and Subject.
"""
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)

    student = relationship("StudentProfile", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")


"""
Attendance - Records the attendance of students for each subject on a specific date.
"""
class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LEAVE = "LEAVE"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)

    student = relationship("StudentProfile", back_populates="attendance_records")
    subject = relationship("Subject", back_populates="attendance_records")


"""
Exam & Result - Records the exams conducted for each subject and the results of students in those exams.
"""
class Exam(Base):
    __tablename__ = "exams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)
    exam_type = Column(String, nullable=False)  # e.g., Midterm, Final
    date = Column(Date, nullable=False)

    subject = relationship("Subject", back_populates="exams")
    results = relationship("Result", back_populates="exam")


class Result(Base):
    __tablename__ = "results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id"), nullable=False)
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id"), nullable=False)
    marks = Column(Float, nullable=False)

    student = relationship("StudentProfile", back_populates="results")
    exam = relationship("Exam", back_populates="results")


"""
StudentParent - Many-to-Many relationship between students and parents. A student can have multiple parents, and a parent can have multiple students.

Note: This is a join table that links StudentProfile and ParentProfile.
"""
class StudentParent(Base):
    __tablename__ = "student_parents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("parent_profiles.id"), nullable=False)

    student = relationship("StudentProfile")
    parent = relationship("ParentProfile", back_populates="students")
