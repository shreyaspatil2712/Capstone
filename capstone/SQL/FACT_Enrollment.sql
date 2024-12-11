CREATE TABLE FACT_Enrollment (
    Fact_Key INT IDENTITY(1,1) PRIMARY KEY, -- Surrogate Key
    Country_Key INT NOT NULL, -- Foreign Key
    Indicator_Key INT NOT NULL, -- Foreign Key
    Time_Key INT NOT NULL, -- Foreign Key
    Indicator_Value FLOAT,

    -- Define foreign key relationships
    FOREIGN KEY (Country_Key) REFERENCES DIM_Country(Country_Key),
    FOREIGN KEY (Indicator_Key) REFERENCES DIM_Indicator(Indicator_Key),
    FOREIGN KEY (Time_Key) REFERENCES DIM_Time(Time_Key)
);
