# DDL und prompts für die Neuseeland Datenquelle

ddl = 'CREATE TABLE [dbo].[new_zealand_birthplace_2018_census](\
	[Code] [int] NOT NULL,\
	[Birthplace] [nvarchar](150) NULL,\
	[Census_night_population_count] [int] NULL,\
	[Census_usually_resident_population_count] [int] NULL,\
PRIMARY KEY CLUSTERED \
(\
	[Code] ASC\
 )\
);'

prompts = [
     'How many of the usual residents of new zealand were born in Germany?'
    ,'In how many different regions where the usual residents of new zealand born?'
    ,'How many percent of the usual residents of new zealand where born in new zealand?'
    ,'In which region outside of new zealand where most usual residents of new zealand born?'
    ,'Which birthplace region has the highest absolute discrepancy between its amount of usual residents and the census night population?'
]