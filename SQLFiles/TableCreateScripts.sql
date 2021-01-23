CREATE TABLE LifeList(
    BIRD_ID int IDENTITY(1,1) PRIMARY KEY,
    SPECIES varchar(50) NOT NULL,
    Category varchar(50) NULL,
    CategoryAlt varchar(50) NULL,
    First_Sight_City varchar(30) NULL,
    First_Sight_State varchar(3) NULL,
    First_Sight_Details varchar(50) NULL,
    First_Sight_Date date NULL
)

CREATE TABLE YearList2021 (
    BIRD_ID int NOT NULL,
    SPECIES varchar(50) NOT NULL,
    Category varchar(50) NULL,
    CategoryAlt varchar(50) NULL,
    First_Sight_City varchar(30) NULL,
    First_Sight_State varchar(3) NULL,
    First_Sight_Details varchar(50) NULL,
    First_Sight_Date date NULL,
    WasLifeBird BIT NOT NULL,
)

CREATE TABLE CaliList2021 (
    BIRD_ID int NOT NULL,
    SPECIES varchar(50) NOT NULL,
    Category varchar(50) NULL,
    CategoryAlt varchar(50) NULL,
    Sight_Details varchar(50) NULL,
    Sight_Date date NULL
)


select * from dbo.YearList2021
select * from dbo.LifeList
 

