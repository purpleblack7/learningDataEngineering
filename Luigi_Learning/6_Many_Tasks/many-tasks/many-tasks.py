import luigi
from luigi import Task, LocalTarget, WrapperTask


class DownloadSalesData(Task):
    def output(self):
        return LocalTarget('all_sales.csv')

    def run(self):
        with self.output().open('w') as f:
            print('France,May,100', file = f)
            print('Germany,May,120', file = f)
            print('France,June,150', file = f)
            print('Germany,June,180', file = f)

class GetFranceSales(Task):
    def requires(self):
        return DownloadSalesData()

    def output(self):
        return LocalTarget('france_sales.csv')

    def run(self):
        with self.output().open('w') as out:
            with self.input().open() as f:
                for line in f:
                    if line.startswith('France'):
                        out.write(line)

class SummarizeFranceSales(Task):
    def requires(self):
        return GetFranceSales()
    def output(self):
        return LocalTarget('summary_france_sales.csv')

    def run(self):
        total = 0
        with self.input().open() as f:
            for line in f:
                aa = line.split(',')
                total += float(aa[2])
        with self.output().open('w') as out:
            out.write(str(total))


class GetGermanySales(Task):
    def requires(self):
        return DownloadSalesData()

    def output(self):
        return LocalTarget('germany_sales.csv')

    def run(self):
        with self.output().open('w') as out:
            with self.input().open() as f:
                for line in f:
                    if line.startswith('Germany'):
                        out.write(line)


class SummarizeGermanySales(Task):
    def requires(self):
        return GetGermanySales()
    def output(self):
        return LocalTarget('summary_germany_sales.csv')

    def run(self):
        total = 0
        with self.input().open() as f:
            for line in f:
                aa = line.split(',')
                total += float(aa[2])
        with self.output().open('w') as out:
            out.write(str(total))

#Wrapper Task
class Final(WrapperTask):
    def requires(self):
        return [SummarizeFranceSales(),SummarizeGermanySales()]

if __name__ == '__main__':
    luigi.run(['Final'])

