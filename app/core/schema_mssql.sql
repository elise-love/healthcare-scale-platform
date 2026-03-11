-- SQL Server schema for Healthcare Scale Platform (idempotent)

-- USERS (for login/auth)
IF OBJECT_ID(N'dbo.users', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.users (
    user_id       UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    email         NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    created_at    DATETIME2 NOT NULL CONSTRAINT DF_users_created_at DEFAULT SYSUTCDATETIME()
  );
END;

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_users_email' AND object_id = OBJECT_ID('dbo.users'))
  CREATE INDEX idx_users_email ON dbo.users(email);

-- USERS (for register/login)
IF OBJECT_ID(N'dbo.users', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.users (
    user_id       UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    email         NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    created_at    DATETIME2 NOT NULL CONSTRAINT DF_users_created_at DEFAULT SYSUTCDATETIME()
  );
END;

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_users_email' AND object_id = OBJECT_ID('dbo.users'))
  CREATE INDEX idx_users_email ON dbo.users(email);

--create table if scale doesn't exist
IF OBJECT_ID(N'dbo.scales', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.scales (
    scale_id   NVARCHAR(255) NOT NULL PRIMARY KEY,
    name       NVARCHAR(255) NOT NULL,
    short_name NVARCHAR(255) NULL,
    language   NVARCHAR(50)  NULL,
    created_at DATETIME2     NOT NULL CONSTRAINT DF_scales_created_at DEFAULT SYSUTCDATETIME()
  );
END;

--for different version scales
IF OBJECT_ID(N'dbo.scale_versions', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.scale_versions (
    scale_id        NVARCHAR(255) NOT NULL,
    version         NVARCHAR(50)  NOT NULL,
    definition_json NVARCHAR(MAX) NOT NULL, --save as json
    created_at      DATETIME2     NOT NULL CONSTRAINT DF_scale_versions_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_scale_versions PRIMARY KEY (scale_id, version),
    CONSTRAINT FK_scale_versions_scales FOREIGN KEY (scale_id)
      REFERENCES dbo.scales(scale_id) ON DELETE CASCADE--delete all version if scale is deleted
  );
END;

--scale items
IF OBJECT_ID(N'dbo.scale_items', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.scale_items (
    scale_id   NVARCHAR(255) NOT NULL,
    version    NVARCHAR(50)  NOT NULL,
    item_id    NVARCHAR(255) NOT NULL,
    item_order INT           NOT NULL,
    [text]     NVARCHAR(MAX) NOT NULL,
    item_type  NVARCHAR(50)  NOT NULL CONSTRAINT DF_scale_items_item_type DEFAULT 'single_choice',
    reverse    BIT           NOT NULL CONSTRAINT DF_scale_items_reverse DEFAULT 0,
    weight     FLOAT         NOT NULL CONSTRAINT DF_scale_items_weight DEFAULT 1.0,
    CONSTRAINT PK_scale_items PRIMARY KEY (scale_id, version, item_id),
    CONSTRAINT FK_scale_items_scale_versions FOREIGN KEY (scale_id, version)
      REFERENCES dbo.scale_versions(scale_id, version) ON DELETE CASCADE
  );
END;

--different kinds of options
IF OBJECT_ID(N'dbo.scale_options', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.scale_options (
    scale_id   NVARCHAR(255) NOT NULL,
    version    NVARCHAR(50)  NOT NULL,
    option_key NVARCHAR(255) NOT NULL, --yes/no/0/1/2/3/never/somtimes/etc
    label      NVARCHAR(255) NOT NULL,
    CONSTRAINT PK_scale_options PRIMARY KEY (scale_id, version, option_key),
    CONSTRAINT FK_scale_options_scale_versions FOREIGN KEY (scale_id, version)
      REFERENCES dbo.scale_versions(scale_id, version) ON DELETE CASCADE
  );
END;

--result data as one assessment
IF OBJECT_ID(N'dbo.assessments', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.assessments (
    assessment_id  UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    scale_id       NVARCHAR(255) NOT NULL,
    version        NVARCHAR(50)  NOT NULL,
    subject_id UNIQUEIDENTIFIER NULL,
    total_score    FLOAT         NOT NULL, --total score
    interpretation NVARCHAR(MAX) NULL, --interpretation of the score, from the original chart
    answers_json   NVARCHAR(MAX) NOT NULL, --save as json
    created_at     DATETIME2     NOT NULL CONSTRAINT DF_assessments_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_assessments_scale_versions FOREIGN KEY (scale_id, version)
      REFERENCES dbo.scale_versions(scale_id, version)
  );
END;

--detailed answer data for each item in the assessment
IF OBJECT_ID(N'dbo.assessment_answers', N'U') IS NULL
BEGIN
  CREATE TABLE dbo.assessment_answers (
    assessment_id UNIQUEIDENTIFIER NOT NULL,
    item_id       NVARCHAR(255) NOT NULL,
    answer_value  NVARCHAR(255) NOT NULL,
    score         FLOAT         NOT NULL,
    CONSTRAINT PK_assessment_answers PRIMARY KEY (assessment_id, item_id),
    CONSTRAINT FK_assessment_answers_assessments FOREIGN KEY (assessment_id)
      REFERENCES dbo.assessments(assessment_id) ON DELETE CASCADE
  );
END;

--search for all items of a scale version, so index on scale_id, version, as item_order
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_scale_items_order' AND object_id = OBJECT_ID('dbo.scale_items'))
  CREATE INDEX idx_scale_items_order ON dbo.scale_items(scale_id, version, item_order);

--search for specific user's history , so index on subject_id and created_at
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_assessments_subject_time' AND object_id = OBJECT_ID('dbo.assessments'))
  CREATE INDEX idx_assessments_subject_time ON dbo.assessments(subject_id, created_at);

--search for specific item's statistical analysis, so index on item_id
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_answers_item' AND object_id = OBJECT_ID('dbo.assessment_answers'))
  CREATE INDEX idx_answers_item ON dbo.assessment_answers(item_id);