DROP DATABASE IF EXISTS EuroTour;

CREATE DATABASE EuroTour;

USE EuroTour;

CREATE TABLE RoadQuality (
    Country VARCHAR(255) NOT NULL,
    RoadYear YEAR,
    Score DECIMAL,
    PRIMARY KEY (Country, RoadYear)
);

CREATE TABLE TourismPrioritization (
    Country VARCHAR(255) NOT NULL,
    TourismYear YEAR,
    Score DECIMAL(4, 3),
    PRIMARY KEY (Country, TourismYear)
);

CREATE TABLE RoadDensity (
    Country VARCHAR(255) NOT NULL,
    DataYear YEAR,
    KmRoadPerKmSquared DECIMAL(6, 3),
    Score DECIMAL(4, 3),
    PRIMARY KEY (Country, DataYear)
);

CREATE TABLE AvgFuelPrice (
    Country VARCHAR(255) NOT NULL,
    FuelPriceYear YEAR,
    Score DECIMAL(4, 3),
    AvgPricePerLiter DECIMAL(4, 3),
    PRIMARY KEY (Country, FuelPriceYear)
);

CREATE TABLE RoadSpending (
    Country VARCHAR(255) NOT NULL,
    SpendingYear YEAR,
    RoadSpending DECIMAL(4, 3),
    GDP DECIMAL(4, 3),
    SpendingByGDPPercent DECIMAL(4, 3),
    PRIMARY KEY (Country, SpendingYear),
    CONSTRAINT fk_3 FOREIGN KEY (Country, SpendingYear) REFERENCES RoadQuality (Country, RoadYear)
);

CREATE TABLE PassengerCars (
    Country VARCHAR(255) NOT NULL,
    PCDataYear YEAR,
    MotorType VARCHAR(50),
    EngineSize VARCHAR(100),
    Numcars INT,
    PRIMARY KEY (Country, PCDataYear, MotorType, EngineSize),
    CONSTRAINT fk_2 FOREIGN KEY (Country, PCDataYear) REFERENCES RoadQuality (Country, RoadYear),
    CONSTRAINT fk_5 FOREIGN KEY (Country, PCDataYear) REFERENCES RoadDensity (Country, DataYear),
    CONSTRAINT fk_6 FOREIGN KEY (Country, PCDataYear) REFERENCES AvgFuelPrice (Country, FuelPriceYear)
);

CREATE TABLE Trips (
    Country VARCHAR(255) NOT NULL,
    TripYear YEAR,
    Purpose VARCHAR(255),
    Duration VARCHAR(255),
    NumTrips INTEGER,
    PRIMARY KEY (Country, TripYear, Purpose, Duration),
    CONSTRAINT fk_1 FOREIGN KEY (Country, TripYear) REFERENCES RoadQuality (Country, RoadYear),
    CONSTRAINT fk_4 FOREIGN KEY (Country, TripYear) REFERENCES TourismPrioritization (Country, TourismYear)
);


-- Researcher Stuff
CREATE TABLE Researcher (
    ResearcherID INT AUTO_INCREMENT PRIMARY KEY,
    ResearcherName VARCHAR(255),
    FieldOfStudy VARCHAR(255)
);

INSERT INTO Researcher (ResearcherName, FieldOfStudy)
Values ('Ellie Willems', 'Tourism Studies');

CREATE TABLE ResearchFindings (
    ResearchPostID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    PostDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Research TEXT,
    AuthorID INT,
    FOREIGN KEY (AuthorID) REFERENCES Researcher (ResearcherID)
);

CREATE TABLE Files (
    FileID INT AUTO_INCREMENT PRIMARY KEY,
    FileName VARCHAR(255) NOT NULL,  
    FileType VARCHAR(50),                       
    MimeType VARCHAR(100),                       
    FileSize INT,                               
    FileData LONGBLOB,                           
    UploadDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    ResearchPostID INT,                              
    FOREIGN KEY (ResearchPostID) REFERENCES ResearchFindings (ResearchPostID)
);
