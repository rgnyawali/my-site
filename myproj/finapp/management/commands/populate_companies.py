from django.core.management.base import BaseCommand
from finapp.models import Company

class Command(BaseCommand):
    help = 'Populate the Company model with initial data'

    def handle(self, *args, **options):
        companies_data = [
            ('TXG', '10x Genomics, Inc.'),
            ('ATNF', '180 Life Sciences Corp.'),
            ('BCOW','1895 Bancorp of Wisconsin, Inc.'),
            ('SRCE','1st Source Corporation'),
            ('DIBS','1stdibs.Com, Inc.'),
            ('XXII','22nd Century Group, Inc.'),
            ('ME','23andMe Holding Co.'),
            ('TSVT','2seventy bio, Inc.'),
            ('TWOU','2U, Inc.'),
            ('DDD','3D Systems Corporation'),
            ('MMM','3M Company'),
            ('FDMT','4D Molecular Therapeutics, Inc.'),
            ('FEAM','5E Advanced Materials Inc.'),
            ('ETNB','89bio, Inc.'),
            ('EGHT','8x8, Inc.'),
            ('MASS','908 Devices Inc.'),
            ('AOS','A. O. Smith Corporation'),
            ('AKA','a.k.a. Brands Holding Corp.'),
            ('ATEN','A10 Networks, Inc.'),
            ('AADI','Aadi Bioscience, Inc.')
            # Add more companies if needed
        ]

        for ticker, name in companies_data:
            Company.objects.create(name=name, ticker=ticker)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Company model.'))
