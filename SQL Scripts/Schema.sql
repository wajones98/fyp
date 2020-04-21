USE [MetaData]
GO

CREATE SCHEMA [metadata]
GO

CREATE SCHEMA [prj]
GO

CREATE SCHEMA [usr]
GO

/****** Object:  Table [metadata].[Dataset]    Script Date: 22/04/2020 00:44:18 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [metadata].[Dataset](
	[DatasetID] [uniqueidentifier] NOT NULL,
	[DatasetName] [varchar](64) NULL,
PRIMARY KEY CLUSTERED 
(
	[DatasetID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [metadata].[File]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [metadata].[File](
	[FileID] [uniqueidentifier] NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[SignalType] [varchar](64) NOT NULL,
	[Species] [varchar](64) NOT NULL,
	[Gender] [bit] NOT NULL,
	[Age] [int] NOT NULL,
	[Target] [varchar](64) NOT NULL,
	[Action] [varchar](64) NOT NULL,
	[DataSet] [uniqueidentifier] NULL,
	[ChannelCount] [int] NOT NULL,
	[Device] [varchar](256) NOT NULL,
	[FileName] [varchar](64) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[FileID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [metadata].[FileHistory]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [metadata].[FileHistory](
	[FileID] [uniqueidentifier] NULL,
	[UserID] [uniqueidentifier] NULL,
	[ProjectID] [uniqueidentifier] NULL,
	[Change] [varchar](64) NULL,
	[Filepath] [varchar](256) NOT NULL,
	[Active] [bit] NULL,
	[StartDate] [date] NULL,
	[EndDate] [date] NULL,
	[Previous] [varchar](256) NULL,
	[PreviousChange] [varchar](64) NULL,
PRIMARY KEY CLUSTERED 
(
	[Filepath] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [metadata].[Tag]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [metadata].[Tag](
	[DatasetId] [uniqueidentifier] NOT NULL,
	[TagKey] [varchar](64) NOT NULL,
	[TagValue] [varchar](64) NULL,
PRIMARY KEY CLUSTERED 
(
	[DatasetId] ASC,
	[TagKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [prj].[Project]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [prj].[Project](
	[ProjectID] [uniqueidentifier] NOT NULL,
	[Creator] [uniqueidentifier] NULL,
	[Name] [varchar](256) NULL,
	[Desc] [varchar](512) NULL,
	[StartDate] [date] NULL,
	[EndDate] [date] NULL,
	[Public] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ProjectID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [prj].[ProjectMember]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [prj].[ProjectMember](
	[UserID] [uniqueidentifier] NOT NULL,
	[ProjectID] [uniqueidentifier] NOT NULL,
	[Pending] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[UserID] ASC,
	[ProjectID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[Institution]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[Institution](
	[InstitutionID] [uniqueidentifier] NOT NULL,
	[Name] [varchar](64) NOT NULL,
	[Desc] [varchar](512) NULL,
	[Owner] [uniqueidentifier] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[InstitutionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[InstitutionMember]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[InstitutionMember](
	[InstitutionId] [uniqueidentifier] NOT NULL,
	[UserId] [uniqueidentifier] NULL,
	[Role] [varchar](50) NULL,
	[Pending] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[InstitutionId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[Session]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[Session](
	[UserID] [uniqueidentifier] NOT NULL,
	[SessionID] [uniqueidentifier] NULL,
	[Expiry] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[UserID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[User]    Script Date: 22/04/2020 00:44:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[User](
	[UserID] [uniqueidentifier] NOT NULL,
	[Email] [varchar](64) NOT NULL,
	[FirstName] [varchar](64) NOT NULL,
	[LastName] [varchar](64) NOT NULL,
	[Pass] [binary](64) NOT NULL,
	[Salt] [uniqueidentifier] NOT NULL,
	[Institution] [uniqueidentifier] NULL,
PRIMARY KEY CLUSTERED 
(
	[UserID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [metadata].[Dataset] ADD  DEFAULT (newid()) FOR [DatasetID]
GO

ALTER TABLE [metadata].[File] ADD  DEFAULT (newid()) FOR [FileID]
GO

ALTER TABLE [prj].[Project] ADD  DEFAULT (newid()) FOR [ProjectID]
GO

ALTER TABLE [prj].[ProjectMember] ADD  DEFAULT ((1)) FOR [Pending]
GO

ALTER TABLE [usr].[Institution] ADD  DEFAULT (newid()) FOR [InstitutionID]
GO

ALTER TABLE [usr].[User] ADD  DEFAULT (newid()) FOR [UserID]
GO

ALTER TABLE [metadata].[File]  WITH CHECK ADD FOREIGN KEY([DataSet])
REFERENCES [metadata].[Dataset] ([DatasetID])
GO

ALTER TABLE [metadata].[FileHistory]  WITH CHECK ADD FOREIGN KEY([FileID])
REFERENCES [metadata].[File] ([FileID])
GO

ALTER TABLE [metadata].[FileHistory]  WITH CHECK ADD FOREIGN KEY([FileID])
REFERENCES [metadata].[File] ([FileID])
GO

ALTER TABLE [metadata].[FileHistory]  WITH CHECK ADD FOREIGN KEY([ProjectID])
REFERENCES [prj].[Project] ([ProjectID])
GO

ALTER TABLE [metadata].[FileHistory]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User] ([UserID])
GO

ALTER TABLE [metadata].[Tag]  WITH CHECK ADD FOREIGN KEY([DatasetId])
REFERENCES [metadata].[Dataset] ([DatasetID])
GO

ALTER TABLE [prj].[ProjectMember]  WITH CHECK ADD FOREIGN KEY([ProjectID])
REFERENCES [prj].[Project] ([ProjectID])
ON DELETE CASCADE
GO

ALTER TABLE [usr].[Institution]  WITH CHECK ADD FOREIGN KEY([Owner])
REFERENCES [usr].[User] ([UserID])
GO

ALTER TABLE [usr].[InstitutionMember]  WITH CHECK ADD FOREIGN KEY([InstitutionId])
REFERENCES [usr].[Institution] ([InstitutionID])
GO

ALTER TABLE [usr].[InstitutionMember]  WITH CHECK ADD FOREIGN KEY([UserId])
REFERENCES [usr].[User] ([UserID])
GO

ALTER TABLE [usr].[Session]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User] ([UserID])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([Institution])
REFERENCES [usr].[Institution] ([InstitutionID])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([Institution])
REFERENCES [usr].[Institution] ([InstitutionID])
GO

CREATE     TRIGGER [metadata].[InitSlowlyChangingDimension]
ON [metadata].[File]
AFTER INSERT
NOT FOR REPLICATION
AS
BEGIN

	DECLARE @FileID VARCHAR(256) = (SELECT TOP 1 [FileID] FROM inserted)
	DECLARE @UserID UNIQUEIDENTIFIER = (SELECT TOP 1 [UserID] FROM inserted)
	DECLARE @FileName VARCHAR(64) = (SELECT TOP 1 [FileName] FROM inserted)
	DECLARE @DatasetID VARCHAR(256) = (SELECT TOP 1 [Dataset] FROM inserted)
	DECLARE @FilePath VARCHAR(256) = @DatasetID + '/' + @FileID + '-' + @FileName
	INSERT INTO [metadata].[FileHistory]
           ([FileID]
           ,[UserID]
           ,[ProjectID]
           ,[Change]
           ,[Filepath]
           ,[Active]
           ,[StartDate]
           ,[EndDate])
     VALUES
           (@FileID
           ,@UserID
           ,NULL
           ,'source'
           ,@FilePath
           ,1
           ,GETDATE()
           ,NULL)

END
GO

ALTER TABLE [metadata].[File] ENABLE TRIGGER [InitSlowlyChangingDimension]
GO

CREATE VIEW [metadata].[Search]
AS
SELECT
	f.[FileID]
	,f.[Filename]
	,d.[DatasetName]
	,ISNULL(p.[Name],'none') AS [ProjectName] 
	,f.[SignalType]
	,f.[Species]
	,CASE
		WHEN f.[Gender] = 0 THEN 'Male'
		WHEN f.[Gender] = 1 THEN 'Female'
	END AS Gender
	,f.[Age]
	,f.[Target]
	,f.[Action]
	,f.[ChannelCount]
	,f.[Device]
	,fh.[Change]
	,fh.[Filepath]
	,d.[DatasetID]
	,p.[ProjectID]
	,fh.[Previous]
	,fh.[PreviousChange]
FROM 
	[MetaData].[metadata].[File] f
	INNER JOIN
	[MetaData].[metadata].[Dataset] d
ON
	f.[DataSet] = d.[DatasetID]
	INNER JOIN
	[MetaData].[metadata].[FileHistory] fh
ON
	f.[FileID] = fh.[FileID]
	LEFT JOIN
	[MetaData].[prj].[Project] p
ON
	p.[ProjectID] = fh.[ProjectID]
WHERE
	fh.[Active] = 1
	AND
	(SELECT ISNULL(p.[Public],1)) = 1
GO

/****** Object:  View [metadata].[SearchPrivate]    Script Date: 22/04/2020 00:45:15 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO







CREATE VIEW [metadata].[SearchPrivate]
AS
SELECT
	f.[FileID]
	,f.[Filename]
	,d.[DatasetName]
	,ISNULL(p.[Name],'none') AS [ProjectName] 
	,f.[SignalType]
	,f.[Species]
	,CASE
		WHEN f.[Gender] = 0 THEN 'Male'
		WHEN f.[Gender] = 1 THEN 'Female'
	END AS Gender
	,f.[Age]
	,f.[Target]
	,f.[Action]
	,f.[ChannelCount]
	,f.[Device]
	,fh.[Change]
	,fh.[Filepath]
	,d.[DatasetID]
	,p.[ProjectID]
	,fh.[Previous]
	,fh.[PreviousChange]
FROM 
	[MetaData].[metadata].[File] f
	INNER JOIN
	[MetaData].[metadata].[Dataset] d
ON
	f.[DataSet] = d.[DatasetID]
	INNER JOIN
	[MetaData].[metadata].[FileHistory] fh
ON
	f.[FileID] = fh.[FileID]
	LEFT JOIN
	[MetaData].[prj].[Project] p
ON
	p.[ProjectID] = fh.[ProjectID]
WHERE
	fh.[Active] = 1
GO

USE [MetaData]
GO

/****** Object:  StoredProcedure [metadata].[GetOrInsertDataSet]    Script Date: 22/04/2020 00:45:53 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [metadata].[GetOrInsertDataSet]
(
	@DatasetName VARCHAR(64),
	@DataSetId VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
	SET NOCOUNT ON
	BEGIN TRY
	IF NOT EXISTS(SELECT TOP 1 [DatasetID] FROM [metadata].[Dataset] WHERE [DatasetID] = @DataSetId)
	BEGIN
		INSERT INTO 
			[metadata].[Dataset] 
			([DatasetID], [DatasetName])
		VALUES
			(@DatasetID, @DatasetName)
		SET @responseMessage = 'DataSet created'
		RETURN 201
	END
	ELSE
	BEGIN
		SET @responseMessage = 'DataSet already exists'
		RETURN 200
	END
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [metadata].[InsertFileMetaData]    Script Date: 22/04/2020 00:45:53 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO









CREATE    PROCEDURE [metadata].[InsertFileMetaData]
(
	@FileID VARCHAR(256)
	,@FileName VARCHAR(64)
    ,@UserID VARCHAR(256)
    ,@SignalType VARCHAR(64)
    ,@Species VARCHAR(64)
    ,@Gender BIT
    ,@Age VARCHAR(64)
    ,@Target VARCHAR(64)
    ,@Action VARCHAR(64)
	,@Device VARCHAR(64)
	,@Dataset VARCHAR(256)
	,@ChannelCount INT
	,@responseMessage NVARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
BEGIN TRY
	INSERT INTO [metadata].[File]
			   ([FileID]
			   ,[FileName]
			   ,[UserID]
			   ,[SignalType]
			   ,[Species]
			   ,[Gender]
			   ,[Age]
			   ,[Target]
			   ,[Action]
			   ,[Device]
			   ,[Dataset]
			   ,[ChannelCount])
		 VALUES
			   (@FileID,
			   @FileName,
			   @UserID,			   
			   @SignalType,
			   @Species,
			   @Gender,
			   @Age,
			   @Target,
			   @Action,
			   @Device,
			   @Dataset,
			   @ChannelCount)
	SET @responseMessage = 'Metadata inserted successfully'
	RETURN 201
END TRY
BEGIN CATCH
	SET @responseMessage = 'Failure due to exception'
	RETURN 500
END CATCH
END
GO

/****** Object:  StoredProcedure [prj].[AcceptProjectInvite]    Script Date: 22/04/2020 00:45:53 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [prj].[AcceptProjectInvite]
(
	@UserId VARCHAR(256),
	@ProjectId VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		UPDATE
			[prj].[ProjectMember]
		SET
			[Pending] = 0
		WHERE
			[ProjectID] = @ProjectId
			AND
			[UserId] = @UserId
		SET @responseMessage = 'Project joined successfully'
		RETURN 201
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [prj].[CreateProject]    Script Date: 22/04/2020 00:45:53 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [prj].[CreateProject]
(
	@Creator VARCHAR(256),
	@Name VARCHAR(256),
	@Desc VARCHAR(512),
	@Public BIT,
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		INSERT INTO
			[prj].[Project]
			(
				[Creator]
				,[Name]
				,[Desc]
				,[StartDate]
				,[EndDate]
				,[Public]
			)
		VALUES
			(@Creator, @Name, @Desc, GETDATE(), NULL, @Public)
		SET @responseMessage = 'Project created successfully'
		RETURN 201
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [prj].[InviteUserToProject]    Script Date: 22/04/2020 00:45:53 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [prj].[InviteUserToProject]
(
	@UserId VARCHAR(256),
	@ProjectId VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		INSERT INTO
			[prj].[ProjectMember]
			(
				[UserId],
				[ProjectID]
			)
		VALUES
			(@UserId, @ProjectId)
		SET @responseMessage = 'User invited successfully'
		RETURN 201
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [prj].[RemoveProject]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [prj].[RemoveProject]
(
	@UserId VARCHAR(256),
	@ProjectId VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		IF EXISTS (SELECT TOP 1 [ProjectId] FROM [prj].[Project] WHERE [Creator] = @UserId AND [ProjectId] = @ProjectId)
		BEGIN
			DELETE FROM
				[prj].[Project]
			 WHERE 
			 [Creator] = @UserId 
			 AND 
			 [ProjectId] = @ProjectId
			SET @responseMessage = 'Project deleted'
			RETURN 200				
		END
		ELSE
		BEGIN
			DELETE FROM
				[prj].[ProjectMember]
			WHERE
				[ProjectID] = @ProjectId
				AND
				[UserId] = @UserId
			SET @responseMessage = 'Project left'
			RETURN 200
		END

	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[AcceptInstitutionInvite]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [usr].[AcceptInstitutionInvite]
(
	@UserId VARCHAR(256),
	@InstitutionId VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		
		UPDATE
			[usr].[InstitutionMember]
		SET
			[Pending] = 0
		WHERE
			[UserId] = @UserId
		
		UPDATE 
			[usr].[User]
		SET
			[Institution] = @InstitutionId
		WHERE
			[UserID] = @UserId

		DELETE FROM
			[usr].[InstitutionMember]
		WHERE
			[UserId] = @UserId
			AND
			[Pending] = 1
		SET @responseMessage = 'Institution joined successfully'
		RETURN 201
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[CheckSessionID]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE   PROCEDURE [usr].[CheckSessionID]
(
	@SessionID VARCHAR(256),
	@responseMessage NVARCHAR(250) OUTPUT
)
AS
BEGIN
	BEGIN TRY
		IF NOT EXISTS (SELECT TOP 1 [SessionID] FROM [usr].[Session] WHERE [SessionID] = @SessionID)
		BEGIN
			SET @responseMessage = 'Session does not exist'
			RETURN 401
		END
		ELSE IF ((SELECT GETDATE()) > (SELECT TOP 1 [Expiry] FROM [usr].[Session] WHERE [SessionID] = @SessionID))
		BEGIN
			DELETE FROM [usr].[Session] WHERE [SessionID] = @SessionID
			SET @responseMessage = 'Session expired'
			RETURN 401
		END
		ELSE
		BEGIN
			UPDATE [usr].[Session] SET [Expiry] = DATEADD(hh,1,GETDATE()) WHERE [SessionID] = @SessionID
			SET @responseMessage = 'Session ok'
			RETURN 200
		END
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[CheckUserSession]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE   PROCEDURE [usr].[CheckUserSession]
(
	@UserID VARCHAR(256),
	@responseMessage NVARCHAR(250) OUTPUT
)
AS
BEGIN
	BEGIN TRY
		IF NOT EXISTS (SELECT TOP 1 [UserID] FROM [usr].[Session] WHERE [UserID] = @UserID)
		BEGIN
			SET @responseMessage = NEWID()
			INSERT INTO 
				[usr].[Session] 
				([UserID], [SessionID], [Expiry]) 
			VALUES
				(@UserID, @responseMessage, DATEADD(hh,1,GETDATE()))
			RETURN 200
		END
		ELSE
		BEGIN
			SET @responseMessage = NEWID()
			UPDATE [usr].[Session] SET [Expiry] = DATEADD(hh,1,GETDATE()), [SessionID] = @responseMessage WHERE [UserID] = @UserID
			SET @responseMessage = (SELECT TOP 1 [SessionID] FROM [usr].[Session] WHERE [UserID] = @UserID)
			RETURN 201
		END
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[CreateInstitution]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [usr].[CreateInstitution]
(
	@Name VARCHAR(64),
	@Desc VARCHAR(512),
	@Owner VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		DECLARE @InstitutionId UNIQUEIDENTIFIER = NEWID()
		INSERT INTO
			[usr].[Institution]
			([InstitutionID],
			[Name],
			[Desc],
			[Owner])
		VALUES
			(@InstitutionId, @Name, @Desc, @Owner)
		UPDATE
			[usr].[User]
		SET
			[Institution] = @InstitutionId
		WHERE
			[UserID] = @Owner
		SET @responseMessage = 'Institution created successfully'
		RETURN 201
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[CreateUser]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [usr].[CreateUser]
(
    @Email VARCHAR(50), 
    @Password VARCHAR(50),
    @FirstName VARCHAR(40) = NULL, 
    @LastName VARCHAR(40) = NULL,
    @responseMessage NVARCHAR(250) OUTPUT
)
AS

BEGIN
    SET NOCOUNT ON

    DECLARE @salt UNIQUEIDENTIFIER=NEWID()
    BEGIN TRY
	IF NOT EXISTS (SELECT TOP 1 [Email] FROM [usr].[User] WHERE [Email] = @Email)
	BEGIN
		INSERT INTO [usr].[User] (Email, FirstName, LastName, Pass, Salt)
		VALUES(@Email, @FirstName, @LastName, HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36))), @salt)

       SET @responseMessage='User successfully registered'
	   RETURN 200
	END
	ELSE
	BEGIN
		SET @responseMessage ='Email already has a registered account'
		RETURN 500
	END
    END TRY
    BEGIN CATCH
        SET @responseMessage='Failure due to exception'
		RETURN 500
    END CATCH

END
GO

/****** Object:  StoredProcedure [usr].[GetUserIDFromSession]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE   PROCEDURE [usr].[GetUserIDFromSession]
(
	@sessionID VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		IF NOT EXISTS(SELECT TOP 1 [SessionID] FROM [usr].[Session] WHERE [SessionID] = @sessionID)
		BEGIN
			SET @responseMessage = 'Session does not exist'
			RETURN 401
		END
		ELSE IF ((SELECT GETDATE()) > (SELECT TOP 1 [Expiry] FROM [usr].[Session] WHERE [SessionID] = @SessionID))
		BEGIN
			DELETE FROM [usr].[Session] WHERE [SessionID] = @sessionID
			SET @responseMessage = 'Session expired'
			RETURN 404
		END
		ELSE
		BEGIN
			UPDATE 
				[usr].[Session] 
			SET
				[Expiry] = DATEADD(hh,1,GETDATE())
			WHERE
				[SessionID] = @sessionID
			SET @responseMessage = (SELECT TOP 1 [UserID] FROM [usr].[Session] WHERE [SessionID] = @sessionID)
			RETURN 200
		END
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[InviteUserToInstitution]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [usr].[InviteUserToInstitution]
(
	@UserId VARCHAR(256),
	@InstitutionId VARCHAR(256),
	@Role VARCHAR(50),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		INSERT INTO
			[usr].[InstitutionMember]
			(
				[InstitutionId],
				[UserId],
				[Role],
				[Pending]
			)
		VALUES
			(@InstitutionId, @UserId, @Role, 1)
		SET @responseMessage = 'User invited to institution'
		RETURN 201
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[RemoveUserFromInstitution]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [usr].[RemoveUserFromInstitution]
(
	@UserId VARCHAR(256),
	@InstitutionId VARCHAR(256),
	@responseMessage VARCHAR(256) OUTPUT
)
AS
BEGIN
SET NOCOUNT ON
	BEGIN TRY
		
		DELETE FROM
			[usr].[InstitutionMember]
		WHERE
			[UserId] = @UserId
			AND
			[InstitutionId] = @InstitutionId
		
		UPDATE
			[usr].[User]
		SET
			[Institution] = NULL
		WHERE
			[UserID] = @UserId

		SET @responseMessage = 'User successfully removed from institution'
		RETURN 200
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[updatePassword]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [usr].[updatePassword]
(
	@UserID VARCHAR(250),
	@Password VARCHAR(50),
	@responseMessage VARCHAR(250) OUTPUT
)
AS
BEGIN
	SET NOCOUNT ON
	BEGIN TRY
		DECLARE @Salt UNIQUEIDENTIFIER = (SELECT TOP 1 [Salt] FROM [usr].[User] WHERE [UserID] = @UserID)
		DECLARE @newPassword BINARY(64) = HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36)))
		DECLARE @oldPassword BINARY(64) = (SELECT TOP 1 [Pass] FROM [usr].[User] WHERE [UserID] = @UserID)
		IF @newPassword != @oldPassword
		BEGIN
			UPDATE
				[usr].[User]
			SET
				[Pass] = HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36)))
			WHERE
				[UserID] = @UserID
			SET @responseMessage = 'Password changed successfully'
		END
		ELSE
		BEGIN
			SET @responseMessage = 'New password cannot be the same as an old password'
		END
	
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[UserLogin]    Script Date: 22/04/2020 00:45:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE   PROCEDURE [usr].[UserLogin]
    @Email VARCHAR(50), 
    @Password VARCHAR(50),
    @responseMessage VARCHAR(50)='' OUTPUT
AS
BEGIN
	BEGIN TRY
		SET NOCOUNT ON

		DECLARE @userID VARCHAR(256)
		DECLARE	@returnValue INT

		IF EXISTS (SELECT TOP 1 UserID FROM [usr].[User] WHERE Email=@Email)
		BEGIN
			BEGIN
				SET @userID=(SELECT UserID FROM [usr].[User] WHERE Email=@Email AND Pass=HASHBYTES('SHA2_512', @Password+CAST(Salt AS NVARCHAR(36))))

				IF(@userID IS NULL)
				BEGIN
					SET @responseMessage='Incorrect password'
					RETURN 500
					END
				ELSE
				BEGIN
						EXEC @returnValue = [usr].[CheckUserSession]
						@UserID = @userID,
						@responseMessage = @responseMessage OUTPUT
					RETURN @returnValue
				END
			END
		END
		ELSE
		BEGIN
		   SET @responseMessage='Invalid email address'
		   RETURN 500
		END
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
		RETURN 500
	END CATCH
END
GO


