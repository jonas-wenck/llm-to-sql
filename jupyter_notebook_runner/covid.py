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

additional_context = """
Use T-SQL syntax.
There are two tables here: 'covid' and 'us_states_population'.
The table 'covid' contains data about the number of covid cases and covid deaths for each day and US state. 
The numbers are cumulative meaning that the cases and deaths of previous dates are always included and do not need to be summed up for the total.
The column 'date' is the date of the covid cases and deaths. The 'state' is the US state where the covid cases and deaths occurred.
The column 'fips' contains the 'Federal Information Processing Standard' code for that state.
The column 'cases' contains the amount of covid cases in that state until that date.
The column 'deaths' contains the amount of covid deaths in that state until that date.
The column 'id' is the primary key of the table and has no inherent meaning.
The table 'us_states_population' contains data about the estimated populations of the different US states.
The column 'Geographic_Area' contains the name of the US state.
The column 'Population_Estimate_of_20200401' contains the estimated population of that US state as of 01.04.2020.
The other columns with similar names contain the estimated population of that US state for the date given in the column name.
The column 'ID' is the primary key of the table and has no inherent meaning.
"""