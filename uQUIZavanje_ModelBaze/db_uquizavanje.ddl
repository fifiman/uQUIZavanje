
CREATE TYPE [Id]
	FROM INTEGER NULL
go

CREATE TABLE [Friendships]
( 
	[Id_first]           [Id]  NOT NULL ,
	[Id_second]          [Id]  NOT NULL 
)
go

ALTER TABLE [Friendships]
	ADD CONSTRAINT [XPKFriendships] PRIMARY KEY  CLUSTERED ([Id_first] ASC,[Id_second] ASC)
go

CREATE TABLE [Games]
( 
	[Id_player_two]      [Id]  NOT NULL ,
	[Id_player_three]    [Id] ,
	[Id_player_four]     [Id] ,
	[Player_one_pts]     integer  NULL ,
	[Player_two_pts]     integer  NULL ,
	[Player_three_pts]   integer  NULL ,
	[Player_four_pts]    integer  NULL ,
	[IdGames]            [Id]  NOT NULL ,
	[Id_player_one]      [Id]  NOT NULL 
)
go

ALTER TABLE [Games]
	ADD CONSTRAINT [XPKGames] PRIMARY KEY  CLUSTERED ([IdGames] ASC)
go

CREATE TABLE [Question]
( 
	[Text]               varchar()  NULL ,
	[Answer_one]         varchar()  NULL ,
	[Answer_two]         varchar()  NULL ,
	[Answer_three]       varchar()  NULL ,
	[Answer_four]        varchar()  NULL ,
	[Correct]            bit  NULL ,
	[IdQuestion]         [Id]  NOT NULL 
)
go

ALTER TABLE [Question]
	ADD CONSTRAINT [XPKQuestion] PRIMARY KEY  CLUSTERED ([IdQuestion] ASC)
go

CREATE TABLE [Users]
( 
	[Username]           varchar(20)  NULL ,
	[Rankings]           char(18)  NULL ,
	[Pictures]           binary  NULL ,
	[Privileges]         varchar()  NULL ,
	[Banned]             bit  NULL ,
	[IdUsers]            [Id]  NOT NULL 
)
go

ALTER TABLE [Users]
	ADD CONSTRAINT [XPKUsers] PRIMARY KEY  CLUSTERED ([IdUsers] ASC)
go


ALTER TABLE [Friendships]
	ADD CONSTRAINT [R_7] FOREIGN KEY ([Id_first]) REFERENCES [Users]([IdUsers])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go

ALTER TABLE [Friendships]
	ADD CONSTRAINT [R_8] FOREIGN KEY ([Id_second]) REFERENCES [Users]([IdUsers])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go


ALTER TABLE [Games]
	ADD CONSTRAINT [R_3] FOREIGN KEY ([Id_player_two]) REFERENCES [Users]([IdUsers])
		ON UPDATE CASCADE
go

ALTER TABLE [Games]
	ADD CONSTRAINT [R_4] FOREIGN KEY ([Id_player_three]) REFERENCES [Users]([IdUsers])
		ON UPDATE CASCADE
go

ALTER TABLE [Games]
	ADD CONSTRAINT [R_5] FOREIGN KEY ([Id_player_four]) REFERENCES [Users]([IdUsers])
		ON UPDATE CASCADE
go

ALTER TABLE [Games]
	ADD CONSTRAINT [R_6] FOREIGN KEY ([Id_player_one]) REFERENCES [Users]([IdUsers])
		ON UPDATE CASCADE
go


CREATE TRIGGER tD_Friendships ON Friendships FOR DELETE AS
/* erwin Builtin Trigger */
/* DELETE trigger on Friendships */
BEGIN
  DECLARE  @errno   int,
           @severity int,
           @state    int,
           @errmsg  varchar(255)
    /* erwin Builtin Trigger */
    /* Users  Friendships on child delete no action */
    /* ERWIN_RELATION:CHECKSUM="0002685b", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_8", FK_COLUMNS="Id_second" */
    IF EXISTS (SELECT * FROM deleted,Users
      WHERE
        /* %JoinFKPK(deleted,Users," = "," AND") */
        deleted.Id_second = Users.IdUsers AND
        NOT EXISTS (
          SELECT * FROM Friendships
          WHERE
            /* %JoinFKPK(Friendships,Users," = "," AND") */
            Friendships.Id_second = Users.IdUsers
        )
    )
    BEGIN
      SELECT @errno  = 30010,
             @errmsg = 'Cannot delete last Friendships because Users exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Friendships on child delete no action */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_7", FK_COLUMNS="Id_first" */
    IF EXISTS (SELECT * FROM deleted,Users
      WHERE
        /* %JoinFKPK(deleted,Users," = "," AND") */
        deleted.Id_first = Users.IdUsers AND
        NOT EXISTS (
          SELECT * FROM Friendships
          WHERE
            /* %JoinFKPK(Friendships,Users," = "," AND") */
            Friendships.Id_first = Users.IdUsers
        )
    )
    BEGIN
      SELECT @errno  = 30010,
             @errmsg = 'Cannot delete last Friendships because Users exists.'
      GOTO error
    END


    /* erwin Builtin Trigger */
    RETURN
