from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    blood_group = Column(String)
    allergies = Column(String)
    chronic_diseases = Column(String)
    medications = Column(String)
    emergency_contact = Column(String)
    fingerprint_id = Column(String, unique=True)
    qr_code_id = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="patient")
    reports = relationship("Report", back_populates="patient")


class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    verified = Column(Boolean, default=True)
    doctors = relationship("Doctor", back_populates="hospital")


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship("Hospital", back_populates="doctors")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    hospital_name = Column(String)
    doctor_name = Column(String)
    diagnosis = Column(String)
    prescription = Column(String)
    report_file = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    patient = relationship("User", back_populates="reports")