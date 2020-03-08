CREATE VIEW [runningQueries]
AS
SELECT sqltext.TEXT,
req.session_id,
req.status,
req.command,
req.cpu_time,
req.total_elapsed_time
FROM sys.dm_exec_requests req
CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS sqltext
GO

CREATE OR ALTER PROCEDURE [usr].[CreateUser]
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
	END
	ELSE
	BEGIN
		SET @responseMessage ='Email already has a registered account'
	END
    END TRY
    BEGIN CATCH
        SET @responseMessage='Failure due to exception'
    END CATCH

END
GO

CREATE OR ALTER PROCEDURE [usr].[UserLogin]
    @Email VARCHAR(50), 
    @Password VARCHAR(50),
    @responseMessage VARCHAR(50)='' OUTPUT
AS
BEGIN

    SET NOCOUNT ON

    DECLARE @userID UNIQUEIDENTIFIER

    IF EXISTS (SELECT TOP 1 UserID FROM [usr].[User] WHERE Email=@Email)
    BEGIN
		BEGIN
			SET @userID=(SELECT UserID FROM [usr].[User] WHERE Email=@Email AND Pass=HASHBYTES('SHA2_512', @Password+CAST(Salt AS NVARCHAR(36))))

			IF(@userID IS NULL)
				SET @responseMessage='Incorrect password'
			ELSE 
				SET @responseMessage='Login successful'
		END
    END
    ELSE
       SET @responseMessage='Invalid email address'

END
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