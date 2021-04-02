# Generated by Django 3.1.6 on 2021-04-02 13:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pgcrypto.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('business_code', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('attributes', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='IqpRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_uid', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=255)),
                ('dossier_id', models.CharField(max_length=255)),
                ('process_id', models.CharField(max_length=255)),
                ('verify_request_uid', models.CharField(max_length=255, null=True)),
                ('presentation_id', models.CharField(default='N/A', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('business_code', models.CharField(max_length=255, null=True)),
                ('ip_address', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProofRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_code', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_uid', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('request_type', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.organization')),
                ('parent_request', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.request')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_id', models.CharField(max_length=255)),
                ('connection_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.organization')),
            ],
            options={
                'unique_together': {('connection_id', 'organization')},
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('source', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255, null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.request')),
                ('user_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.userconnection')),
            ],
        ),
        migrations.CreateModel(
            name='WebIdRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_uid', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('request_type', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('dossier_id', models.CharField(max_length=255)),
                ('verify_request_uid', models.CharField(max_length=255, null=True)),
                ('presentation_id', models.CharField(default='N/A', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectionRequest',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generic_organization_service.request')),
                ('allow_multiple_read', models.BooleanField(default=False)),
            ],
            bases=('generic_organization_service.request',),
        ),
        migrations.CreateModel(
            name='WebIdDossier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dossier_id', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('data', models.TextField()),
                ('reason', models.CharField(max_length=255, null=True)),
                ('token_link', models.CharField(max_length=255, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update_date', models.DateTimeField(blank=True)),
                ('user_connection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.userconnection')),
                ('webid_request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.webidrequest')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='user_connection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.userconnection'),
        ),
        migrations.CreateModel(
            name='ProofServiceAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.action')),
                ('proof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.proofrequest')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.service')),
            ],
            options={
                'unique_together': {('proof', 'service')},
            },
        ),
        migrations.CreateModel(
            name='IssuedCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.CharField(max_length=255)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('revoked_date', models.DateTimeField(blank=True, null=True)),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.credential')),
                ('request_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.request')),
                ('user_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.userconnection')),
            ],
        ),
        migrations.CreateModel(
            name='IqpDossier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dossier_id', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('data', models.TextField()),
                ('reason', models.CharField(max_length=255, null=True)),
                ('awaited_owner_confirmation', models.IntegerField(default=0, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update_date', models.DateTimeField(blank=True)),
                ('iqp_request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.iqprequest')),
                ('user_connection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.userconnection')),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('ip_address', models.CharField(max_length=255, null=True)),
                ('auth', models.JSONField(null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.organization')),
            ],
        ),
        migrations.CreateModel(
            name='WebIdUserData',
            fields=[
                ('userdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generic_organization_service.userdata')),
                ('webid_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.webidrequest')),
            ],
            bases=('generic_organization_service.userdata',),
        ),
        migrations.CreateModel(
            name='VerifyRequest',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generic_organization_service.request')),
                ('allow_multiple_read', models.BooleanField(default=False)),
                ('restrictions', models.TextField(null=True)),
                ('proof_service_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.proofserviceaction')),
            ],
            bases=('generic_organization_service.request',),
        ),
        migrations.CreateModel(
            name='VerifyConfirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirm_date', models.DateTimeField(null=True)),
                ('proof_evidence', pgcrypto.fields.EncryptedTextField(charset='utf-8', check_armor=True, cipher='aes', versioned=False)),
                ('proof_request', models.JSONField(null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('user_connection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='generic_organization_service.userconnection')),
                ('verify_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.verifyrequest')),
            ],
        ),
        migrations.CreateModel(
            name='ProofServiceActionCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.credential')),
                ('proof_service_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.proofserviceaction')),
            ],
            options={
                'unique_together': {('proof_service_action', 'credential')},
            },
        ),
        migrations.CreateModel(
            name='IssueRequest',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generic_organization_service.request')),
                ('values_for_credential', models.JSONField(null=True)),
                ('discard_description', models.TextField(null=True)),
                ('issued_by_operator', models.BooleanField(default=False)),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.credential')),
            ],
            bases=('generic_organization_service.request',),
        ),
        migrations.CreateModel(
            name='IqpUserData',
            fields=[
                ('userdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generic_organization_service.userdata')),
                ('iqp_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.iqprequest')),
            ],
            bases=('generic_organization_service.userdata',),
        ),
        migrations.CreateModel(
            name='ConnectionAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('user_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generic_organization_service.userconnection')),
            ],
            options={
                'unique_together': {('name', 'value', 'user_connection')},
            },
        ),
    ]
