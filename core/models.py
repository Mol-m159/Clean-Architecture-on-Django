from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    registration_date = models.DateTimeField()
    last_activity_date = models.DateTimeField()

    class Meta:
        db_table = 'users'
        managed = False  

class GameSystems(models.Model):
    system_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        db_table = 'game_systems'
        managed = False

class Characters(models.Model):
    character_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='user_id')
    system = models.ForeignKey(GameSystems, on_delete=models.DO_NOTHING, db_column='system_id')
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        db_table = 'characters'
        managed = False

class CharacterEdits(models.Model):
    edit_id = models.AutoField(primary_key=True)
    character = models.ForeignKey(Characters, on_delete=models.DO_NOTHING, db_column='character_id')
    edit_date = models.DateTimeField()
    edit_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'character_edits'
        managed = False

class HomebrewEntities(models.Model):
    entity_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='author_id')
    system = models.ForeignKey(GameSystems, on_delete=models.DO_NOTHING, db_column='system_id')
    entity_type = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'homebrew_entities'
        managed = False

class HomebrewEdits(models.Model):
    edit_id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(HomebrewEntities, on_delete=models.DO_NOTHING, db_column='entity_id')
    edit_date = models.DateTimeField()
    version_number = models.IntegerField()

    class Meta:
        db_table = 'homebrew_edits'
        managed = False

class HomebrewModerations(models.Model):
    moderation_id = models.AutoField(primary_key=True)
    moderator = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='moderator_id')
    entity = models.ForeignKey(HomebrewEntities, on_delete=models.DO_NOTHING, db_column='entity_id')
    moderation_date = models.DateTimeField()
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)

    class Meta:
        db_table = 'homebrew_moderations'
        managed = False

class EntityViews(models.Model):
    view_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='user_id')
    entity = models.ForeignKey(HomebrewEntities, on_delete=models.DO_NOTHING, db_column='entity_id')
    view_date = models.DateTimeField()

    class Meta:
        db_table = 'entity_views'
        managed = False

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='user_id')
    created_date = models.DateTimeField()
    notification_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'notifications'
        managed = False

class NotificationEvents(models.Model):
    event_id = models.AutoField(primary_key=True)
    notification = models.ForeignKey(Notifications, on_delete=models.DO_NOTHING, db_column='notification_id')
    event_date = models.DateTimeField()
    event_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'notification_events'
        managed = False

class UserSessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='user_id')
    login_date = models.DateTimeField()
    logout_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_sessions'
        managed = False

class SystemEvents(models.Model):
    event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column='user_id', null=True, blank=True)
    system = models.ForeignKey(GameSystems, on_delete=models.DO_NOTHING, db_column='system_id', null=True, blank=True)
    event_date = models.DateTimeField()
    event_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'system_events'
        managed = False