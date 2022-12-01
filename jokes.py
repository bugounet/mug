import os
api_key = os.environ.get("AIRTABLE_API_KEY", None)

from pyairtable import Table
base_id = 'app60r3wYfbygIeZ5'
table_name = 'tblVGZBO6BSTH1EHL'
table = Table(api_key, base_id, table_name)
print(table.all())