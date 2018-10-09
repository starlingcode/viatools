import csv


class Wavetable:

    tables_used = set([])
    slopes_used = set([])
    table_bank = []
    slope_tables = []
    slopes = []


    def get_table_lengths(self, family, familybank, slopefamilies, tables):

        familydef = ''
        example_slope = ''
        num_tables = 0
        num_samples = 0

        for idx in familybank:
            if idx[0] == family:
                familydef = idx[1]
        for jdx in slopefamilies:
            if jdx[0] == familydef:
                example_slope = jdx[1]
                num_tables = len(jdx) - 1
        for udx in tables:
            if udx[0] == example_slope:
                num_samples = len(udx) - 2

        return [num_tables, num_samples]


    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def read_meta_tables(self):

        tables = []

        with open('wavetable_resources/meta_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                    tables.append([row[0], row[1], row[2]])

            for table in tables:
                self.tables_used.add(table[2])

        return tables

    def get_table_set_info(self):

        with open('wavetable_resources/table_definitions.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                if row[0] in self.tables_used:
                    self.table_bank.append([row[0], row[1], row[2], row[3]])
                    self.slopes_used.add(row[1])
                    self.slopes_used.add(row[2])

    def read_sample_data(self):

        for slope_tag in self.slopes_used:
            with open('wavetable_resources/table_sample_defs/' + slope_tag + '.csv', 'r') as csvfile:
                slope_table = [slope_tag]
                slopereader = csv.reader(csvfile, delimiter=',')
                rowcounter = 0
                # not very pythonic...
                for row in slopereader:
                    if row[0] != '':
                        slope_table.append(slope_tag + str(rowcounter))
                        slope = []
                        slope.append(slope_tag + str(rowcounter))
                        j = 0
                        while j < len(row) and row[j] != '':
                            if self.is_number(row[j]):
                                slope.append(row[j])
                            j += 1
                        self.slopes.append(slope)
                    rowcounter += 1

                self.slope_tables.append(slope_table)









