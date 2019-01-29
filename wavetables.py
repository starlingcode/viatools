import csv


class Wavetable:
    meta_tables = []
    meta_tables_used = set([])
    meta_table_data = {}
    meta_slope_banks = []
    meta_slope_data = {}
    meta_sample_data = {}
    sync_tables = []
    sync_tables_used = set([])
    sync_table_data = {}
    sync_slope_banks = []
    sync_slope_data = {}
    sync_sample_data = {}
    scanner_tables = []
    scanner_tables_used = set([])
    scanner_table_data = {}
    scanner_slope_banks = []
    scanner_slope_data = {}
    scanner_sample_data = {}

    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def read_meta_tables(self):

        with open('wavetable_resources/meta_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                self.meta_tables.append([row[0], row[1], row[2]])
                self.meta_tables_used.add(row[2])

    def read_sync_tables(self):

        with open('wavetable_resources/sync_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                self.sync_tables.append([row[0], row[1], row[2]])
                self.sync_tables_used.add(row[2])

    def read_scanner_tables(self):

        with open('wavetable_resources/scanner_tables.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:
                self.scanner_tables.append([row[0], row[1], row[2]])
                self.scanner_tables_used.add(row[2])

    def get_table_set_info(self):

        with open('wavetable_resources/table_definitions.csv', 'r') as csvfile:
            tablereader = csv.reader(csvfile, delimiter=',')
            for row in tablereader:

                if row[0] in self.meta_tables_used:
                    self.meta_table_data[row[0]] = [row[0], row[1], row[2], row[3]]
                    self.meta_slope_banks.append(row[1])
                    self.meta_slope_banks.append(row[2])

                if row[0] in self.sync_tables_used:
                    self.sync_table_data[row[0]] = [row[0], row[1], row[2], row[3]]
                    self.sync_slope_banks.append(row[1])
                    self.sync_slope_banks.append(row[2])

                if row[0] in self.scanner_tables_used:
                    self.scanner_table_data[row[0]] = [row[0], row[1], row[2], row[3]]
                    self.scanner_slope_banks.append(row[1])
                    self.scanner_slope_banks.append(row[2])

    def read_sample_data(self):

        for slope_tag in self.meta_slope_banks:
            with open('wavetable_resources/table_sample_defs/' + slope_tag + '.csv', 'r') as csvfile:
                slope_table = []
                slopereader = csv.reader(csvfile, delimiter=',')
                rowcounter = 0
                for row in slopereader:
                    if row[0] != '':
                        slope_table.append(slope_tag + str(rowcounter))
                        slope = []
                        for cell in row:
                            if self.is_number(cell) and cell != '':
                                slope.append(cell)
                        self.meta_sample_data[slope_tag + str(rowcounter)] = slope
                    rowcounter += 1

                self.meta_slope_data[slope_tag] = slope_table

        for slope_tag in self.sync_slope_banks:
            with open('wavetable_resources/table_sample_defs/' + slope_tag + '.csv', 'r') as csvfile:
                slope_table = []
                slopereader = csv.reader(csvfile, delimiter=',')
                rowcounter = 0
                for row in slopereader:
                    if row[0] != '':
                        slope_table.append(slope_tag + str(rowcounter))
                        slope = []
                        for cell in row:
                            if self.is_number(cell) and cell != '':
                                slope.append(cell)
                        self.sync_sample_data[slope_tag + str(rowcounter)] = slope
                    rowcounter += 1

                self.sync_slope_data[slope_tag] = slope_table

        for slope_tag in self.scanner_slope_banks:
            with open('wavetable_resources/table_sample_defs/' + slope_tag + '.csv', 'r') as csvfile:
                slope_table = []
                slopereader = csv.reader(csvfile, delimiter=',')
                rowcounter = 0
                for row in slopereader:
                    if row[0] != '' and rowcounter < 5:
                        slope_table.append(slope_tag + str(rowcounter))
                        slope = []
                        for cell in row:
                            if self.is_number(cell) and cell != '':
                                slope.append(cell)
                        self.scanner_sample_data[slope_tag + str(rowcounter)] = slope
                    rowcounter += 1

                self.scanner_slope_data[slope_tag] = slope_table

    def write_meta_header(self):

        text_file = open("generated_code/meta_tables.hpp", "w")
        text_file.truncate()

        header_stub = open("wavetable_resources/meta_tables_header.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        for slope in self.meta_sample_data:
            slope_length = len(self.meta_sample_data[slope]) - 1
            # text_file.write('\tstatic constexpr uint16_t ' + slope + '[' + str(slope_length) + '] = {\n\t\t')
            text_file.write('\t#define ' + slope + ' {\\\n\t\t')

            for index, i in enumerate(self.meta_sample_data[slope][0:slope_length]):
                if (index % 16) == 15:
                    text_file.write(i + ',\\\n\t\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(self.meta_sample_data[slope][slope_length] + '}\n\n')

        for bank in self.meta_slope_data:
            table_length = len(self.meta_slope_data[bank]) - 1
            text_file.write('\tstatic constexpr uint16_t ' + bank + '[' + str(table_length + 1) + '][257] = {\n\t\t')
            for index, i in enumerate(self.meta_slope_data[bank][0:table_length]):
                if (index % 4) == 3:
                    text_file.write(i + ',\n\t\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(self.meta_slope_data[bank][table_length] + '};\n\n')

        text_file.write("\t// TABLES \n\n")

        for wavetable in self.meta_table_data:
            text_file.write('\tstatic constexpr Wavetable ' + self.meta_table_data[wavetable][0] + ' = {\n')
            text_file.write('\t\t.attackSlope = ' + self.meta_table_data[wavetable][1] + ',\n')
            text_file.write('\t\t.releaseSlope = ' + self.meta_table_data[wavetable][2] + ',\n')
            text_file.write('\t\t.slopeLength = 256,\n')
            text_file.write('\t\t.numWaveforms = ' + str(len(self.meta_slope_data[self.meta_table_data[wavetable][1]]))
                            + '};\n\n')

        text_file.write('};\n\n')

        text_file.write('#endif')

        text_file.close()

    def write_sync_header(self):
        
        text_file = open("generated_code/sync_tables.hpp", "w")
        text_file.truncate()

        header_stub = open("wavetable_resources/sync_tables_header.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        for slope in self.sync_sample_data:
            slope_length = len(self.sync_sample_data[slope]) - 1
            # text_file.write('\tstatic constexpr uint16_t ' + slope + '[' + str(slope_length) + '] = {\n\t\t')
            text_file.write('\t#define ' + slope + ' {\\\n\t\t')
            for index, i in enumerate(self.sync_sample_data[slope][0:slope_length]):
                if (index % 16) == 15:
                    text_file.write(i + ',\\\n\t\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(self.sync_sample_data[slope][slope_length] + '}\n\n')

        for bank in self.sync_slope_data:
            table_length = len(self.sync_slope_data[bank]) - 1
            text_file.write('\tstatic constexpr uint16_t ' + bank + '[' + str(table_length + 1) + '][257] = {\n\t\t')
            for index, i in enumerate(self.sync_slope_data[bank][0:table_length]):
                if (index % 4) == 3:
                    text_file.write(i + ',\n\t\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(self.sync_slope_data[bank][table_length] + '};\n\n')

        text_file.write("\t// TABLES \n\n")

        for wavetable in self.sync_table_data:
            text_file.write('\tstatic constexpr Wavetable ' + self.sync_table_data[wavetable][0] + ' = {\n')
            text_file.write('\t\t.attackSlope = ' + self.sync_table_data[wavetable][1] + ',\n')
            text_file.write('\t\t.releaseSlope = ' + self.sync_table_data[wavetable][2] + ',\n')
            text_file.write('\t\t.slopeLength = 256,\n')
            text_file.write('\t\t.numWaveforms = ' + str(len(self.sync_slope_data[self.sync_table_data[wavetable][1]]))
                            + '};\n\n')

        text_file.write('};\n\n')

        text_file.write('#endif')

        text_file.close()

    def write_scanner_header(self):
        
        text_file = open("generated_code/scanner_tables.hpp", "w")
        text_file.truncate()

        header_stub = open("wavetable_resources/scanner_tables_header.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        for slope in self.scanner_sample_data:
            slope_length = len(self.scanner_sample_data[slope]) - 1
            # text_file.write('\tstatic constexpr uint16_t ' + slope + '[' + str(slope_length) + '] = {\n\t\t')
            text_file.write('\t#define ' + slope + ' {\\\n\t\t')

            for index, i in enumerate(self.scanner_sample_data[slope][0:slope_length]):
                if (index % 16) == 15:
                    text_file.write(i + ',\\\n\t\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(self.scanner_sample_data[slope][slope_length] + '}\n\n')

        for bank in self.scanner_slope_data:
            table_length = len(self.scanner_slope_data[bank]) - 1
            text_file.write('\tstatic constexpr uint16_t ' + bank + '[' + str(table_length + 1) + '][257] = {\n\t\t')
            for index, i in enumerate(self.scanner_slope_data[bank][0:table_length]):
                if (index % 4) == 3:
                    text_file.write(i + ',\n\t\t')
                else:
                    text_file.write(i + ', ')
            text_file.write(self.scanner_slope_data[bank][table_length] + '};\n\n')

        text_file.write("\t// TABLES \n\n")

        for wavetable in self.scanner_table_data:
            text_file.write('\tstatic constexpr Wavetable ' + self.scanner_table_data[wavetable][0] + ' = {\n')
            text_file.write('\t\t.attackSlope = ' + self.scanner_table_data[wavetable][1] + ',\n')
            text_file.write('\t\t.releaseSlope = ' + self.scanner_table_data[wavetable][2] + ',\n')
            text_file.write('\t\t.slopeLength = 256,\n')
            text_file.write('\t\t.numWaveforms = ' + str(len(self.scanner_slope_data[
                                                                 self.scanner_table_data[wavetable][1]])) + '};\n\n')

        text_file.write('};\n\n')

        text_file.write('#endif')

        text_file.close()
        
    def write_source_code(self):

        size_in_bytes = 0
        word_size = 4
        halfword_size = 2

        text_file = open("generated_code/meta_table_init.cpp", "w")
        text_file.truncate()

        text_file.write("#include \"meta.hpp\"\n\n\n")

        text_file.write('void ViaMeta::fillWavetableArray(void) {\n\n')

        for table in self.meta_tables:
            if int(table[0]) < 3:
                text_file.write('\twavetableArray[' + table[0] + '][' + table[1] + '] = &wavetableSet.' + table[2] + ';\n')

        text_file.write("}\n\n")

        for table in self.meta_tables_used:
            text_file.write('constexpr Wavetable MetaWavetableSet::' + table + ';\n')
            size_in_bytes += word_size * 5

        text_file.write('\n')

        for key, item in self.meta_slope_data.items():
            size_in_bytes += word_size * 1
            text_file.write('constexpr uint16_t MetaWavetableSet::' + key + '[' + str(len(item)) + '][257];\n')
            for slope in item:
                size_in_bytes += halfword_size * 257
                # text_file.write('constexpr uint16_t MetaWavetableSet::' + slope + '[];\n')
            text_file.write('\n')

        print("The meta data should take up ~ " + str(size_in_bytes) + " bytes")

        header_stub = open("wavetable_resources/meta_source_footer.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        text_file = open("generated_code/sync_table_init.cpp", "w")
        text_file.truncate()

        text_file.write("#include \"sync.hpp\"\n\n\n")

        text_file.write('void ViaSync::fillWavetableArray(void) {\n\n')

        for table in self.sync_tables:
            if int(table[0]) < 4:
                text_file.write('\twavetableArray[' + table[0] + '][' + table[1] + '] = &wavetableSet.' + table[2] + ';\n')
            else:
                text_file.write('\twavetableArrayGlobal[' + table[1] + '] = &wavetableSet.' + table[2] + ';\n')

        text_file.write("}\n\n")

        size_in_bytes = 0

        for key in self.sync_tables_used:
            text_file.write('constexpr Wavetable SyncWavetableSet::' + key + ';\n')
            size_in_bytes += word_size * 5

        text_file.write('\n')

        for key, item in self.sync_slope_data.items():
            text_file.write('constexpr uint16_t SyncWavetableSet::' + key + '[' + str(len(item)) + '][257];\n')
            size_in_bytes += word_size * 1
            for slope in item:
                # text_file.write('constexpr uint16_t SyncWavetableSet::' + slope + '[];\n')
                size_in_bytes += halfword_size * 257
            text_file.write('\n')

        print("The sync data should take up ~ " + str(size_in_bytes) + " bytes")

        header_stub = open("wavetable_resources/sync_source_footer.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()

        text_file = open("generated_code/scanner_table_init.cpp", "w")
        text_file.truncate()

        text_file.write("#include \"scanner.hpp\"\n\n\n")

        text_file.write('void ViaScanner::fillWavetableArray(void) {\n\n')

        for table in self.scanner_tables:
            if int(table[0]) < 4:
                text_file.write('\twavetableArray[' + table[0] + '][' + table[1] + '] = &wavetableSet.' + table[2] + ';\n')
            else:
                text_file.write('\twavetableArrayGlobal[' + table[1] + '] = &wavetableSet.' + table[2] + ';\n')

        text_file.write("}\n\n")

        size_in_bytes = 0

        for key in self.scanner_tables_used:
            text_file.write('constexpr Wavetable ScannerWavetableSet::' + key + ';\n')
            size_in_bytes += word_size * 5

        text_file.write('\n')

        for key, item in self.scanner_slope_data.items():
            text_file.write('constexpr uint16_t ScannerWavetableSet::' + key + '[' + str(len(item)) + '][257];\n')
            size_in_bytes += word_size * 1
            for slope in item:
                # text_file.write('constexpr uint16_t ScannerWavetableSet::' + slope + '[];\n')
                size_in_bytes += halfword_size * 257
            text_file.write('\n')

        print("The scanner data should take up ~ " + str(size_in_bytes) + " bytes")

        header_stub = open("wavetable_resources/scanner_source_footer.txt", 'r')

        for line in header_stub:
            text_file.write(line)

        header_stub.close()


    def generate_table_code(self):

        self.read_meta_tables()
        self.read_scanner_tables()
        self.read_sync_tables()
        self.get_table_set_info()
        self.read_sample_data()
        self.write_meta_header()
        self.write_sync_header()
        self.write_scanner_header()
        self.write_source_code()
