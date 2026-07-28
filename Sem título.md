-----------------BEGIN: Script to be run at Publisher 'SRV-JD-FIGUEIRA'-----------------

use [ecm_copel_jdfigueira] exec sp_addsubscription @publication = N'PublicacaoClienteJdFigueira',

@subscriber = N 'DISMONTFLIC\MSSQLSERVERTT',

@destination_db = N'ecm_copel_jdfigueira',

@sync_type = N'Automatic',

@subscription_type = N'pull',

@update_mode = N'read only'

GO

    -----------------END: Script to be run at Publisher 'SRV-JD-FIGUEIRA'-----------------

    -----------------BEGIN: Script to be run at Subscriber 'DISMONTFLIC\MSSQLSERVERTT'-----------------

    use [ecm_copel_jdfigueira] exec sp_addpullsubscription @publisher = N'SRV-JD-FIGUEIRA',

    @publication = N'PublicacaoClienteJdFigueira',

    @publisher_db = N'ecm_copel_jdfigueira',

    @independent_agent = N'True',

    @subscription_type = N'pull',

    @description = N'',

    @update_mode = N'read only',

    @immediate_sync = 1 exec sp_addpullsubscription_agent @publisher = N'SRV-JD-FIGUEIRA',

    @publisher_db = N'ecm_copel_jdfigueira',

    @publication = N'PublicacaoClienteJdFigueira',

    @distributor = N'SRV-JD-FIGUEIRA',

    @distributor_security_mode = 0,

    @distributor_login = N'app.ecm',

    @distributor_password = null,  🔑 SUBSTITUA null POR N'SENHA_DO_APP_ECM_AQUI'

    @enabled_for_syncmgr = N'False',

    @frequency_type = 64,

    @frequency_interval = 0,

    @frequency_relative_interval = 0,

    @frequency_recurrence_factor = 0,

    @frequency_subday = 0,

    @frequency_subday_interval = 0,

    @active_start_time_of_day = 0,

    @active_end_time_of_day = 235959,

    @active_start_date = 20260629,

    @active_end_date = 99991231,

    @alt_snapshot_folder = N'',

    @working_directory = N'',  🔑 SUBSTITUA N'' POR N'\\SRV-JD-FIGUEIRA\repldata' (CRIE A PASTA E COMPARTILHE)

    @use_ftp = N'False',

    @job_login = null,  🔑 SUBSTITUA null POR N'NT SERVICE\SQLSERVERAGENT'

    @job_password = null,  ✅ MANTENHA null (quando usa conta de serviço, a senha é gerenciada pelo sistema)

    @publication_type = 0

GO

    -----------------END: Script to be run at Subscriber 'DISMONTFLIC\MSSQLSERVERTT'-----------------