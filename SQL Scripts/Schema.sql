USE [fyp]
GO
CREATE SCHEMA [usr]
GO
CREATE TABLE [User](
	UserID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
	[Email] [varchar](50) NOT NULL UNIQUE,
	[FirstName] [varchar](40) NOT NULL,
	[LastName] [varchar](40) NOT NULL,
	[Pass] [binary](64) NOT NULL,
	[Salt] [uniqueidentifier] NOT NULL,
	[DepartmentCode] [char](5) NOT NULL
)
GO