# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-17 18:27
from __future__ import unicode_literals

import autoslug.fields
import carceropolis.options
import carceropolis.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaDeAtuacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=250, unique=True, verbose_name=b'Nome da \xc3\xa1rea')),
                ('descricao', models.TextField(verbose_name=b'Descri\xc3\xa7\xc3\xa3o')),
                ('ordem', models.IntegerField(unique=True, verbose_name=b'Ordem')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from=b'nome')),
            ],
            options={
                'verbose_name': '\xc1rea de Atua\xe7\xe3o',
                'verbose_name_plural': '\xc1reas de Atua\xe7\xe3o',
            },
        ),
        migrations.CreateModel(
            name='ArquivoBaseCarceropolis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=carceropolis.options.current_year)),
                ('mes', models.CharField(choices=[(b'Janeiro', b'Janeiro'), (b'Fevereiro', b'Fevereiro'), (b'Mar\xc3\xa7o', b'Mar\xc3\xa7o'), (b'Abril', b'Abril'), (b'Maio', b'Maio'), (b'Junho', b'Junho'), (b'Julho', b'Julho'), (b'Agosto', b'Agosto'), (b'Setembro', b'Setembro'), (b'Outubro', b'Outubro'), (b'Novembro', b'Novembro'), (b'Dezembro', b'Dezembro')], default=carceropolis.options.current_month, max_length=40, verbose_name=b'M\xc3\xaas')),
                ('arquivo', models.FileField(upload_to=b'base_bruta_carceropolis/', validators=[carceropolis.validators.check_filetype])),
                ('salvo_em', models.DateTimeField(auto_now_add=True, verbose_name=b'Salvo em')),
            ],
            options={
                'verbose_name': 'Base bruta Carcer\xf3polis',
                'verbose_name_plural': 'Bases brutas Carcer\xf3polis',
            },
        ),
        migrations.CreateModel(
            name='BaseMJ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=carceropolis.options.current_year)),
                ('mes', models.CharField(choices=[(b'Janeiro', b'Janeiro'), (b'Fevereiro', b'Fevereiro'), (b'Mar\xc3\xa7o', b'Mar\xc3\xa7o'), (b'Abril', b'Abril'), (b'Maio', b'Maio'), (b'Junho', b'Junho'), (b'Julho', b'Julho'), (b'Agosto', b'Agosto'), (b'Setembro', b'Setembro'), (b'Outubro', b'Outubro'), (b'Novembro', b'Novembro'), (b'Dezembro', b'Dezembro')], default=carceropolis.options.current_month, max_length=40, verbose_name=b'M\xc3\xaas')),
                ('arquivo', models.FileField(upload_to=b'base_bruta_mj/', validators=[carceropolis.validators.check_filetype])),
                ('salvo_em', models.DateTimeField(auto_now_add=True, verbose_name=b'Salvo em')),
            ],
            options={
                'verbose_name': 'Base bruta MJ',
                'verbose_name_plural': 'Bases brutas MJ',
            },
        ),
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80, unique=True, verbose_name=b'Nome da especialidade')),
                ('descricao', models.TextField(blank=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from=b'nome')),
            ],
            options={
                'verbose_name': 'Especialidade',
                'verbose_name_plural': 'Especialidades',
            },
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('ddi', models.IntegerField(blank=True, default=55, null=True, verbose_name=b'DDI')),
                ('ddd', models.IntegerField(blank=True, null=True, verbose_name=b'DDD')),
                ('telefone', models.IntegerField(blank=True, null=True, verbose_name=b'Telefone')),
                ('mini_bio', models.CharField(blank=True, max_length=600)),
                ('instituicao', models.CharField(max_length=250, verbose_name=b'Institui\xc3\xa7\xc3\xa3o')),
                ('area_de_atuacao', models.ManyToManyField(to='carceropolis.AreaDeAtuacao', verbose_name=b'\xc3\x81rea de atua\xc3\xa7\xc3\xa3o')),
                ('especialidades', models.ManyToManyField(to='carceropolis.Especialidade')),
            ],
            options={
                'verbose_name': 'Especialista',
                'verbose_name_plural': 'Especialistas',
            },
        ),
        migrations.CreateModel(
            name='Publicacao',
            fields=[
                ('blogpost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.BlogPost')),
                ('autoria', models.CharField(max_length=150, verbose_name=b'Autoria')),
                ('ano_de_publicacao', models.IntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=carceropolis.options.current_year, verbose_name=b'Ano de publica\xc3\xa7\xc3\xa3o')),
                ('arquivo_publicacao', models.FileField(upload_to=b'publicacoes/', verbose_name=b'Arquivo da publica\xc3\xa7\xc3\xa3o')),
                ('categorias', models.ManyToManyField(to='carceropolis.AreaDeAtuacao', verbose_name=b'Categorias')),
            ],
            options={
                'verbose_name': 'Publica\xe7\xe3o',
                'verbose_name_plural': 'Publica\xe7\xf5es',
            },
            bases=('blog.blogpost',),
        ),
        migrations.CreateModel(
            name='UnidadePrisional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_unidade', models.CharField(max_length=255, verbose_name=b'Nome da Unidade')),
                ('sigla_unidade', models.CharField(max_length=10)),
                ('tipo_logradouro', models.CharField(max_length=20)),
                ('nome_logradouro', models.CharField(max_length=255)),
                ('numero', models.IntegerField(blank=True, null=True, verbose_name=b'N\xc3\xbamero')),
                ('complemento', models.CharField(blank=True, max_length=255)),
                ('bairro', models.CharField(max_length=255)),
                ('uf', models.CharField(choices=[(b'AC', b'Acre'), (b'AL', b'Alagoas'), (b'AP', b'Amap\xc3\xa1'), (b'AM', b'Amazonas'), (b'BA', b'Bahia'), (b'CE', b'Cear\xc3\xa1'), (b'DF', b'Distrito Federal'), (b'ES', b'Esp\xc3\xadrito Santo'), (b'GO', b'Goi\xc3\xa1s'), (b'MA', b'Maranh\xc3\xa3o'), (b'MT', b'Mato Grosso'), (b'MS', b'Mato Grosso do Sul'), (b'MG', b'Minas Gerais'), (b'PA', b'Par\xc3\xa1'), (b'PB', b'Para\xc3\xadba'), (b'PR', b'Paran\xc3\xa1'), (b'PE', b'Pernambuco'), (b'PI', b'Piau\xc3\xad'), (b'RJ', b'Rio de Janeiro'), (b'RN', b'Rio Grande do Norte'), (b'RS', b'Rio Grande do Sul'), (b'RO', b'Rond\xc3\xb4nia'), (b'RR', b'Roraima'), (b'SC', b'Santa Catarina'), (b'SP', b'S\xc3\xa3o Paulo'), (b'SE', b'Sergipe'), (b'TO', b'Tocantins')], max_length=2)),
                ('cep', models.CharField(max_length=8)),
                ('ddd', models.IntegerField(blank=True, null=True, verbose_name=b'DDD')),
                ('telefone', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cidades.Cidade', verbose_name=b'Munic\xc3\xadpio')),
            ],
            options={
                'verbose_name': 'Unidade Prisional',
                'verbose_name_plural': 'Unidades Prisionais',
            },
        ),
    ]