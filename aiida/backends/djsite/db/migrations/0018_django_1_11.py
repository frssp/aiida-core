# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
# Generated by Django 1.11.16 on 2018-11-12 16:46
# pylint: disable=invalid-name
"""Migration for upgrade to django 1.11"""

# Remove when https://github.com/PyCQA/pylint/issues/1931 is fixed
# pylint: disable=no-name-in-module,import-error
from django.db import migrations, models
import aiida.common.utils
from aiida.backends.djsite.db.migrations import upgrade_schema_version

REVISION = '1.0.18'
DOWN_REVISION = '1.0.17'

tables = ['db_dbcomment', 'db_dbcomputer', 'db_dbgroup', 'db_dbworkflow']


def _verify_uuid_uniqueness(apps, schema_editor):
    """Check whether the respective tables contain rows with duplicate UUIDS.

    Note that we have to redefine this method from aiida.manage.database.integrity
    because the migrations.RunPython command that will invoke this function, will pass two arguments and therefore
    this wrapper needs to have a different function signature.

    :raises: IntegrityError if database contains rows with duplicate UUIDS.
    """
    # pylint: disable=unused-argument
    from aiida.backends.general.migrations.duplicate_uuids import verify_uuid_uniqueness

    for table in tables:
        verify_uuid_uniqueness(table=table)


def reverse_code(apps, schema_editor):
    # pylint: disable=unused-argument
    pass


class Migration(migrations.Migration):
    """Migration for upgrade to django 1.11

    This migration switches from the django_extensions UUID field to the
    native UUIDField of django 1.11

    It also introduces unique constraints on all uuid columns
    (previously existed only on dbnode).
    """

    dependencies = [
        ('db', '0017_drop_dbcalcstate'),
    ]

    operations = [
        migrations.RunPython(_verify_uuid_uniqueness, reverse_code=reverse_code),
        migrations.AlterField(
            model_name='dbcomment',
            name='uuid',
            field=models.UUIDField(unique=True, default=aiida.common.utils.get_new_uuid),
        ),
        migrations.AlterField(
            model_name='dbcomputer',
            name='uuid',
            field=models.UUIDField(unique=True, default=aiida.common.utils.get_new_uuid),
        ),
        migrations.AlterField(
            model_name='dbgroup',
            name='uuid',
            field=models.UUIDField(unique=True, default=aiida.common.utils.get_new_uuid),
        ),
        # first: remove index
        migrations.AlterField(
            model_name='dbnode',
            name='uuid',
            field=models.CharField(max_length=36, default=aiida.common.utils.get_new_uuid, unique=False),
        ),
        # second: switch to UUIDField
        migrations.AlterField(
            model_name='dbnode',
            name='uuid',
            field=models.UUIDField(default=aiida.common.utils.get_new_uuid, unique=True),
        ),
        migrations.AlterField(
            model_name='dbuser',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='dbuser',
            name='groups',
            field=models.ManyToManyField(
                blank=True,
                help_text=
                'The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                related_name='user_set',
                related_query_name='user',
                to='auth.Group',
                verbose_name='groups'
            ),
        ),
        migrations.AlterField(
            model_name='dbworkflow',
            name='uuid',
            field=models.UUIDField(unique=True, default=aiida.common.utils.get_new_uuid),
        ),
        upgrade_schema_version(REVISION, DOWN_REVISION)
    ]
