CREATE TABLE DIM_Indicator (
    Indicator_Key INT IDENTITY(1,1) PRIMARY KEY, -- Surrogate Key
    Indicator_Code NVARCHAR(50) NOT NULL UNIQUE, -- Business Key
    Indicator_Name NVARCHAR(50)
);
