-- Active: 1670088204836@@127.0.0.1@3307@hospitalmanagement
CREATE DATABASE HospitalManagement;
USE HospitalManagement;

CREATE TABLE PATIENT (
PatientSSN DECIMAL(50),
PatientFirstName VARCHAR(50) NOT NULL,
PatientLastName VARCHAR(50) NOT NULL,
PatientAge DECIMAL(3,0),
PatientAddress VARCHAR(100),
PatientGender VARCHAR(8),
PatientPass VARCHAR(50) NOT NULL,
PatientPhoneNumber DECIMAL(8,0) NOT NULL,
PatientFamilyNumber DECIMAL(8,0),
Symptoms VARCHAR(100),
PatientEnteringDateRoom DATE,
PatientLeavingDateRoom DATE,
RegistrationDate DATE,
ReceptionistSSN DECIMAL(50),
RoomNb DECIMAL(4,0),
PRIMARY KEY(PatientSSN)
);

CREATE TABLE RECEPTIONIST (
ReceptionistSSN DECIMAL(50),
ReceptionistFirstName VARCHAR(50) NOT NULL,
ReceptionistLastName VARCHAR(50) NOT NULL,
ReceptionistPass VARCHAR(50) NOT NULL,
ReceptionistAddress VARCHAR(100),
ReceptionistGender VARCHAR(8),
ReceptionistPhoneNumber DECIMAL(8,0),
PRIMARY KEY(ReceptionistSSN)
);

CREATE TABLE DOCTOR (
DoctorSSN DECIMAL(5,0),
DoctorFirstName VARCHAR(50) NOT NULL,
DoctorLastName VARCHAR(50) NOT NULL,
DoctorAge DECIMAL(3,0),
DoctorSpecialization VARCHAR(50) NOT NULL,
DoctorPass VARCHAR(50) NOT NULL,
DoctorAddress VARCHAR(100),
DoctorGender VARCHAR(8),
DoctorPhoneNumber DECIMAL(8,0),
PRIMARY KEY(DoctorSSN)
);

CREATE TABLE NURSE (
NurseSSN DECIMAL(5,0),
NurseFirstName VARCHAR(50) NOT NULL,
NurseLastName VARCHAR(50) NOT NULL,
NurseAge DECIMAL(3,0),
NursePass VARCHAR(50) NOT NULL,
NurseAddress VARCHAR(100),
NurseGender VARCHAR(8),
NursePhoneNumber DECIMAL(8,0),
PRIMARY KEY(NurseSSN)
);

CREATE TABLE MEDICINE (
MedicineName VARCHAR(50),
MedicineType VARCHAR(50) NOT NULL,
CompanyName VARCHAR(100),
ExpiryDate DATE,
MedicinePrice DECIMAL(8,0),
DoctorSSN DECIMAL(5,0),
PRIMARY KEY(MedicineName),
Foreign Key (DoctorSSN) REFERENCES DOCTOR(DoctorSSN)
);

CREATE TABLE BILL (
BillNb DECIMAL(10,0),
BillAmount DECIMAL(9,0) NOT NULL,
BillDetails VARCHAR(1000) NOT NULL,
Currency VARCHAR(50),
BillStatus VARCHAR(50),
PRIMARY KEY(BillNb)
);

CREATE TABLE MEDICALRECORD (
MedicalRecordID DECIMAL(5,0),
Diseases VARCHAR(100),
PreviousSurgeries VARCHAR(100),
Allergies VARCHAR(100) NOT NULL,
BloodType VARCHAR(3) NOT NULL,
VaccinationHistory VARCHAR(100),
recordTDate Date,
PatientSSN DECIMAL(50),
PRIMARY KEY(MedicalRecordID),
Foreign Key (PatientSSN) REFERENCES PATIENT(PatientSSN)
);

CREATE TABLE HFLOOR (
FloorNb DECIMAL(2,0),
NumberofRooms DECIMAL(3,0),
PRIMARY KEY(FloorNb)
);

CREATE TABLE ROOM (
RoomNb DECIMAL(4,0),
Availibility VARCHAR(10) Not Null,
RoomClass VARCHAR(10),
NumberofBeds DECIMAL(2,0),
FloorNb DECIMAL(2,0),
PRIMARY KEY(RoomNb),
Foreign Key (FloorNb) REFERENCES HFLOOR(FloorNb)
);

CREATE TABLE APPOINTMENT (
AppointmentNb DECIMAL(4,0),
AppointmentDate DATE,
AppointmentTime TIME,
AppointmentStatus VARCHAR(100),
PatientSSN DECIMAL(50),
DoctorSSN DECIMAL(5,0),
PRIMARY KEY (AppointmentNb, PatientSSN, DoctorSSN),
FOREIGN KEY (PatientSSN) REFERENCES PATIENT(PatientSSN),
FOREIGN KEY (DoctorSSN) REFERENCES DOCTOR(DoctorSSN)
);

CREATE TABLE TAKES (
MedicineDuration DATE,
PatientSSN DECIMAL(50),
MedicineName VARCHAR(50),
PRIMARY KEY (MedicineDuration, PatientSSN, MedicineName),
FOREIGN KEY (PatientSSN) REFERENCES PATIENT(PatientSSN),
FOREIGN KEY (MedicineName) REFERENCES MEDICINE(MedicineName)
);

CREATE TABLE PAYMENT (
PaymentYEAR DATE,
PatientSSN DECIMAL(50),
MedicineName VARCHAR(50),
BillNb DECIMAL(10,0),
PRIMARY KEY (PaymentYEAR, BillNb, PatientSSN, MedicineName),
FOREIGN KEY (PatientSSN) REFERENCES PATIENT(PatientSSN),
FOREIGN KEY (BillNb) REFERENCES BILL(BillNb),
FOREIGN KEY (MedicineName) REFERENCES MEDICINE(MedicineName)
);

CREATE TABLE FCONTAINS (
WorkingDate DATE,
DoctorSSN DECIMAL(50),
NurseSSN DECIMAL(50),
FloorNb DECIMAL(2,0),
PRIMARY KEY (WorkingDate, DoctorSSN, NurseSSN, FLoorNb),
FOREIGN KEY (DoctorSSN) REFERENCES DOCTOR(DoctorSSN),
FOREIGN KEY (NurseSSN) REFERENCES NURSE(NurseSSN),
FOREIGN KEY (FloorNb) REFERENCES HFLOOR(FloorNb)
);

ALTER TABLE PATIENT
ADD Foreign Key (RoomNb) REFERENCES ROOM(RoomNb)

ALTER TABLE PATIENT
ADD Foreign Key (ReceptionistSSN) REFERENCES RECEPTIONIST(ReceptionistSSN);
