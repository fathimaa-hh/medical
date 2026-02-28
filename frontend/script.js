let currentPatientID=null;

function showSection(id){ document.querySelectorAll('.section').forEach(sec=>sec.classList.add('hidden')); document.getElementById(id).classList.remove('hidden'); }

function nextStep(){ 
    const name=document.getElementById("name").value.trim();
    const age=document.getElementById("age").value;
    const blood=document.getElementById("blood").value.trim();
    const phone=document.getElementById("phone").value.trim();
    if(!name||!age||!blood||!phone){ alert("Fill all details"); return;}
    document.getElementById("step1").classList.add("hidden");
    document.getElementById("step2").classList.remove("hidden");
}
async function registerPatient() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const blood_group = document.getElementById("blood").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const allergies = document.getElementById("allergy").value.trim();
    const chronic_diseases = document.getElementById("disease").value.trim();
    const emergency_contact = document.getElementById("contact").value.trim();
    const password = "demo123"; // for demo purposes

    if (!name || !age || !blood_group || !phone) {
        alert("Please fill all fields");
        return;
    }

    const patientData = {
        name,
        age: Number(age),
        blood_group,
        allergies,
        chronic_diseases,
        medications: "None",
        emergency_contact,
        password
    };

    try {
        const res = await fetch("http://127.0.0.1:8001/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(patientData)
        });

        const data = await res.json();

        if (res.ok) {
            alert("Registered! ID: " + data.patient_id);

            // Correct QR image path using static route
            const qrUrl = `http://127.0.0.1:8001${data.qr_image_path.replace(/\\/g, "/")}`;

            // Display QR image
            document.getElementById("qrOutput").innerHTML = `<img src="${qrUrl}" width="150"/>`;

            // Hide step 2 and optionally show a success message
            document.getElementById("step2").classList.add("hidden");
        } else {
            alert(data.detail || "Registration failed");
        }
    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}

async function loginPatient(){
    const patientID=document.getElementById("loginID").value.trim();
    if(!patientID){alert("Enter ID"); return;}
    try{ const res=await fetch(`http://127.0.0.1:8001/profile/${patientID}`); const data=await res.json(); if(res.ok){ currentPatientID=patientID; showDashboard(data); } else{alert(data.detail||"Not found");} }
    catch(err){ console.error(err); alert("Server error");}
}

function showDashboard(patient){
    document.getElementById("patientInfo").innerHTML=`<p>Name:${patient.name}</p><p>Age:${patient.age}</p><p>Blood:${patient.blood_group}</p>`;
    showSection("dashboard");
}

function logout(){ currentPatientID=null; showSection("home"); }

function simulateFingerprint(){ const id=prompt("Enter Patient ID for demo"); if(id) fetch(`http://127.0.0.1:8001/emergency_data/${id}`).then(r=>r.json()).then(data=>showEmergencyData(data)).catch(e=>alert("Server error")) }

function startQRScanner(){
    const scanner=new Html5Qrcode("reader");
    scanner.start({facingMode:"environment"},{fps:10,qrbox:250},decodedText=>{scanner.stop(); const patientID=atob(decodedText); fetch(`http://127.0.0.1:8001/emergency_data/${patientID}`).then(r=>r.json()).then(d=>showEmergencyData(d)).catch(e=>alert("Invalid QR"));});
}
function registerDoctor(){
    const doctorName=document.getElementById("doctorName").value.trim();
    const hospital=document.getElementById("hospitalName").value.trim();
    const doctorID=document.getElementById("doctorID").value.trim();

    if(!doctorName||!hospital||!doctorID){alert("Fill all fields"); return;}

    if(localStorage.getItem("doctor_"+doctorID)){alert("Doctor ID exists"); return;}

    const username=doctorName.replace(/\s+/g,"").toLowerCase();
    const password="demo123"; // for demo, you can later change

    const doctorData={doctorName,hospital,doctorID,username,password};

    localStorage.setItem("doctor_"+doctorID,JSON.stringify(doctorData));

    document.getElementById("doctorRegisterMsg").innerHTML=`<p>✅ Doctor Registered! Username: ${username}, Password: ${password}</p>`;
}
async function loginDoctor(){
    const username=document.getElementById("hospitalUser").value.trim();
    const password=document.getElementById("hospitalPass").value.trim();

    let found=false;
    for(let key in localStorage){
        if(key.startsWith("doctor_")){
            const doctor=JSON.parse(localStorage.getItem(key));
            if(doctor.username===username && doctor.password===password){
                localStorage.setItem("loggedDoctor",JSON.stringify(doctor));
                localStorage.setItem("loggedInRole","hospital");
                found=true;
                showSection("hospital");
                break;
            }
        }
    }
    if(!found) alert("Invalid username/password");
}

function showEmergencyData(patient){ document.getElementById("emergencyData").innerHTML=`<h2>🚨 Emergency</h2><p>Name:${patient.name}</p><p>Age:${patient.age}</p><p>Blood:${patient.blood_group}</p><p>Allergies:${patient.allergies}</p><p>Chronic:${patient.chronic_diseases}</p>`; }

// Doctor login and dashboard functions remain the same as in your final JS