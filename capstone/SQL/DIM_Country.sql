CREATE TABLE DIM_Country (
    Country_Key INT IDENTITY(1,1) PRIMARY KEY, -- Surrogate Key
    Country_Code VARCHAR(10) NOT NULL UNIQUE, -- Business Key
    Country_Name NVARCHAR(72),
    Region VARCHAR(255),
    IncomeGroup VARCHAR(255),
    SpecialNotes TEXT
);
