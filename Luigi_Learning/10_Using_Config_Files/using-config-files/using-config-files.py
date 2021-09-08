import luigi
import os
from luigi import Task, Parameter, LocalTarget, IntParameter

OUTPUT_FOLDER = 'output'

class DownloadFile(Task):
    input_folder = Parameter()
    file_name = Parameter()
    index = IntParameter()

    def output(self):
        path = os.path.join(OUTPUT_FOLDER, str(self.index), self.file_name)
        return LocalTarget(path)

    def run(self):
        input_self = os.path.join(self.input_folder,self.file_name)
        with open(input_self) as f:
            with self.output().open('w') as out:
                for line in f:
                    out.write(line)


class DownloadSalesData(Task):
    input_folder = Parameter()

    def output(self):
        return LocalTarget('all_sales.csv')

    def run(self):
        processed_files = []
        counter = 1
        for file in sorted(os.listdir(self.input_folder)):
            target = yield DownloadFile(self.input_folder, file, counter )
            counter += 1
            processed_files.append(target)

        with self.output().open('w') as out:
            for file in processed_files:
                with file.open() as f:
                    for line in f:
                        out.write(line)

if __name__ == '__main__':
    luigi.run(['DownloadSalesData'])

