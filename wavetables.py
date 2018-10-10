import csv


class Wavetable:

    tables_used = set([])
    slopes_used = set([])
    meta_tables = []
    scanner_tables = []
    sync_tables = []
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

        self.meta_tables = []

        with open('wavetable_resources/meta_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                    self.meta_tables.append([row[0], row[1], row[2]])

            for table in self.meta_tables:
                self.tables_used.add(table[2])

    def read_sync_tables(self):

        self.meta_tables = []

        with open('wavetable_resources/sync_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                    self.sync_tables.append([row[0], row[1], row[2]])

            for table in self.sync_tables:
                self.tables_used.add(table[2])

    def read_scanner_tables(self):

        self.meta_tables = []

        with open('wavetable_resources/scanner_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                    self.scanner_tables.append([row[0], row[1], row[2]])

            for table in self.scanner_tables:
                self.tables_used.add(table[2])


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

    def write_sample_data(self):

        text_file = open("generated_code/sample_data.hpp", "w")
        text_file.truncate()

        header_stub = open("wavetable_resources/table_samples_header.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        for slope in self.slopes:
            slope_length = len(slope) - 1
            text_file.write('static const uint16_t ' + slope[0] + '[' + str(slope_length) + '] = {\n\t')
            for i in slope[1:(slope_length)]:
                if (slope.index(i) % 8) == 0:
                    text_file.write(i + ',\n\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(slope[slope_length] + '};\n\n\n')

        header_stub = open("wavetable_resources/table_samples_footer.txt")

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        text_file.close()

    def write_table_header(self):

        text_file = open("generated_code/tables.hpp", "w")
        text_file.truncate()

        header_stub = open("wavetable_resources/table_defs_header.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        for table in self.slope_tables:
            table_length = len(table) - 1
            text_file.write('static const uint16_t *' + table[0] + '[' + str(table_length) + '] = {\n\t')
            for i in table[1:(table_length)]:
                if (table.index(i) % 8) == 0:
                    text_file.write(i + ',\n\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(table[table_length] + '};\n\n\n')

        text_file.write("// TABLES \n\n\n")

        for wavetable in self.table_bank:
            text_file.write('static const Wavetable ' + wavetable[0] + ' = {\n')
            text_file.write('\t.attackSlope = ' + wavetable[1] + ',\n')
            text_file.write('\t.releaseSlope = ' + wavetable[2] + ',\n')
            text_file.write(
                '\t.slopeLength = ' + str(self.get_table_lengths(wavetable[0], self.table_bank, self.slope_tables, self.slopes)[1]) + ',\n')
            text_file.write('\t.numWaveforms = ' + str(
                self.get_table_lengths(wavetable[0], self.table_bank, self.slope_tables, self.slopes)[0]) + '};\n\n\n')

        text_file.write('\n\n')

        header_stub = open("wavetable_resources/table_defs_footer.txt")

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        text_file.close()

    def write_meta_source(self):

        text_file = open("generated_code/meta_table_init.cpp", "w")
        text_file.truncate()

        text_file.write("# include \"meta.hpp\"\n\n\n")

        text_file.write('void ViaMeta::fillWavetableArray(void) {\n\n')

        for table in self.meta_tables:
                text_file.write('\twavetableArray[' + table[0] + '][' + table[1] + '] = &' + table[2] + ';\n')

        text_file.write("}\n\n")

        header_stub = open("wavetable_resources/meta_tables_footer.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()
        
    def write_sync_source(self):

        text_file = open("generated_code/sync_table_init.cpp", "w")
        text_file.truncate()

        text_file.write("# include \"sync.hpp\"\n\n\n")

        text_file.write('void ViaSync::fillWavetableArray(void) {\n\n')

        for table in self.sync_tables:
            if int(table[0]) < 4:
                text_file.write('\twavetableArray[' + table[0] + '][' + table[1] + '] = &' + table[2] + ';\n')
            else:
                text_file.write('\twavetableArrayGlobal[' + table[1] + '] = &' + table[2] + ';\n')

        text_file.write("}\n\n")

        header_stub = open("wavetable_resources/sync_tables_footer.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()
        
    def write_scanner_source(self):

        text_file = open("generated_code/scanner_table_init.cpp", "w")
        text_file.truncate()

        text_file.write("#include \"scanner.hpp\"\n\n\n")

        text_file.write('void ViaScanner::fillWavetableArray(void) {\n\n')

        for table in self.scanner_tables:
                text_file.write('\twavetableArray[' + table[1] + '] = &' + table[2] + ';\n')

        text_file.write("}\n\n")

        header_stub = open("wavetable_resources/scanner_tables_footer.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

    def generate_table_code(self):

        self.read_meta_tables()
        self.read_scanner_tables()
        self.read_sync_tables()
        self.get_table_set_info()
        self.read_sample_data()
        self.write_sample_data()
        self.write_table_header()
        self.write_meta_source()
        self.write_sync_source()
        self.write_scanner_source()












