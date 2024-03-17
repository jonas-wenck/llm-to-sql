# DDL und prompts für die Neuseeland Datenquelle
ddl = """
CREATE TABLE [dbo].[covid](
	[date] [date] NULL,
	[state] [varchar](50) NULL,
	[fips] [int] NULL,
	[cases] [int] NULL,
	[deaths] [int] NULL,
	[id] [int] NOT NULL,
PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [dbo].[us_states_population](
	[Geographic_Area] [nvarchar](150) NULL,
	[Population_Estimate_of_20200401] [int] NULL,
	[Population_Estimate_of_20200701] [int] NULL,
	[Population_Estimate_of_20210701] [int] NULL,
	[Population_Estimate_of_20220701] [int] NULL,
	[Population_Estimate_of_20230701] [int] NULL,
	[ID] [int] NOT NULL,
PRIMARY KEY CLUSTERED ([ID] ASC)
);
"""

prompts = [
    'Which US state had the most corona deaths?'
    , 'Which US state was the last one to have its first corona death and when was that?'
    , 'Which US state had, relative to its population, the least amount of corona cases and what was that percentage?'
    , 'How many daily new corona cases where there on average for each US state?'
    , 'In which month occurred the most corona cases within a single US state and which state was that?'
]