error:
   RAISERROR (@errmsg, -- Message text.
              @severity, -- Severity (0~25).
              @state) -- State (0~255).
    rollback transaction
END

go


CREATE TRIGGER tU_Friendships ON Friendships FOR UPDATE AS
/* erwin Builtin Trigger */
/* UPDATE trigger on Friendships */
BEGIN
  DECLARE  @numrows int,
           @nullcnt int,
           @validcnt int,
           @insId_first Id, 
           @insId_second Id,
           @errno   int,
           @severity int,
           @state    int,
           @errmsg  varchar(255)

  SELECT @numrows = @@rowcount
  /* erwin Builtin Trigger */
  /* Users  Friendships on child update no action */
  /* ERWIN_RELATION:CHECKSUM="000296ab", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_8", FK_COLUMNS="Id_second" */
  IF
    /* %ChildFK(" OR",UPDATE) */
    UPDATE(Id_second)
  BEGIN
    SELECT @nullcnt = 0
    SELECT @validcnt = count(*)
      FROM inserted,Users
        WHERE
          /* %JoinFKPK(inserted,Users) */
          inserted.Id_second = Users.IdUsers
    /* %NotnullFK(inserted," IS NULL","select @nullcnt = count(*) from inserted where"," AND") */
    
    IF @validcnt + @nullcnt != @numrows
    BEGIN
      SELECT @errno  = 30007,
             @errmsg = 'Cannot update Friendships because Users does not exist.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Friendships on child update no action */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_7", FK_COLUMNS="Id_first" */
  IF
    /* %ChildFK(" OR",UPDATE) */
    UPDATE(Id_first)
  BEGIN
    SELECT @nullcnt = 0
    SELECT @validcnt = count(*)
      FROM inserted,Users
        WHERE
          /* %JoinFKPK(inserted,Users) */
          inserted.Id_first = Users.IdUsers
    /* %NotnullFK(inserted," IS NULL","select @nullcnt = count(*) from inserted where"," AND") */
    
    IF @validcnt + @nullcnt != @numrows
    BEGIN
      SELECT @errno  = 30007,
             @errmsg = 'Cannot update Friendships because Users does not exist.'
      GOTO error
    END
  END


  /* erwin Builtin Trigger */
  RETURN
error:
   RAISERROR (@errmsg, -- Message text.
              @severity, -- Severity (0~25).
              @state) -- State (0~255).
    rollback transaction
END

go




CREATE TRIGGER tD_Games ON Games FOR DELETE AS
/* erwin Builtin Trigger */
/* DELETE trigger on Games */
BEGIN
  DECLARE  @errno   int,
           @severity int,
           @state    int,
           @errmsg  varchar(255)
    /* erwin Builtin Trigger */
    /* Users  Games on child delete no action */
    /* ERWIN_RELATION:CHECKSUM="00048698", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_6", FK_COLUMNS="Id_player_one" */
    IF EXISTS (SELECT * FROM deleted,Users
      WHERE
        /* %JoinFKPK(deleted,Users," = "," AND") */
        deleted.Id_player_one = Users.IdUsers AND
        NOT EXISTS (
          SELECT * FROM Games
          WHERE
            /* %JoinFKPK(Games,Users," = "," AND") */
            Games.Id_player_one = Users.IdUsers
        )
    )
    BEGIN
      SELECT @errno  = 30010,
             @errmsg = 'Cannot delete last Games because Users exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Games on child delete no action */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_5", FK_COLUMNS="Id_player_four" */
    IF EXISTS (SELECT * FROM deleted,Users
      WHERE
        /* %JoinFKPK(deleted,Users," = "," AND") */
        deleted.Id_player_four = Users.IdUsers AND
        NOT EXISTS (
          SELECT * FROM Games
          WHERE
            /* %JoinFKPK(Games,Users," = "," AND") */
            Games.Id_player_four = Users.IdUsers
        )
    )
    BEGIN
      SELECT @errno  = 30010,
             @errmsg = 'Cannot delete last Games because Users exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Games on child delete no action */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_4", FK_COLUMNS="Id_player_three" */
    IF EXISTS (SELECT * FROM deleted,Users
      WHERE
        /* %JoinFKPK(deleted,Users," = "," AND") */
        deleted.Id_player_three = Users.IdUsers AND
        NOT EXISTS (
          SELECT * FROM Games
          WHERE
            /* %JoinFKPK(Games,Users," = "," AND") */
            Games.Id_player_three = Users.IdUsers
        )
    )
    BEGIN
      SELECT @errno  = 30010,
             @errmsg = 'Cannot delete last Games because Users exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Games on child delete no action */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_3", FK_COLUMNS="Id_player_two" */
    IF EXISTS (SELECT * FROM deleted,Users
      WHERE
        /* %JoinFKPK(deleted,Users," = "," AND") */
        deleted.Id_player_two = Users.IdUsers AND
        NOT EXISTS (
          SELECT * FROM Games
          WHERE
            /* %JoinFKPK(Games,Users," = "," AND") */
            Games.Id_player_two = Users.IdUsers
        )
    )
    BEGIN
      SELECT @errno  = 30010,
             @errmsg = 'Cannot delete last Games because Users exists.'
      GOTO error
    END


    /* erwin Builtin Trigger */
    RETURN
