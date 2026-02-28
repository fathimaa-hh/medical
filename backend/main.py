from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models, schema as schemas, auth
import shutil, os

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.staticfiles import StaticFiles

# Serve the uploads folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Patient Registration
# -------------------------
@app.post("/register")
def register_patient(patient: schemas.PatientRegister, db: Session = Depends(get_db)):
    # Check duplicate
    existing_user = db.query(models.User).filter(models.User.name == patient.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    fingerprint_id = auth.generate_fingerprint_id()
    qr_id = auth.generate_qr_id()
    hashed_password = auth.hash_password(patient.password)

    new_user = models.User(
        name=patient.name,
        age=patient.age,
        blood_group=patient.blood_group,
        allergies=patient.allergies,
        chronic_diseases=patient.chronic_diseases,
        medications=patient.medications,
        emergency_contact=patient.emergency_contact,
        fingerprint_id=fingerprint_id,
        qr_code_id=qr_id,
        password=hashed_password,
        role="patient"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate QR
    import qrcode
    os.makedirs("uploads", exist_ok=True)
    qr_path = f"uploads/{qr_id}.png"
    qrcode.make(qr_id).save(qr_path)

    return {
    "message": "Patient registered",
    "patient_id": new_user.id,
    "fingerprint_id": fingerprint_id,
    "qr_code_id": qr_id,
    "qr_image_path": f"/uploads/{qr_id}.png"  # <-- change here
    }

# -------------------------
# Get Patient Profile + Reports
# -------------------------
@app.get("/profile/{patient_id}")
def get_profile(patient_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == patient_id).first()
    if not user:
        raise HTTPException(404, "Patient not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "blood_group": user.blood_group,
        "allergies": user.allergies,
        "chronic_diseases": user.chronic_diseases,
        "medications": user.medications,
        "emergency_contact": user.emergency_contact,
        "reports": [
            {
                "diagnosis": r.diagnosis,
                "prescription": r.prescription,
                "report_file": r.report_file,
                "date": r.date.isoformat()
            } for r in user.reports
        ]
    }

# -------------------------
# Hospital Login
# -------------------------
@app.post("/hospital_login")
def hospital_login(credentials: dict, db: Session = Depends(get_db)):
    username = credentials.get("username")
    password = credentials.get("password")
    doctor = db.query(models.Doctor).filter(models.Doctor.username==username).first()
    if not doctor or doctor.password != password:
        raise HTTPException(401, "Invalid credentials")
    return {"doctorName": doctor.name, "hospital": doctor.hospital.name}

# -------------------------
# Add Report
# -------------------------
@app.post("/add_report")
def add_report(patient_id: int = None,
               hospital_name: str = None,
               doctor_name: str = None,
               diagnosis: str = None,
               prescription: str = None,
               file: UploadFile = File(None),
               db: Session = Depends(get_db)):

    patient = db.query(models.User).filter(models.User.id==patient_id).first()
    if not patient:
        raise HTTPException(404, "Patient not found")

    report_file_path = None
    if file:
        os.makedirs("uploads", exist_ok=True)
        report_file_path = f"uploads/{file.filename}"
        with open(report_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    report = models.Report(
        patient_id=patient.id,
        hospital_name=hospital_name,
        doctor_name=doctor_name,
        diagnosis=diagnosis,
        prescription=prescription,
        report_file=report_file_path
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"message": "Report added"}

# -------------------------
# Emergency Data
# -------------------------
@app.get("/emergency_data/{patient_id}")
def emergency_data(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.User).filter(models.User.id==patient_id).first()
    if not patient:
        raise HTTPException(404, "Patient not found")
    return {
        "name": patient.name,
        "age": patient.age,
        "blood_group": patient.blood_group,
        "allergies": patient.allergies,
        "chronic_diseases": patient.chronic_diseases
    }