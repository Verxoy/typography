"""Вывод схемы PostgreSQL для проекта Tipography."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

TABLES = [
    'api_callbackrequest',
    'api_contactmessage',
    'api_resume',
    'api_quoterequest',
    'api_quoteattachment',
    'auth_user',
    'django_migrations',
]


def main():
  with connection.cursor() as c:
    c.execute(
      """
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
      ORDER BY table_name
      """
    )
    all_tables = [r[0] for r in c.fetchall()]

  print('=' * 72)
  print('ТАБЛИЦЫ В БД (public)')
  print('=' * 72)
  for t in all_tables:
    print(f'  • {t}')
  print()

  focus = [t for t in TABLES if t in all_tables]
  extra = [t for t in all_tables if t.startswith('api_') and t not in focus]
  for t in extra:
    focus.append(t)

  with connection.cursor() as c:
    for table in focus:
      c.execute(
        """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
        """,
        [table],
      )
      cols = c.fetchall()
      c.execute(f'SELECT COUNT(*) FROM "{table}"')
      count = c.fetchone()[0]

      print('=' * 72)
      print(f'{table}  ({count} записей)')
      print('=' * 72)
      for name, dtype, nullable, default in cols:
        null = 'NULL' if nullable == 'YES' else 'NOT NULL'
        dflt = f'  default={default}' if default else ''
        print(f'  {name:28} {dtype:24} {null}{dflt}')
      print()

      if count and table.startswith('api_') and count <= 20:
        c.execute(f'SELECT * FROM "{table}" ORDER BY id DESC LIMIT 5')
        colnames = [d[0] for d in c.description]
        rows = c.fetchall()
        print('  Последние записи:')
        for row in rows:
          print('  ---')
          for col, val in zip(colnames, row):
            if val is not None and str(val) != '':
              s = str(val)
              if len(s) > 80:
                s = s[:77] + '...'
              print(f'    {col}: {s}')
        print()


if __name__ == '__main__':
  main()
