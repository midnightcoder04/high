CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phoneno VARCHAR(15),
    profile_image BLOB
);

CREATE TABLE Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doc_name VARCHAR(100),
    profile_image VARCHAR(255),
    specialty VARCHAR(100),
    bio TEXT,
    ratings FLOAT,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    status ENUM('requested', 'accepted', 'rejected', 'concluded') NOT NULL,
    gmeet_link VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE
);

CREATE TABLE Chat (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    sender_id INT,
    receiver_id INT,
    message TEXT,
    file VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    rating FLOAT NOT NULL,
    review_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE
);


INSERT INTO Doctors (doc_name, profile_image, specialty, bio, ratings, password)
VALUES 
    ('Dr. Smith', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Pediatricians', 'Our pediatricians provide comprehensive care for infants, children, and adolescents.', 4.5, '123'),
    ('Dr. Johnson', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Pediatricians', 'Specializing in pediatric care with a focus on child development and well-being.', 4.2, '123'),
    ('Dr. Williams', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Neurologists', 'Expert care for disorders of the nervous system, including the brain and spinal cord.', 4.8, '123'),
    ('Dr. Brown', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Neurologists', 'Treating neurological conditions with personalized care and advanced techniques.', 4.4, '123'),
    ('Dr. Miller', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Cardiologists', 'Specialized care for heart-related conditions and diseases.', 4.7, '123'),
    ('Dr. Wilson', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Cardiologists', 'Expertise in cardiac health with a focus on prevention and treatment.', 4.3, '123'),
    ('Dr. Martinez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Endocrinologists', 'Management of hormonal imbalances and endocrine disorders.', 4.6, '123'),
    ('Dr. Garcia', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Endocrinologists', 'Specializing in comprehensive endocrine care for patients of all ages.', 4.1, '123'),
    ('Dr. Lopez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Psychiatrists', 'Expert mental health care for a variety of psychiatric conditions.', 4.9, '123'),
    ('Dr. Gonzalez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Psychiatrists', 'Treating psychiatric disorders with compassion and evidence-based therapies.', 4.2, '123'),
    ('Dr. Rodriguez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Dermatologists', 'Treatment for skin conditions and diseases.', 4.5, '123'),
    ('Dr. Perez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Dermatologists', 'Providing specialized dermatological care with the latest treatments.', 4.4, '123'),
    ('Dr. Sanchez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Oncologists', 'Comprehensive care for patients with cancer.', 4.8, '123'),
    ('Dr. Torres', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Oncologists', 'Treating cancer patients with personalized treatment plans and supportive care.', 4.3, '123'),
    ('Dr. Ramirez', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Gastroenterologists', 'Specialized care for digestive system disorders.', 4.7, '123'),
    ('Dr. Flores', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Gastroenterologists', 'Expertise in gastroenterology with a focus on patient wellness and digestive health.', 4.2, '123'),
    ('Dr. King', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Radiologists', 'Specializing in diagnostic imaging and interpretation.', 4.6, '123'),
    ('Dr. Turner', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3onmoYr9iN85uwpvgKtwpET99_l4Et92T2g&s', 'Radiologists', 'Providing accurate and timely radiology services for medical diagnosis.', 4.1, '123');

update doctors set profile_image = 'https://lifehacker.com/imagery/articles/01J18F8YP5JAGB28DQE70HGBJ5/hero-image.fill.size_1248x702.v1719348182.png' where doc_name = 'Dr. Gracia';    

