# OTree ARK Experiment
## What to change to make it work
The server uses an external PostgreSQL database. Please create one and change the settings in `InitializeDatabase.py`. OTree uses a SQLite database by default, which is contained in the repository.

To initialize the external database, please run the following script:

```bash
python InitializeDatabase.py
```

If the database/user/password is changed, please do not forget to change the settings under `phase2/__init__.py` in `class Correct(Page)`.

You can change the number of participants allowed at once in `settings.py` under `SESSION_CONFIGS` under `num_demo_participants`.