error:
   RAISERROR (@errmsg, -- Message text.
              @severity, -- Severity (0~25).
              @state) -- State (0~255).
    rollback transaction
END

go


CREATE TRIGGER tU_Games ON Games FOR UPDATE AS
/* erwin Builtin Trigger */
/* UPDATE trigger on Games */
BEGIN
  DECLARE  @numrows int,
           @nullcnt int,
           @validcnt int,
           @insIdGames Id,
           @errno   int,
           @severity int,
           @state    int,
           @errmsg  varchar(255)

  SELECT @numrows = @@rowcount
  /* erwin Builtin Trigger */
  /* Users  Games on child update no action */
  /* ERWIN_RELATION:CHECKSUM="00056973", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_6", FK_COLUMNS="Id_player_one" */
  IF
    /* %ChildFK(" OR",UPDATE) */
    UPDATE(Id_player_one)
  BEGIN
    SELECT @nullcnt = 0
    SELECT @validcnt = count(*)
      FROM inserted,Users
        WHERE
          /* %JoinFKPK(inserted,Users) */
          inserted.Id_player_one = Users.IdUsers
    /* %NotnullFK(inserted," IS NULL","select @nullcnt = count(*) from inserted where"," AND") */
    
    IF @validcnt + @nullcnt != @numrows
    BEGIN
      SELECT @errno  = 30007,
             @errmsg = 'Cannot update Games because Users does not exist.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on child update no action */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_5", FK_COLUMNS="Id_player_four" */
  IF
    /* %ChildFK(" OR",UPDATE) */
    UPDATE(Id_player_four)
  BEGIN
    SELECT @nullcnt = 0
    SELECT @validcnt = count(*)
      FROM inserted,Users
        WHERE
          /* %JoinFKPK(inserted,Users) */
          inserted.Id_player_four = Users.IdUsers
    /* %NotnullFK(inserted," IS NULL","select @nullcnt = count(*) from inserted where"," AND") */
    select @nullcnt = count(*) from inserted where
      inserted.Id_player_four IS NULL
    IF @validcnt + @nullcnt != @numrows
    BEGIN
      SELECT @errno  = 30007,
             @errmsg = 'Cannot update Games because Users does not exist.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on child update no action */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_4", FK_COLUMNS="Id_player_three" */
  IF
    /* %ChildFK(" OR",UPDATE) */
    UPDATE(Id_player_three)
  BEGIN
    SELECT @nullcnt = 0
    SELECT @validcnt = count(*)
      FROM inserted,Users
        WHERE
          /* %JoinFKPK(inserted,Users) */
          inserted.Id_player_three = Users.IdUsers
    /* %NotnullFK(inserted," IS NULL","select @nullcnt = count(*) from inserted where"," AND") */
    select @nullcnt = count(*) from inserted where
      inserted.Id_player_three IS NULL
    IF @validcnt + @nullcnt != @numrows
    BEGIN
      SELECT @errno  = 30007,
             @errmsg = 'Cannot update Games because Users does not exist.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on child update no action */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_3", FK_COLUMNS="Id_player_two" */
  IF
    /* %ChildFK(" OR",UPDATE) */
    UPDATE(Id_player_two)
  BEGIN
    SELECT @nullcnt = 0
    SELECT @validcnt = count(*)
      FROM inserted,Users
        WHERE
          /* %JoinFKPK(inserted,Users) */
          inserted.Id_player_two = Users.IdUsers
    /* %NotnullFK(inserted," IS NULL","select @nullcnt = count(*) from inserted where"," AND") */
    
    IF @validcnt + @nullcnt != @numrows
    BEGIN
      SELECT @errno  = 30007,
             @errmsg = 'Cannot update Games because Users does not exist.'
      GOTO error
    END
  END


  /* erwin Builtin Trigger */
  RETURN
