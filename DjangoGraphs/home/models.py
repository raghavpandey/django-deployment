from django.db import models


class SocTable(models.Model):
    soc_id = models.IntegerField()
    soc_name = models.CharField(max_length=150)
    soc_addr = models.CharField(max_length=300)
    work_area = models.CharField(max_length=150)
    dist_id = models.IntegerField()
    dist_name = models.CharField(max_length=200)
    division_name = models.CharField(max_length=150, blank=True, null=True)
    stype_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=200)
    reg_date = models.DateTimeField()
    ren_date = models.DateTimeField()
    #app_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'soc_table'


class LogTable(models.Model):
    user_id = models.IntegerField(db_column='User_id', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_name', max_length=150)  # Field name made lowercase.
    module_name = models.CharField(db_column='Module_name', max_length=100)  # Field name made lowercase.
    time_login = models.DateTimeField(db_column='Time_login')  # Field name made lowercase.
    logout_time = models.DateTimeField(db_column='LogOut_time', blank=True, null=True)  # Field name made lowercase.
    is_success = models.IntegerField(db_column='Is_success')  # Field name made lowercase.
    trk_ip_address = models.CharField(db_column='Trk_Ip_address', max_length=50)  # Field name made lowercase.
    action_date = models.DateTimeField(db_column='Action_date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'log_table'


class Reviews(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    user_name = models.CharField(db_column='User_name', max_length=200)
    age = models.IntegerField(db_column='age')
    comments = models.CharField(db_column='comments', max_length=500)
    rate = models.IntegerField(db_column='rate',)

    class Meta:
        managed = False
        db_table = 'reviews'


class SocMaster(models.Model):
    soc_id = models.IntegerField()
    soc_name = models.CharField(max_length=200)
    soc_addr = models.CharField(max_length=200)
    work_area = models.CharField(max_length=150)
    dist_id = models.IntegerField()
    dist_name = models.CharField(max_length=150)
    division_name = models.CharField(max_length=200)
    stype_name = models.CharField(max_length=150)
    reg_no = models.CharField(max_length=150)
    reg_date = models.DateField()
    ren_date = models.DateField()
    app_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'soc_master'
