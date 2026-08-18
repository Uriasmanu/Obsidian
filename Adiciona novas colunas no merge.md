
Roda em Figueira

USE sigmaecm_copel_figueira;
GO
SELECT c.name AS coluna, ty.name AS tipo, c.is_identity, c.is_rowguidcol
FROM   sys.columns c
JOIN   sys.types ty ON ty.user_type_id = c.user_type_id
WHERE  c.object_id = OBJECT_ID(N'dbo.ConfiguracaoAlarme')
  AND  (c.is_identity = 1 OR ty.name = 'uniqueidentifier')
ORDER  BY c.column_id;


Vamos alterar a coluna Id para rowguid

USE sigmaecm_copel_figueira;
GO
ALTER TABLE dbo.ConfiguracaoAlarme ALTER COLUMN Id ADD ROWGUIDCOL;
GO


rodar na central  

USE sigmaecm;
GO
ALTER TABLE dbo.ConfiguracaoAlarme ALTER COLUMN Id ADD ROWGUIDCOL;
GO


Pois ambas tem que estar igual


Agora vamos adicionar a nova tabela ao processo


USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergearticle
     @publication               = N'Pub_sigmaecm',
     @article                   = N'ConfiguracaoAlarme',
     @source_owner              = N'dbo',
     @source_object             = N'ConfiguracaoAlarme',
     @type                      = N'table',
     @column_tracking           = N'true',
     @force_invalidate_snapshot = 1,
     @force_reinit_subscription = 1;
GO


USE sigmaecm_copel_figueira;
GO
EXEC sp_helpmergesubscription @publication = N'Pub_sigmaecm';
GO



USE sigmaecm_copel_figueira;
GO
EXEC sp_helpmergearticle @publication = N'Pub_sigmaecm';
GO



USE sigmaecm;
GO
SELECT OBJECT_NAME(fk.parent_object_id) AS tabela_que_referencia
FROM   sys.foreign_keys fk
WHERE  OBJECT_NAME(fk.referenced_object_id) = N'ConfiguracaoAlarme';
GO