error:
   RAISERROR (@errmsg, -- Message text.
              @severity, -- Severity (0~25).
              @state) -- State (0~255).
    rollback transaction
END

go




CREATE TRIGGER tD_Users ON Users FOR DELETE AS
/* erwin Builtin Trigger */
/* DELETE trigger on Users */
BEGIN
  DECLARE  @errno   int,
           @severity int,
           @state    int,
           @errmsg  varchar(255)
    /* erwin Builtin Trigger */
    /* Users  Friendships on parent delete cascade */
    /* ERWIN_RELATION:CHECKSUM="0004fbbd", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_8", FK_COLUMNS="Id_second" */
    DELETE Friendships
      FROM Friendships,deleted
      WHERE
        /*  %JoinFKPK(Friendships,deleted," = "," AND") */
        Friendships.Id_second = deleted.IdUsers

    /* erwin Builtin Trigger */
    /* Users  Friendships on parent delete cascade */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_7", FK_COLUMNS="Id_first" */
    DELETE Friendships
      FROM Friendships,deleted
      WHERE
        /*  %JoinFKPK(Friendships,deleted," = "," AND") */
        Friendships.Id_first = deleted.IdUsers

    /* erwin Builtin Trigger */
    /* Users  Games on parent delete restrict */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_6", FK_COLUMNS="Id_player_one" */
    IF EXISTS (
      SELECT * FROM deleted,Games
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_one = deleted.IdUsers
    )
    BEGIN
      SELECT @errno  = 30001,
             @errmsg = 'Cannot delete Users because Games exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Games on parent delete restrict */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_5", FK_COLUMNS="Id_player_four" */
    IF EXISTS (
      SELECT * FROM deleted,Games
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_four = deleted.IdUsers
    )
    BEGIN
      SELECT @errno  = 30001,
             @errmsg = 'Cannot delete Users because Games exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Games on parent delete restrict */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_4", FK_COLUMNS="Id_player_three" */
    IF EXISTS (
      SELECT * FROM deleted,Games
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_three = deleted.IdUsers
    )
    BEGIN
      SELECT @errno  = 30001,
             @errmsg = 'Cannot delete Users because Games exists.'
      GOTO error
    END

    /* erwin Builtin Trigger */
    /* Users  Games on parent delete restrict */
    /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_3", FK_COLUMNS="Id_player_two" */
    IF EXISTS (
      SELECT * FROM deleted,Games
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_two = deleted.IdUsers
    )
    BEGIN
      SELECT @errno  = 30001,
             @errmsg = 'Cannot delete Users because Games exists.'
      GOTO error
    END


    /* erwin Builtin Trigger */
    RETURN
error:
   RAISERROR (@errmsg, -- Message text.
              @severity, -- Severity (0~25).
              @state) -- State (0~255).
    rollback transaction
END

go


