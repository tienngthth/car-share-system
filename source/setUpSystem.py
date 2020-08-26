from setupSampleRecord import add_sample_data
from setupTables import create_all_tables

if __name__ == "__main__":
    create_all_tables()
    add_sample_data()