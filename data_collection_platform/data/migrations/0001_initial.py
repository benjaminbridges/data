# Generated by Django 4.0 on 2022-04-08 15:58

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
                ('category_description', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_name', models.CharField(max_length=200, unique=True)),
                ('entity_email_primary', models.EmailField(blank=True, max_length=200, null=True)),
                ('entity_website', models.URLField(blank=True, null=True)),
                ('entity_postcode', models.CharField(blank=True, max_length=200, null=True)),
                ('entity_address', models.CharField(blank=True, max_length=200, null=True)),
                ('entity_city_town', models.CharField(blank=True, max_length=200, null=True)),
                ('entity_created', models.DateField(auto_now_add=True)),
                ('entity_last_edited', models.DateField(auto_now=True)),
                ('entity_status', models.BooleanField(default=True, verbose_name='Is this Entity active?')),
                ('entity_year_founded', models.IntegerField(blank=True, choices=[(1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030)], null=True)),
            ],
            options={
                'verbose_name_plural': 'Entities',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=200, unique=True)),
                ('group_description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=200, unique=True)),
                ('org_description', models.CharField(max_length=200)),
                ('org_color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None)),
                ('org_logo', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('site_permission', models.CharField(choices=[('user', 'user'), ('centalteam', 'centalteam'), ('entity', 'entity'), ('org', 'org'), ('sa', 'sa')], default='user', max_length=30, null=True)),
                ('profile_pic', models.ImageField(null=True, upload_to='')),
                ('entity', models.ManyToManyField(blank=True, to='data.Entity')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.CharField(max_length=200, verbose_name='Survey Name')),
                ('survey_entity_to_set_times', models.BooleanField(default=False, verbose_name='Allow Entity to set dates, interval and occurances')),
                ('survey_interval', models.CharField(choices=[('Daily', 'Daily'), ('Daily weekdays', 'Daily weekdays'), ('Weekly', 'Weekly'), ('Fortnightly', 'Fortnightly'), ('Monthly', 'Monthly'), ('Last day of the month', 'Last day of the month'), ('First working day monthly', 'First working day monthly'), ('Annually', 'Annually'), ('Previous year', 'Previous year')], default='weekly', help_text='how regularily should this survey take place', max_length=30, null=True, verbose_name='Interval')),
                ('survey_time', models.TimeField(help_text='at what time should this survey take place', null=True, verbose_name='Time')),
                ('survey_occurances', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(365), django.core.validators.MinValueValidator(1)], verbose_name='Occurances')),
                ('survey_start_date', models.DateField(null=True, verbose_name='Start Date')),
                ('survey_breakdown_allowed', models.BooleanField(default=True, verbose_name='Allow Entity to segment this survey')),
                ('survey_active', models.BooleanField(default=True, verbose_name='Survey Active')),
                ('survey_created_by', models.CharField(max_length=200, verbose_name='Created by')),
                ('category', models.ForeignKey(help_text='Please select the monst relevant category', on_delete=django.db.models.deletion.CASCADE, to='data.category')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyBreakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surveybreakdown_name', models.CharField(max_length=200)),
                ('surveybreakdown_time', models.TimeField(help_text='at what time should this survey take place', null=True)),
                ('surveybreakdown_active', models.BooleanField(default=True, verbose_name='Breakdown Active')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_date', models.DateField(null=True)),
                ('survey_start_date', models.DateField(null=True)),
                ('survey_end_date', models.DateField(null=True)),
                ('survey_time', models.TimeField(null=True)),
                ('survey_instance_complete', models.BooleanField(default=False)),
                ('surveyinstance_active', models.BooleanField(default=True, verbose_name='Instance Active')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.profile')),
                ('surveybreakdown', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveybreakdown')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_interval', models.CharField(choices=[('Daily', 'Daily'), ('Daily weekdays', 'Daily weekdays'), ('Weekly', 'Weekly'), ('Fortnightly', 'Fortnightly'), ('Monthly', 'Monthly'), ('Last day of the month', 'Last day of the month'), ('First working day monthly', 'First working day monthly'), ('Annually', 'Annually'), ('Previous year', 'Previous year')], default='weekly', help_text='how regularily should this survey take place', max_length=30, null=True)),
                ('survey_occurances', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(365), django.core.validators.MinValueValidator(1)])),
                ('survey_start_date', models.DateField(null=True)),
                ('survey_times_assigned', models.BooleanField(default=False)),
                ('surveyentity_active', models.BooleanField(default=True, verbose_name='Survey Entity Active')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.entity')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.survey')),
            ],
            options={
                'verbose_name_plural': 'Survey Entities',
            },
        ),
        migrations.CreateModel(
            name='SurveyBreakdownProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surveybreakdownprofile_active', models.BooleanField(default=True, verbose_name='Breakdown Profile Active')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.profile')),
                ('surveybreakdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.surveybreakdown')),
            ],
        ),
        migrations.AddField(
            model_name='surveybreakdown',
            name='profile',
            field=models.ManyToManyField(through='data.SurveyBreakdownProfile', to='data.Profile'),
        ),
        migrations.AddField(
            model_name='surveybreakdown',
            name='surveyentity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.surveyentity'),
        ),
        migrations.AddField(
            model_name='survey',
            name='entity',
            field=models.ManyToManyField(blank=True, help_text='You can select multiple entities by using the ctrl or shift key.', through='data.SurveyEntity', to='data.Entity', verbose_name='Select Entities'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_content', models.CharField(max_length=200)),
                ('question_type', models.CharField(choices=[('ShortText', 'ShortText'), ('LongText', 'LongText'), ('File', 'File'), ('Integer', 'Integer'), ('Float', 'Float'), ('Duration', 'Duration'), ('Date', 'Date')], default='text', max_length=20)),
                ('survey', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='data.survey')),
            ],
        ),
        migrations.CreateModel(
            name='EntityGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.entity')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.group')),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='group',
            field=models.ManyToManyField(through='data.EntityGroup', to='data.Group'),
        ),
        migrations.AddField(
            model_name='entity',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.organisation'),
        ),
        migrations.CreateModel(
            name='BreakdownCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=25)),
                ('category_description', models.CharField(max_length=200)),
                ('survey', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='data.survey')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerShortText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_short_text', models.CharField(max_length=140)),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerLongText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_long_text', models.TextField()),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerInteger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_integer', models.IntegerField(default=1)),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerFloat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_float', models.FloatField()),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_file', models.FileField(upload_to='')),
                ('answer_file_name', models.CharField(max_length=30)),
                ('answer_caption', models.CharField(max_length=140)),
                ('answer_description', models.TextField(null=True)),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerDuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_duration', models.DurationField()),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_date', models.DateField()),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_currency_currency', djmoney.models.fields.CurrencyField(choices=[('XUA', 'ADB Unit of Account'), ('AFN', 'Afghan Afghani'), ('AFA', 'Afghan Afghani (1927–2002)'), ('ALL', 'Albanian Lek'), ('ALK', 'Albanian Lek (1946–1965)'), ('DZD', 'Algerian Dinar'), ('ADP', 'Andorran Peseta'), ('AOA', 'Angolan Kwanza'), ('AOK', 'Angolan Kwanza (1977–1991)'), ('AON', 'Angolan New Kwanza (1990–2000)'), ('AOR', 'Angolan Readjusted Kwanza (1995–1999)'), ('ARA', 'Argentine Austral'), ('ARS', 'Argentine Peso'), ('ARM', 'Argentine Peso (1881–1970)'), ('ARP', 'Argentine Peso (1983–1985)'), ('ARL', 'Argentine Peso Ley (1970–1983)'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('ATS', 'Austrian Schilling'), ('AZN', 'Azerbaijani Manat'), ('AZM', 'Azerbaijani Manat (1993–2006)'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('BDT', 'Bangladeshi Taka'), ('BBD', 'Barbadian Dollar'), ('BYN', 'Belarusian Ruble'), ('BYB', 'Belarusian Ruble (1994–1999)'), ('BYR', 'Belarusian Ruble (2000–2016)'), ('BEF', 'Belgian Franc'), ('BEC', 'Belgian Franc (convertible)'), ('BEL', 'Belgian Franc (financial)'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudan Dollar'), ('BTN', 'Bhutanese Ngultrum'), ('BOB', 'Bolivian Boliviano'), ('BOL', 'Bolivian Boliviano (1863–1963)'), ('BOV', 'Bolivian Mvdol'), ('BOP', 'Bolivian Peso'), ('BAM', 'Bosnia-Herzegovina Convertible Mark'), ('BAD', 'Bosnia-Herzegovina Dinar (1992–1994)'), ('BAN', 'Bosnia-Herzegovina New Dinar (1994–1997)'), ('BWP', 'Botswanan Pula'), ('BRC', 'Brazilian Cruzado (1986–1989)'), ('BRZ', 'Brazilian Cruzeiro (1942–1967)'), ('BRE', 'Brazilian Cruzeiro (1990–1993)'), ('BRR', 'Brazilian Cruzeiro (1993–1994)'), ('BRN', 'Brazilian New Cruzado (1989–1990)'), ('BRB', 'Brazilian New Cruzeiro (1967–1986)'), ('BRL', 'Brazilian Real'), ('GBP', 'British Pound'), ('BND', 'Brunei Dollar'), ('BGL', 'Bulgarian Hard Lev'), ('BGN', 'Bulgarian Lev'), ('BGO', 'Bulgarian Lev (1879–1952)'), ('BGM', 'Bulgarian Socialist Lev'), ('BUK', 'Burmese Kyat'), ('BIF', 'Burundian Franc'), ('XPF', 'CFP Franc'), ('KHR', 'Cambodian Riel'), ('CAD', 'Canadian Dollar'), ('CVE', 'Cape Verdean Escudo'), ('KYD', 'Cayman Islands Dollar'), ('XAF', 'Central African CFA Franc'), ('CLE', 'Chilean Escudo'), ('CLP', 'Chilean Peso'), ('CLF', 'Chilean Unit of Account (UF)'), ('CNX', 'Chinese People’s Bank Dollar'), ('CNY', 'Chinese Yuan'), ('CNH', 'Chinese Yuan (offshore)'), ('COP', 'Colombian Peso'), ('COU', 'Colombian Real Value Unit'), ('KMF', 'Comorian Franc'), ('CDF', 'Congolese Franc'), ('CRC', 'Costa Rican Colón'), ('HRD', 'Croatian Dinar'), ('HRK', 'Croatian Kuna'), ('CUC', 'Cuban Convertible Peso'), ('CUP', 'Cuban Peso'), ('CYP', 'Cypriot Pound'), ('CZK', 'Czech Koruna'), ('CSK', 'Czechoslovak Hard Koruna'), ('DKK', 'Danish Krone'), ('DJF', 'Djiboutian Franc'), ('DOP', 'Dominican Peso'), ('NLG', 'Dutch Guilder'), ('XCD', 'East Caribbean Dollar'), ('DDM', 'East German Mark'), ('ECS', 'Ecuadorian Sucre'), ('ECV', 'Ecuadorian Unit of Constant Value'), ('EGP', 'Egyptian Pound'), ('GQE', 'Equatorial Guinean Ekwele'), ('ERN', 'Eritrean Nakfa'), ('EEK', 'Estonian Kroon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('XBA', 'European Composite Unit'), ('XEU', 'European Currency Unit'), ('XBB', 'European Monetary Unit'), ('XBC', 'European Unit of Account (XBC)'), ('XBD', 'European Unit of Account (XBD)'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fijian Dollar'), ('FIM', 'Finnish Markka'), ('FRF', 'French Franc'), ('XFO', 'French Gold Franc'), ('XFU', 'French UIC-Franc'), ('GMD', 'Gambian Dalasi'), ('GEK', 'Georgian Kupon Larit'), ('GEL', 'Georgian Lari'), ('DEM', 'German Mark'), ('GHS', 'Ghanaian Cedi'), ('GHC', 'Ghanaian Cedi (1979–2007)'), ('GIP', 'Gibraltar Pound'), ('XAU', 'Gold'), ('GRD', 'Greek Drachma'), ('GTQ', 'Guatemalan Quetzal'), ('GWP', 'Guinea-Bissau Peso'), ('GNF', 'Guinean Franc'), ('GNS', 'Guinean Syli'), ('GYD', 'Guyanaese Dollar'), ('HTG', 'Haitian Gourde'), ('HNL', 'Honduran Lempira'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Hungarian Forint'), ('IMP', 'IMP'), ('ISK', 'Icelandic Króna'), ('ISJ', 'Icelandic Króna (1918–1981)'), ('INR', 'Indian Rupee'), ('IDR', 'Indonesian Rupiah'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('IEP', 'Irish Pound'), ('ILS', 'Israeli New Shekel'), ('ILP', 'Israeli Pound'), ('ILR', 'Israeli Shekel (1980–1985)'), ('ITL', 'Italian Lira'), ('JMD', 'Jamaican Dollar'), ('JPY', 'Japanese Yen'), ('JOD', 'Jordanian Dinar'), ('KZT', 'Kazakhstani Tenge'), ('KES', 'Kenyan Shilling'), ('KWD', 'Kuwaiti Dinar'), ('KGS', 'Kyrgystani Som'), ('LAK', 'Laotian Kip'), ('LVL', 'Latvian Lats'), ('LVR', 'Latvian Ruble'), ('LBP', 'Lebanese Pound'), ('LSL', 'Lesotho Loti'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('LTL', 'Lithuanian Litas'), ('LTT', 'Lithuanian Talonas'), ('LUL', 'Luxembourg Financial Franc'), ('LUC', 'Luxembourgian Convertible Franc'), ('LUF', 'Luxembourgian Franc'), ('MOP', 'Macanese Pataca'), ('MKD', 'Macedonian Denar'), ('MKN', 'Macedonian Denar (1992–1993)'), ('MGA', 'Malagasy Ariary'), ('MGF', 'Malagasy Franc'), ('MWK', 'Malawian Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MVR', 'Maldivian Rufiyaa'), ('MVP', 'Maldivian Rupee (1947–1981)'), ('MLF', 'Malian Franc'), ('MTL', 'Maltese Lira'), ('MTP', 'Maltese Pound'), ('MRU', 'Mauritanian Ouguiya'), ('MRO', 'Mauritanian Ouguiya (1973–2017)'), ('MUR', 'Mauritian Rupee'), ('MXV', 'Mexican Investment Unit'), ('MXN', 'Mexican Peso'), ('MXP', 'Mexican Silver Peso (1861–1992)'), ('MDC', 'Moldovan Cupon'), ('MDL', 'Moldovan Leu'), ('MCF', 'Monegasque Franc'), ('MNT', 'Mongolian Tugrik'), ('MAD', 'Moroccan Dirham'), ('MAF', 'Moroccan Franc'), ('MZE', 'Mozambican Escudo'), ('MZN', 'Mozambican Metical'), ('MZM', 'Mozambican Metical (1980–2006)'), ('MMK', 'Myanmar Kyat'), ('NAD', 'Namibian Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillean Guilder'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('NIO', 'Nicaraguan Córdoba'), ('NIC', 'Nicaraguan Córdoba (1988–1991)'), ('NGN', 'Nigerian Naira'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('OMR', 'Omani Rial'), ('PKR', 'Pakistani Rupee'), ('XPD', 'Palladium'), ('PAB', 'Panamanian Balboa'), ('PGK', 'Papua New Guinean Kina'), ('PYG', 'Paraguayan Guarani'), ('PEI', 'Peruvian Inti'), ('PEN', 'Peruvian Sol'), ('PES', 'Peruvian Sol (1863–1965)'), ('PHP', 'Philippine Piso'), ('XPT', 'Platinum'), ('PLN', 'Polish Zloty'), ('PLZ', 'Polish Zloty (1950–1995)'), ('PTE', 'Portuguese Escudo'), ('GWE', 'Portuguese Guinea Escudo'), ('QAR', 'Qatari Rial'), ('XRE', 'RINET Funds'), ('RHD', 'Rhodesian Dollar'), ('RON', 'Romanian Leu'), ('ROL', 'Romanian Leu (1952–2006)'), ('RUB', 'Russian Ruble'), ('RUR', 'Russian Ruble (1991–1998)'), ('RWF', 'Rwandan Franc'), ('SVC', 'Salvadoran Colón'), ('WST', 'Samoan Tala'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('CSD', 'Serbian Dinar (2002–2006)'), ('SCR', 'Seychellois Rupee'), ('SLL', 'Sierra Leonean Leone'), ('XAG', 'Silver'), ('SGD', 'Singapore Dollar'), ('SKK', 'Slovak Koruna'), ('SIT', 'Slovenian Tolar'), ('SBD', 'Solomon Islands Dollar'), ('SOS', 'Somali Shilling'), ('ZAR', 'South African Rand'), ('ZAL', 'South African Rand (financial)'), ('KRH', 'South Korean Hwan (1953–1962)'), ('KRW', 'South Korean Won'), ('KRO', 'South Korean Won (1945–1953)'), ('SSP', 'South Sudanese Pound'), ('SUR', 'Soviet Rouble'), ('ESP', 'Spanish Peseta'), ('ESA', 'Spanish Peseta (A account)'), ('ESB', 'Spanish Peseta (convertible account)'), ('XDR', 'Special Drawing Rights'), ('LKR', 'Sri Lankan Rupee'), ('SHP', 'St. Helena Pound'), ('XSU', 'Sucre'), ('SDD', 'Sudanese Dinar (1992–2007)'), ('SDG', 'Sudanese Pound'), ('SDP', 'Sudanese Pound (1957–1998)'), ('SRD', 'Surinamese Dollar'), ('SRG', 'Surinamese Guilder'), ('SZL', 'Swazi Lilangeni'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('STN', 'São Tomé & Príncipe Dobra'), ('STD', 'São Tomé & Príncipe Dobra (1977–2017)'), ('TVD', 'TVD'), ('TJR', 'Tajikistani Ruble'), ('TJS', 'Tajikistani Somoni'), ('TZS', 'Tanzanian Shilling'), ('XTS', 'Testing Currency Code'), ('THB', 'Thai Baht'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('TPE', 'Timorese Escudo'), ('TOP', 'Tongan Paʻanga'), ('TTD', 'Trinidad & Tobago Dollar'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TRL', 'Turkish Lira (1922–2005)'), ('TMT', 'Turkmenistani Manat'), ('TMM', 'Turkmenistani Manat (1993–2009)'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('USS', 'US Dollar (Same day)'), ('UGX', 'Ugandan Shilling'), ('UGS', 'Ugandan Shilling (1966–1987)'), ('UAH', 'Ukrainian Hryvnia'), ('UAK', 'Ukrainian Karbovanets'), ('AED', 'United Arab Emirates Dirham'), ('UYW', 'Uruguayan Nominal Wage Index Unit'), ('UYU', 'Uruguayan Peso'), ('UYP', 'Uruguayan Peso (1975–1993)'), ('UYI', 'Uruguayan Peso (Indexed Units)'), ('UZS', 'Uzbekistani Som'), ('VUV', 'Vanuatu Vatu'), ('VES', 'Venezuelan Bolívar'), ('VEB', 'Venezuelan Bolívar (1871–2008)'), ('VEF', 'Venezuelan Bolívar (2008–2018)'), ('VND', 'Vietnamese Dong'), ('VNN', 'Vietnamese Dong (1978–1985)'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('XOF', 'West African CFA Franc'), ('YDD', 'Yemeni Dinar'), ('YER', 'Yemeni Rial'), ('YUN', 'Yugoslavian Convertible Dinar (1990–1992)'), ('YUD', 'Yugoslavian Hard Dinar (1966–1990)'), ('YUM', 'Yugoslavian New Dinar (1994–2002)'), ('YUR', 'Yugoslavian Reformed Dinar (1992–1993)'), ('ZWN', 'ZWN'), ('ZRN', 'Zairean New Zaire (1993–1998)'), ('ZRZ', 'Zairean Zaire (1971–1993)'), ('ZMW', 'Zambian Kwacha'), ('ZMK', 'Zambian Kwacha (1968–2012)'), ('ZWD', 'Zimbabwean Dollar (1980–2008)'), ('ZWR', 'Zimbabwean Dollar (2008)'), ('ZWL', 'Zimbabwean Dollar (2009)')], default='GBP', editable=False, max_length=3)),
                ('answer_currency', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='GBP', max_digits=14)),
                ('answer_status', models.BooleanField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.question')),
                ('surveyinstance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.surveyinstance')),
            ],
        ),
    ]