CREATE TRIGGER tU_Users ON Users FOR UPDATE AS
/* erwin Builtin Trigger */
/* UPDATE trigger on Users */
BEGIN
  DECLARE  @numrows int,
           @nullcnt int,
           @validcnt int,
           @insIdUsers Id,
           @errno   int,
           @severity int,
           @state    int,
           @errmsg  varchar(255)

  SELECT @numrows = @@rowcount
  /* erwin Builtin Trigger */
  /* Users  Friendships on parent update cascade */
  /* ERWIN_RELATION:CHECKSUM="00080dbe", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_8", FK_COLUMNS="Id_second" */
  IF
    /* %ParentPK(" OR",UPDATE) */
    UPDATE(IdUsers)
  BEGIN
    IF @numrows = 1
    BEGIN
      SELECT @insIdUsers = inserted.IdUsers
        FROM inserted
      UPDATE Friendships
      SET
        /*  %JoinFKPK(Friendships,@ins," = ",",") */
        Friendships.Id_second = @insIdUsers
      FROM Friendships,inserted,deleted
      WHERE
        /*  %JoinFKPK(Friendships,deleted," = "," AND") */
        Friendships.Id_second = deleted.IdUsers
    END
    ELSE
    BEGIN
      SELECT @errno = 30006,
             @errmsg = 'Cannot cascade Users update because more than one row has been affected.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Friendships on parent update cascade */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Friendships"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_7", FK_COLUMNS="Id_first" */
  IF
    /* %ParentPK(" OR",UPDATE) */
    UPDATE(IdUsers)
  BEGIN
    IF @numrows = 1
    BEGIN
      SELECT @insIdUsers = inserted.IdUsers
        FROM inserted
      UPDATE Friendships
      SET
        /*  %JoinFKPK(Friendships,@ins," = ",",") */
        Friendships.Id_first = @insIdUsers
      FROM Friendships,inserted,deleted
      WHERE
        /*  %JoinFKPK(Friendships,deleted," = "," AND") */
        Friendships.Id_first = deleted.IdUsers
    END
    ELSE
    BEGIN
      SELECT @errno = 30006,
             @errmsg = 'Cannot cascade Users update because more than one row has been affected.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on parent update cascade */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_6", FK_COLUMNS="Id_player_one" */
  IF
    /* %ParentPK(" OR",UPDATE) */
    UPDATE(IdUsers)
  BEGIN
    IF @numrows = 1
    BEGIN
      SELECT @insIdUsers = inserted.IdUsers
        FROM inserted
      UPDATE Games
      SET
        /*  %JoinFKPK(Games,@ins," = ",",") */
        Games.Id_player_one = @insIdUsers
      FROM Games,inserted,deleted
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_one = deleted.IdUsers
    END
    ELSE
    BEGIN
      SELECT @errno = 30006,
             @errmsg = 'Cannot cascade Users update because more than one row has been affected.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on parent update cascade */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_5", FK_COLUMNS="Id_player_four" */
  IF
    /* %ParentPK(" OR",UPDATE) */
    UPDATE(IdUsers)
  BEGIN
    IF @numrows = 1
    BEGIN
      SELECT @insIdUsers = inserted.IdUsers
        FROM inserted
      UPDATE Games
      SET
        /*  %JoinFKPK(Games,@ins," = ",",") */
        Games.Id_player_four = @insIdUsers
      FROM Games,inserted,deleted
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_four = deleted.IdUsers
    END
    ELSE
    BEGIN
      SELECT @errno = 30006,
             @errmsg = 'Cannot cascade Users update because more than one row has been affected.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on parent update cascade */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_4", FK_COLUMNS="Id_player_three" */
  IF
    /* %ParentPK(" OR",UPDATE) */
    UPDATE(IdUsers)
  BEGIN
    IF @numrows = 1
    BEGIN
      SELECT @insIdUsers = inserted.IdUsers
        FROM inserted
      UPDATE Games
      SET
        /*  %JoinFKPK(Games,@ins," = ",",") */
        Games.Id_player_three = @insIdUsers
      FROM Games,inserted,deleted
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_three = deleted.IdUsers
    END
    ELSE
    BEGIN
      SELECT @errno = 30006,
             @errmsg = 'Cannot cascade Users update because more than one row has been affected.'
      GOTO error
    END
  END

  /* erwin Builtin Trigger */
  /* Users  Games on parent update cascade */
  /* ERWIN_RELATION:CHECKSUM="00000000", PARENT_OWNER="", PARENT_TABLE="Users"
    CHILD_OWNER="", CHILD_TABLE="Games"
    P2C_VERB_PHRASE="", C2P_VERB_PHRASE="", 
    FK_CONSTRAINT="R_3", FK_COLUMNS="Id_player_two" */
  IF
    /* %ParentPK(" OR",UPDATE) */
    UPDATE(IdUsers)
  BEGIN
    IF @numrows = 1
    BEGIN
      SELECT @insIdUsers = inserted.IdUsers
        FROM inserted
      UPDATE Games
      SET
        /*  %JoinFKPK(Games,@ins," = ",",") */
        Games.Id_player_two = @insIdUsers
      FROM Games,inserted,deleted
      WHERE
        /*  %JoinFKPK(Games,deleted," = "," AND") */
        Games.Id_player_two = deleted.IdUsers
    END
    ELSE
    BEGIN
      SELECT @errno = 30006,
             @errmsg = 'Cannot cascade Users update because more than one row has been affected.'
      GOTO error
    END
  END


  /* erwin Builtin Trigger */
  RETURN
error:
   RAISERROR (@errmsg, -- Message text.
              @severity, -- Severity (0~25).
              @state) -- State (0~255).
    rollback transaction
END

go


