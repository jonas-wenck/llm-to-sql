SCHEMA = "CREATE TABLE Personnel (\
        StaffID text(9) CONSTRAINT StaffPK PRIMARY KEY,\
        LastName text(15) not null,\
        FirstName text(15) not null,\
        Birthday date,\
        Department text(12) null);"

QUESTION = "Find all staff with a birthday after 15.4.1964"
