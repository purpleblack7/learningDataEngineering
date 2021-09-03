import luigi
from luigi import LocalTarget, Task
from luigi.contrib import sqla
from sqlalchemy import Float, String


class DownloadFranceSales(Task):
    def output(selfself):
        return LocalTarget('france.csv')

    def run(self):
        with self.output().open('w') as f:
            print('May,100', file=f)
            print('June,200', file=f)


class DownloadGermanySales(Task):
    def output(self):
        return LocalTarget('germany.csv')

    def run(self):
        with self.output().open('w') as f:
            print('May,180', file=f)

class CreateDatabase(sqla.CopyToTable):
    columns = [
        (["month", String(64)], {}),
        (["amount", Float], {})
     ]
    connection_string = "sqlite:///test.db"  # in memory SQLite database
    table = "sales" # name of the table to store data
    column_separator = ','

    def rows(self):
        with self.input()[0].open() as f:
            for line in f:
                yield line.split(self.column_separator)

        with self.input()[1].open() as f:
            for line in f:
                yield line.split(self.column_separator)
    def requires(self):
        return [DownloadFranceSales(),DownloadGermanySales()]

if __name__ == '__main__':
    luigi.run(['CreateDatabase', '--local-scheduler'])