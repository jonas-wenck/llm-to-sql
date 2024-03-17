# DDL und prompts für die Neuseeland Datenquelle

ddl = """
CREATE TABLE [dbo].[new_zealand_birthplace_2018_census](
	[Code] [int] NOT NULL,
	[Birthplace] [nvarchar](150) NULL,
	[Census_night_population_count] [int] NULL,
	[Census_usually_resident_population_count] [int] NULL,
PRIMARY KEY CLUSTERED ([Code] ASC)
);
"""

prompts = [
     'How many of the usual residents of New Zealand were born in Germany?'
    ,'In how many different regions where the usual residents of New Zealand born?'
    ,'How many percent of the usual residents of new zealand where born in New Zealand?'
    ,'In which region outside of new zealand where most usual residents of New Zealand born?'
    ,'Which birthplace region has the highest absolute discrepancy between its amount of usual residents and the census night population?'
]

additional_context = """
Use T-SQL syntax.
There is only a single table 'new_zealand_birthplace_2018_census'.
The column 'Code' contains the numerical identifier of that birth place and has no inherent meaning.
The column 'Birthplace' contains the name of the birth place. This can be a country like 'New Zealand'.
The column 'Census_night_population_count' contains the amount of people of a certain birth place that were present on census night. These are not the permanent or usual residents.
The column 'Census_usually_resident_population_count' contains the amount of people of a certain birth place who live permanently in new zealand.
When querying on the columns 'Census_night_population_count' or 'Census_usually_resident_population_count', use 'SUM' instead of 'COUNT'.
"""