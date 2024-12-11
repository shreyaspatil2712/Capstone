CREATE TABLE DIM_Time (
    Time_Key INT IDENTITY(1,1) PRIMARY KEY, -- Surrogate Key
    Year INT NOT NULL UNIQUE -- Business Key
);