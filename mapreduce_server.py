from mrjob.job import MRJob
from mrjob.job import MRStep

class server_login(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper,reducer=self.reducer)
        ]

    def mapper(self, _, line):
        data = line.split("     ")
        yield data, 1

    def reducer(self, key, list_of_values):
        totol_attempts = 0
        for i in list_of_values:
            totol_attempts += i
        if totol_attempts<20:
            return key
        yield key, totol_attempts

if __name__ == '__main__':
    server_login.run()
