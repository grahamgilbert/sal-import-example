from django.core.management.base import BaseCommand, CommandError
from server.models import *
import os
import csv

class Command(BaseCommand):
    args = '<path/to/csv>'
    help = 'Creates Business Units and Machine Groups from a CSV'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('More than one argument passed')
        for path in args:
            if os.path.exists(path):
                with open(path, 'rb') as csvfile:
                    csv_data = csv.DictReader(csvfile, delimiter=',')
                    for row in csv_data:
                        BusinessUnitName = row['BusinessUnit']
                        MachineGroupName = row['MachineGroup']

                        # Get the BU. If it doesn't exist, create it
                        try:
                            bu = BusinessUnit.objects.get(name=BusinessUnitName) 
                            self.stdout.write('%s already exists.' % BusinessUnitName)
                        except BusinessUnit.DoesNotExist:
                            bu = BusinessUnit(name=BusinessUnitName) 
                            bu.save()
                            self.stdout.write('%s didn\'t exist and has been created.' % BusinessUnitName)
                        except BusinessUnit.MultipleObjectsReturned:     
                            raise CommandError('For this import to work, we must be able to identify Business'
                                ' Units uniquely by name')

                        # Now we're going to get the Machine Group
                        try:
                            group = MachineGroup.objects.get(name=MachineGroupName, business_unit=bu) 
                            self.stdout.write('%s already exists.' % MachineGroupName)
                        except MachineGroup.DoesNotExist:
                            group = MachineGroup(name=MachineGroupName, business_unit=bu) 
                            group.save()
                            self.stdout.write('%s didn\'t exist and has been created.' % MachineGroupName)
                        except MachineGroup.MultipleObjectsReturned:     
                            raise CommandError('For this import to work, we must be able to identify Machine'
                                ' Groups uniquely by name and Business Unit pair.')
            else:
                raise CommandError('CSV "%s" does not exist' % path)