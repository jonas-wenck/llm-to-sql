# DDL und prompts für die Neuseeland Datenquelle

ddl = """
CREATE TABLE [dbo].[air_temperature](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Measured_Temperature] [float] NULL,
	[Relative_Humidity] [float] NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[cloudiness](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Type_of_Measurement] [varchar](50) NULL,
	[Degree_of_Cover] [int] NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[moisture](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Absolute_Humidity] [float] NULL,
	[Vapor_Pressure] [float] NULL,
	[Humid_Temperature] [float] NULL,
	[Pressure] [float] NULL,
	[Temperature_2m_High] [float] NULL,
	[Relative_Humidity] [float] NULL,
	[Dewpoint_Temperature] [float] NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[precipitation](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Height] [float] NULL,
	[Has_Precipitation] [int] NULL,
	[Type_of_Precipitation] [int] NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[pressure](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Pressure_at_Sea_Level] [float] NULL,
	[Pressure_at_Station_Height] [float] NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[station](
	[Stations_id] [int] NOT NULL,
	[Station_Height] [varchar](50) NULL,
	[Latitude] [varchar](50) NULL,
	[Longitude] [varchar](50) NULL,
	[Station_Name] [varchar](50) NULL,
	[Federal_State] [varchar](50) NULL,
PRIMARY KEY CLUSTERED ([Stations_id] ASC)
);

CREATE TABLE [dbo].[sun](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Minutes_of_Sunshine] [float] NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[visibility](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Type_of_Measurement] [varchar](50) NULL,
	[Visibility] [varchar](50) NULL,
	[Date_Time_Measured] [datetime] NULL
);

CREATE TABLE [dbo].[wind](
	[STATIONS_ID] [int] NOT NULL,
	[Quality_Level] [int] NULL,
	[Wind_Speed] [varchar](50) NULL,
	[Wind_Direction] [varchar](50) NULL,
	[Date_Time_Measured] [datetime] NULL
);
"""

prompts = [
     'What was the highest temperature ever recorded?'
    ,'What was the lowest temperature recorded in Mannheim in 2023?'
    ,'Which station had  the most precipitation, which had the least? Use the count of times with rain as amount.'
    ,'Which federal state had the most cloud cover, which had the least? Show a list of all states sorted decending.'
    ,'Is there a correlation between the amount of sunshine and air pressure?'
]

additional_context = """
Use T-SQL syntax.
There are multiple tables.
The column 'Station_Name' of the table 'station' is the name of the nearest city.
The column 'Federal_State' of the table 'station' is the federal state in which the station is located.
The column 'Has_Precipitation' of the table 'precipitation' is a boolean value. A value of 1 means 'true' and a value of 0 means 'false'. 
"""