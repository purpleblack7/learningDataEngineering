from luigi import Task, LocalTarget

class ProcessOrders(Task):
    def output(self):
        return LocalTarget('orders.csv')

    def run(self):
        with self.output().open('w') as f:
            print('May,100', file = f)
            print('May,180', file=f)
            print('June,200', file=f)
            print('June,150', file=f)


class GenerateReport(Task):
    def requires(self):
        return ProcessOrders()

    def output(self):
        return LocalTarget('report.csv')

    def run(self):
        report = {}
        for line in self.input().open():
        #From the GenerateReport task, we can read this file without knowing its name using the self.input method
            month,amount  = line.split(',')
            if month in report:
                report[month] += float(amount)
            else:
                report[month] = float(amount)

        with self.output().open('w') as out:
            for month in report:
                print(month + ',' + str(report[month]), file = out)

if __name__ == '__main__':
    import luigi
    luigi.run(['GenerateReport','--local-scheduler'])
