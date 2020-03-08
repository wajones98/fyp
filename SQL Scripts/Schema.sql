CREATE DATABASE [MetaData]
GO

USE [MetaData]
GO

CREATE SCHEMA [usr]
GO

CREATE TABLE [usr].[User](
	[UserID] UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
	[Email] [varchar](64) NOT NULL UNIQUE,
	[FirstName] [varchar](64) NOT NULL,
	[LastName] [varchar](64) NOT NULL,
	[Pass] [binary](64) NOT NULL,
	[Salt] [uniqueidentifier] NOT NULL,
	[Institution] UNIQUEIDENTIFIER NULL
)
GO

CREATE TABLE [usr].[Institution] (
	[InstitutionID] UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
	[Name] VARCHAR(64) NOT NULL,
	[Desc] VARCHAR(512) NULL,
	[Owner] UNIQUEIDENTIFIER NOT NULL
)

ALTER TABLE [usr].[Institution]  WITH CHECK ADD FOREIGN KEY([Owner])
REFERENCES [usr].[User] ([UserID])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([Institution])
REFERENCES [usr].[Institution] ([InstitutionID])
GO


CREATE SCHEMA [prj]
GO

CREATE TABLE [prj].[ProjectMember] (
	[UserID] UNIQUEIDENTIFIER,
	[ProjectID] UNIQUEIDENTIFIER,
	[JoinDate] DATE,
	PRIMARY KEY CLUSTERED 
	(
		[UserID] ASC, 
		[ProjectID] ASC 
	)
)
GO

CREATE TABLE [prj].[Project] (
	[ProjectID] UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
	[Creator] UNIQUEIDENTIFIER,
	[Name] VARCHAR(256),
	[Desc] VARCHAR(512),
	[StartDate] DATE,
	[EndDate] DATE,
	[Public] BIT
)
GO



CREATE SCHEMA [metadata]
GO

CREATE TABLE [metadata].[File] (
	FileID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
	UserID UNIQUEIDENTIFIER,
	SignalType VARCHAR(64),
	Species VARCHAR(64),
	Gender BIT,
	Age INT,
	[Target] VARCHAR(64),
	[Action] VARCHAR(64)
)
GO

CREATE TABLE [metadata].[FileHistory](
	FileID UNIQUEIDENTIFIER,
	UserID UNIQUEIDENTIFIER,
	ProjectID UNIQUEIDENTIFIER,
	Change VARCHAR(64),
	Filepath VARCHAR(256),
	Active BIT,
	StartDate DATE,
	EndDate DATE
)
GO

CREATE TABLE [metadata].[Tag] (
	FileID UNIQUEIDENTIFIER DEFAULT NEWID(),
	TagKey VARCHAR(64),
	TagValue VARCHAR(64),
	PRIMARY KEY CLUSTERED (
		[FileID] ASC,
		[TagKey] ASC
	)
)
GO

ALTER TABLE [metadata].[FileHistory] WITH CHECK ADD FOREIGN KEY([FileID])
REFERENCES [metadata].[File]([FileID])
GO
ALTER TABLE [metadata].[FileHistory] WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User]([UserID])
GO
ALTER TABLE [metadata].[FileHistory] WITH CHECK ADD FOREIGN KEY([ProjectID])
REFERENCES [prj].[Project]([ProjectID])
GO
