"""
MARC Crucible is released under "The MIT License (MIT)"

Copyright © 2023 Joseph Alway

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import glob
import pymarc
import datetime
import sys
import os
import re


def load_records():
    # Load records from MARC record file.
    list_of_record_objects = []
    file_loading = True
    while file_loading:
        # Get name of MARC record file to load.
        marc_file_to_load = ''
        file_load_name_not_acceptable = True
        while file_load_name_not_acceptable:
            print('File extension must be \".mrc\" or \".raw\". Extension .mrc assumed, if valid extension not given.')
            print('Enter \":q\" to quit.')
            marc_file_to_load = input('MARC record(s) file path: ')
            if marc_file_to_load.lower() == ':q':
                sys.exit()
            else:
                try:
                    if marc_file_to_load[-4:].lower() != '.mrc' and marc_file_to_load[-4:].lower() != '.raw':
                        marc_file_to_load += '.mrc'
                        if glob.glob(marc_file_to_load):
                            file_load_name_not_acceptable = False
                        else:
                            print('ERROR: Invalid Filename. Does the file exist? '
                                  'Does the file have a .mrc or .raw extension?')
                    elif glob.glob(marc_file_to_load) and ((marc_file_to_load[-4:].lower() == '.mrc')
                                                           or (marc_file_to_load[-4:].lower() == '.raw')):
                        file_load_name_not_acceptable = False
                    elif glob.glob(marc_file_to_load):
                        print('ERROR: Invalid Filename. File must have .mrc or .raw extension. '
                              'Must provide valid MARC file.')
                    else:
                        print('ERROR: Invalid Filename. Does the file exist?')
                except OSError:
                    print('ERROR: Invalid Filename. Does the file exist?')
        # Load MARC file.
        load_start_time = datetime.datetime.now()
        try:
            with open(str(marc_file_to_load), 'rb') as fh:
                # Normal reading of good data:
                # reader = pym.MARCReader(fh)
                #
                # Added to_unicode=False, force_utf8=False, hide_utf8_warnings=False, and utf8_handling='strict'
                # (This keeps the MARCReader module from choking on bad data.
                # It also reports when a warning is encountered.)
                reader = pymarc.MARCReader(fh, to_unicode=False, force_utf8=False, hide_utf8_warnings=True,
                                           utf8_handling='strict')
                for marc_record in reader:
                    list_of_record_objects.append(marc_record)
        except (FileNotFoundError, OSError):
            marc_file_to_load = ''
            list_of_record_objects = [None]
        load_end_time = datetime.datetime.now()

        # Print to screen, the time it took to load the record file.
        load_time = str(format((load_end_time - load_start_time).total_seconds(), '.2f'))
        print('Time to load record(s): ' + load_time + ' seconds')
        if list_of_record_objects == [None]:
            print('ERROR: No records loaded. Does the file exist? Is it a valid MARC file?')
        else:
            file_loading = False
    return list_of_record_objects


def clear_screen():
    microsoft_names = ['nt', 'dos', 'ce']
    unix_and_linux = ['posix']
    if 'idlelib' in sys.modules:
        pass
    elif 'pycharm_hosted' in os.environ:
        pass
    else:
        for name in microsoft_names:
            if name in os.name.lower():
                os.system('cls')
        for name in unix_and_linux:
            if name in os.name.lower():
                os.system('clear')


def main_menu():
    error_message = ''
    selected_menu_number = ''
    invalid_entry = True
    while invalid_entry:
        print('Menu: Enter the number of a menu item to continue.')
        print('[1]:Load MARC File\n'
              '[2]:Enter Search Field(s)\n'
              '[3]:Enter Search Term(s)\n'
              '[4]:Run Search\n'
              '[5]:Run RegEx Search\n'
              '[6]:Count Records\n'
              '[7]:List Fields and Subfields in Record Set\n'
              '[8]:Save Matching Records\n'
              '[9]:Settings\n'
              '[0]:Quit')
        if error_message:
            print(error_message)
            error_message = ''
        else:
            pass
        try:
            selected_menu_number = input('Enter Selection: ')
            if len(selected_menu_number) == 1:
                if selected_menu_number in '1234567890':
                    invalid_entry = False
                else:
                    clear_screen()
                    error_message = 'ERROR: Invalid Entry. Enter matching number of menu entry.'
        except KeyError:
            pass
        clear_screen()
    return selected_menu_number


def user_entry_field_subfield():
    # Search Field(s)
    field_subfield_list = []
    field_subfield_to_search_not_acceptable = True
    while field_subfield_to_search_not_acceptable:
        print('Enter Search Field and/or Subfield Examples: 245a, 245, or a.')
        print('Enter \":q\" to quit.')
        field_subfield_string = input('Search Field+Subfield: ')
        if field_subfield_string.lower() == ':q':
            sys.exit()
        elif field_subfield_string.isnumeric() and len(field_subfield_string) == 3:
            field_to_search = field_subfield_string
            subfield_to_search = ''
            field_subfield_list = [(str(field_to_search), str(subfield_to_search))]
            field_subfield_to_search_not_acceptable = False
        elif field_subfield_string.isalpha() and field_subfield_string.lower() == 'ldr':
            field_to_search = 'ldr'
            subfield_to_search = ''
            field_subfield_list = [(str(field_to_search), str(subfield_to_search))]
            field_subfield_to_search_not_acceptable = False
        elif field_subfield_string.isalnum() and len(field_subfield_string) == 4 \
                and field_subfield_string[:-1].isnumeric() and field_subfield_string[-1:].isalpha():
            field_to_search = field_subfield_string[:-1]
            subfield_to_search = field_subfield_string[-1:]
            field_subfield_list = [(str(field_to_search), str(subfield_to_search))]
            field_subfield_to_search_not_acceptable = False
        elif field_subfield_string == '':
            field_to_search = ''
            subfield_to_search = ''
            field_subfield_list = [(str(field_to_search), str(subfield_to_search))]
            field_subfield_to_search_not_acceptable = False
        elif field_subfield_string.isalpha() and len(field_subfield_string) == 1:
            field_to_search = ''
            subfield_to_search = field_subfield_string
            field_subfield_list = [(str(field_to_search), str(subfield_to_search))]
            field_subfield_to_search_not_acceptable = False
        else:
            field_to_search = ''
            subfield_to_search = ''
            field_subfield_list = [(str(field_to_search), str(subfield_to_search))]
            field_subfield_to_search_not_acceptable = False
            print('WARNING: Searching All Fields and All Subfields of All Records. This may take a long time.')
    return field_subfield_list


def user_entry_search_term_or_terms():
    search_term_list = []
    search_term_not_acceptable = True
    while search_term_not_acceptable:
        print('Enter Search Term. Example: ')
        print('Enter \":q\" to quit.')
        search_term_string = input('Enter Search Term: ')
        if search_term_string.lower() == ':q':
            sys.exit()
        elif 0 < len(search_term_string) < 256:
            search_term_list.append(search_term_string)
            search_term_not_acceptable = False
        else:
            print('ERROR: Must provide a search term.')
    return search_term_list


def user_entry_settings():
    whole_word_search_boolean = False
    whole_word_search_setting_not_acceptable = True
    while whole_word_search_setting_not_acceptable:
        print('Do you want to search by Whole Word? **Not Used in RegEx Search.**')
        print('Enter \":q\" to quit.')
        whole_word_search_string = input('Search by Whole Word (Y/N): ')
        if whole_word_search_string.lower() == ':q':
            sys.exit()
        elif len(whole_word_search_string) < 4:
            if whole_word_search_string.lower() == ('y' or 'yes'):
                whole_word_search_boolean = True
                whole_word_search_setting_not_acceptable = False
            elif whole_word_search_string.lower() == ('n' or 'no'):
                whole_word_search_boolean = False
                whole_word_search_setting_not_acceptable = False
            else:
                pass
        else:
            print('ERROR: Please enter Yes or No.')
    return whole_word_search_boolean


def search_loaded_records(records_to_search, field_subfield_to_search, search_term_or_terms, search_by_whole_word):
    records_to_save = []
    search_field = ''
    search_subfield = ''
    for pair in field_subfield_to_search:
        search_field = pair[0]
        search_subfield = pair[1]
    for record in records_to_search:
        record_saved = False
        if search_field.lower() == 'ldr':
            try:
                leader_data = str(record.leader)
            except OSError:
                leader_data = ''
            for search_term in search_term_or_terms:
                if (str(search_term) in leader_data) and (record_saved is False):
                    records_to_save.append(record)
                    # Don't need to note the record is saved as we are moving on to the next record already.
                    # record_saved = True
        else:
            for field in record:
                # All fields have tag, except leader. The leader isn't listed in record.fields.
                if hasattr(field, 'tag') and (record_saved is False):
                    if ((str(field.tag) == str(search_field)) or (search_field == '')) \
                            and ((int(field.tag) < 10) and (search_subfield == '')):
                        # print(search_field)
                        # Handle field search for 001-009 fields.
                        try:
                            field_data = str(field.data.decode('utf-8'))
                        except UnicodeDecodeError:
                            field_data = str(pymarc.marc8_to_unicode(field.data))
                        for search_term in search_term_or_terms:
                            if str(search_term) in field_data and record_saved is False:
                                records_to_save.append(record)
                                record_saved = True
                    elif ((str(field.tag) == str(search_field)) or (search_field == '')) \
                            and (int(field.tag) < 10) and (search_subfield != ''):
                        # Skip 001-009, if a subfield is specified. Don't want this caught in the next elif.
                        # print('ERROR: field 001 to 010 shouldn\'t have a subfield specified.')
                        pass
                    elif str(field.tag) == str(search_field):
                        # print(search_field, field.tag)
                        # Handle field search for 010 to 999 where the field matches the given search field.
                        for subfield in field:
                            if (((str(search_subfield) in str(subfield[0])) or (search_subfield == ''))
                                    and (record_saved is False)):
                                try:
                                    subfield_data = str(subfield[1].decode('utf-8'))
                                except UnicodeDecodeError:
                                    subfield_data = str(pymarc.marc8_to_unicode(subfield[1]))
                                for search_term in search_term_or_terms:
                                    if search_by_whole_word is True:
                                        for word in subfield_data.split():
                                            if search_term.isalpha():
                                                bad_characters = '?!\"\':|,.0123456789()\\`~<>/=+-_*&^%$#@'
                                            elif search_term.isalnum():
                                                bad_characters = '?!\"\':|,.()\\`~<>/=+-_*&^%$#@'
                                            else:
                                                bad_characters = ''
                                            search_word = ''
                                            if word.isalnum():
                                                search_word = word
                                            else:
                                                for char in word:
                                                    if char in bad_characters:
                                                        char = ' '
                                                    search_word = search_word + char
                                            for word2 in search_word.split(' '):
                                                if (str(search_term) == word2) and (record_saved is False):
                                                    # print(search_word, field.tag, subfield[0])
                                                    print(subfield_data)
                                                    records_to_save.append(record)
                                                    record_saved = True
                                                else:
                                                    break
                                    else:
                                        if (str(search_term) in subfield_data) and (record_saved is False):
                                            print(subfield_data)
                                            records_to_save.append(record)
                                            record_saved = True
                            else:
                                # Don't save the record.
                                pass
                    elif search_field == '':
                        # Handle field search for 010 to 999 where the field isn't specified.
                        for subfield in field:
                            if (((str(search_subfield) in str(subfield[0])) or (search_subfield == ''))
                                    and (record_saved is False)):
                                try:
                                    subfield_data = str(subfield[1].decode('utf-8'))
                                except UnicodeDecodeError:
                                    subfield_data = str(pymarc.marc8_to_unicode(subfield[1]))
                                for search_term in search_term_or_terms:
                                    if (search_by_whole_word is True) and (record_saved is False):
                                        for word in subfield_data.split():
                                            if record_saved is True:
                                                break
                                            elif search_term.isalpha():
                                                bad_characters = '?!\"\':|,.0123456789()\\`~<>/=+-_*&^%$#@'
                                            elif search_term.isalnum():
                                                bad_characters = '?!\"\':|,.()\\`~<>/=+-_*&^%$#@'
                                            else:
                                                bad_characters = ''
                                            search_word = ''
                                            if word.isalnum():
                                                search_word = word
                                            else:
                                                for char in word:
                                                    if char in bad_characters:
                                                        char = ' '
                                                    search_word = search_word + char
                                            for word2 in search_word.split(' '):
                                                if (str(search_term) == word2) and (record_saved is False):
                                                    # print(search_word, field.tag, subfield[0])
                                                    print(subfield_data)
                                                    records_to_save.append(record)
                                                    record_saved = True
                                                else:
                                                    break
                                    elif record_saved is True:
                                        # Catch search that is whole word and the record has already been saved.
                                        break
                                    else:
                                        # Don't search by whole word.
                                        if (str(search_term) in subfield_data) and (record_saved is False):
                                            print(subfield_data)
                                            records_to_save.append(record)
                                            record_saved = True
                            else:
                                # Don't save the record.
                                pass
    return records_to_save


def reg_ex_search_loaded_records(records_to_search, field_subfield_to_search, search_term_or_terms):
    records_to_save = []
    search_field = ''
    search_subfield = ''
    # Convert list to string for regex search.
    search_term_or_terms = rf'{search_term_or_terms[0]}'
    for pair in field_subfield_to_search:
        search_field = pair[0]
        search_subfield = pair[1]
    for record in records_to_search:
        record_saved = False
        if search_field.lower() == 'ldr':
            try:
                leader_data = str(record.leader)
            except OSError:
                leader_data = ''
            match = re.search(rf'{search_term_or_terms}', leader_data)
            if match and (record_saved is False):
                records_to_save.append(record)
                print(leader_data)
                # Don't need to note the record is saved as we are moving on to the next record already.
                # record_saved = True
        else:
            for field in record:
                # All fields have tag, except leader. The leader isn't listed in record.fields.
                if hasattr(field, 'tag') and (record_saved is False):
                    if ((str(field.tag) == str(search_field)) or (search_field == '')) \
                            and ((int(field.tag) < 10) and (search_subfield == '')):
                        # print(search_field)
                        # Handle field search for 001-009 fields.
                        try:
                            field_data = str(field.data.decode('utf-8'))
                        except UnicodeDecodeError:
                            field_data = str(pymarc.marc8_to_unicode(field.data))
                        match = re.search(rf'{search_term_or_terms}', field_data)
                        if match and record_saved is False:
                            records_to_save.append(record)
                            print(field_data)
                            record_saved = True
                    elif ((str(field.tag) == str(search_field)) or (search_field == '')) \
                            and (int(field.tag) < 10) and (search_subfield != ''):
                        # Skip 001-009, if a subfield is specified. Don't want this caught in the next elif.
                        # print('ERROR: field 001 to 010 shouldn\'t have a subfield specified.')
                        pass
                    elif str(field.tag) == str(search_field):
                        # print(search_field, field.tag)
                        # Handle field search for 010 to 999 where the field matches the given search field.
                        for subfield in field:
                            if (((str(search_subfield) in str(subfield[0])) or (search_subfield == ''))
                                    and (record_saved is False)):
                                try:
                                    subfield_data = str(subfield[1].decode('utf-8'))
                                except UnicodeDecodeError:
                                    subfield_data = str(pymarc.marc8_to_unicode(subfield[1]))
                                if search_subfield != '':
                                    match = re.search(f'{search_term_or_terms}', subfield_data)
                                    # print(match, search_term_or_terms)
                                else:
                                    match = re.search(f'{search_term_or_terms}', str(field))
                                if match and (record_saved is False):
                                    if search_subfield != '':
                                        print(field, subfield_data)
                                    else:
                                        print(field, match.group())
                                    records_to_save.append(record)
                                    record_saved = True
                            else:
                                # Don't save the record.
                                pass
                    elif search_field == '':
                        # Handle field search for 010 to 999 where the field isn't specified.
                        for subfield in field:
                            if (((str(search_subfield) in str(subfield[0])) or (search_subfield == ''))
                                    and (record_saved is False)):
                                try:
                                    subfield_data = str(subfield[1].decode('utf-8'))
                                except UnicodeDecodeError:
                                    subfield_data = str(pymarc.marc8_to_unicode(subfield[1]))
                                match = re.search(rf'{search_term_or_terms}', subfield_data)
                                if match and (record_saved is False):
                                    print(subfield_data)
                                    records_to_save.append(record)
                                    record_saved = True
                            else:
                                # Don't save the record.
                                pass
    return records_to_save


def list_used_fields_and_subfields(records_to_search):
    list_of_fields_and_subfields_used = []
    for record in records_to_search:
        for field in record:
            # All fields have tag, except leader. The leader isn't listed in record.fields.
            if hasattr(field, 'tag'):
                field_tag = str(field.tag)
                subfields = []
                for subfield in field:
                    if str(subfield[0]):
                        subfields.append(subfield[0])
                if subfields:
                    for subfield in subfields:
                        field_subfield = field_tag + subfield
                        if field_subfield in list_of_fields_and_subfields_used:
                            pass
                        else:
                            list_of_fields_and_subfields_used.append(field_subfield)
                else:
                    field = field_tag
                    if field in list_of_fields_and_subfields_used:
                        pass
                    else:
                        list_of_fields_and_subfields_used.append(field)
    return list_of_fields_and_subfields_used


def save_matches_to_file(records_matched):
    # Get name of MARC record file to save.
    marc_file_to_save = ''
    file_name_not_acceptable = True
    while file_name_not_acceptable:
        print('File extension must be \".mrc\" or \".raw\". Extension .mrc assumed, if not supplied.')
        print('Enter \":q\" to quit or \":s\" to skip saving a file.')
        marc_file_to_save = input('MARC record(s) file path: ')
        if marc_file_to_save.lower() == ':q':
            # Break out of loop, if :q entered. What about main running loop? (Bad form? Just call sys.exit() ?)
            # running = False
            # file_name_not_acceptable = False
            sys.exit()
        elif marc_file_to_save == ':s':
            file_name_not_acceptable = False
        else:
            try:
                if marc_file_to_save[-4:] != '.mrc':
                    marc_file_to_save += '.mrc'
                    if glob.glob(marc_file_to_save):
                        print('ERROR: File Already Exists. Enter a new file name.')
                    else:
                        file_name_not_acceptable = False
                elif (marc_file_to_save[-4:].lower() == '.mrc') or (marc_file_to_save[-4:].lower() == '.raw'):
                    if glob.glob(marc_file_to_save):
                        print('ERROR: File Already Exists. Enter a new file name.')
                    else:
                        file_name_not_acceptable = False
                else:
                    pass
            except OSError:
                pass
    # Save matching records in new MARC record file. Skip saving, if command :s was entered.
    if marc_file_to_save == ':s':
        pass
    else:
        save_start_time = datetime.datetime.now()
        try:
            with open(str(marc_file_to_save), 'wb') as fh:
                writer = pymarc.MARCWriter(fh)
                for matching_record in records_matched:
                    writer.write(matching_record)
        except FileNotFoundError:
            pass
        save_end_time = datetime.datetime.now()
        # Print to screen the time it took to save the record file.
        save_time = str(format((save_end_time - save_start_time).total_seconds(), '.2f'))
        print('Time to save record(s): ' + save_time + ' seconds')


records_loaded = []
field_subfields_to_search = []
list_of_search_terms = []
matches_list = []
all_fields_and_subfields_used = []
menu_selection = ''
whole_word_search = False
running = True
# [1]:Load MARC File [2]:Enter Search Field(s) [3]:Enter Search Term(s) [4]:Run Search
# [5]:Save Matched Records to File [9]:Count Records [0]:Quit
while running:
    menu_selection = main_menu()
    if menu_selection == '1':
        records_loaded = load_records()
    elif menu_selection == '2':
        field_subfields_to_search = user_entry_field_subfield()
    elif menu_selection == '3':
        list_of_search_terms = user_entry_search_term_or_terms()
    elif menu_selection == '4':
        print('----------------')
        search_start_time = datetime.datetime.now()
        matches_list = search_loaded_records(records_loaded, field_subfields_to_search, list_of_search_terms,
                                             whole_word_search)
        search_end_time = datetime.datetime.now()
        # Print to screen number of records matched.
        count_of_records_matched = len(matches_list)
        print('----------------')
        print(str(count_of_records_matched) + ' records matched.')
        # Print to screen the time it took to search the records.
        search_time = str(format((search_end_time - search_start_time).total_seconds(), '.2f'))
        print('Time to search record(s): ' + search_time + ' seconds')
        input('Press Enter to Continue')
    elif menu_selection == '5':
        print('----------------')
        search_start_time = datetime.datetime.now()
        matches_list = reg_ex_search_loaded_records(records_loaded, field_subfields_to_search, list_of_search_terms)
        search_end_time = datetime.datetime.now()
        # Print to screen number of records matched.
        count_of_records_matched = len(matches_list)
        print('----------------')
        print(str(count_of_records_matched) + ' records matched.')
        # Print to screen the time it took to search the records.
        search_time = str(format((search_end_time - search_start_time).total_seconds(), '.2f'))
        print('Time to search record(s): ' + search_time + ' seconds')
        input('Press Enter to Continue')
    elif menu_selection == '6':
        count_of_records = len(records_loaded)
        print('Number of Records Loaded: ', count_of_records)
        if matches_list:
            count_of_matched_records = len(matches_list)
            print('Number of Records Matching Search: ', count_of_matched_records)
        input('Press Enter to Continue')
    elif menu_selection == '7':
        print('----------------')
        search_start_time = datetime.datetime.now()
        all_fields_and_subfields_used = list_used_fields_and_subfields(records_loaded)
        search_end_time = datetime.datetime.now()
        print('----------------')
        fields_used = {}
        for item in all_fields_and_subfields_used:
            if len(item) == 3:
                fields_used[f'{item}'] = ''
            else:
                if item[:3] in fields_used.keys():
                    temp_item = fields_used[f'{item[:3]}']
                    temp_item += item[3:]
                    temp_sorted = ''.join(sorted(temp_item, key=str.lower))
                    fields_used[f'{item[:3]}'] = temp_sorted
                else:
                    fields_used[f'{item[:3]}'] = f'{item[3:]}'
        sorted_fields = {}
        for item in sorted(fields_used):
            sorted_fields[item] = fields_used[item]

        print('\"Field\",\"Subfields\"')
        print('\"LDR\",\"\"')
        for key, value in sorted_fields.items():
            print('\"' + key + '\",' + '\"' + value + '\"')

        # Print to screen the time it took to search the records.
        search_time = str(format((search_end_time - search_start_time).total_seconds(), '.2f'))
        print('Time to search record(s): ' + search_time + ' seconds')
        input('Press Enter to Continue')
    elif menu_selection == '8':
        if matches_list:
            save_matches_to_file(matches_list)
        else:
            print('Search returned no matches or You\'ve not run a search, yet.')
            print('**Steps needed to save matching records.**')
            print('Load MARC File')
            print('Enter Search Field(s)')
            print('Enter Search Term(s)')
            print('Run Search OR Run RegEx Search')
            input('Press Enter to Continue')
    elif menu_selection == '9':
        try:
            print('Menu: Enter the number of a menu item to continue.')
            print('[1]:About (Display MIT License)\n'
                  '[2]:Change Whole Word Search Setting\n')
            setting_selector = input('Enter Selection: ')
            invalid_setting_entry = True
            if len(setting_selector) == 1:
                if setting_selector in '1234567890':
                    invalid_setting_entry = False
                else:
                    clear_screen()
                    error_message = 'ERROR: Invalid Entry. Enter matching number of menu entry.'
            if invalid_setting_entry:
                pass
            else:
                if int(setting_selector) == 1:
                    print("MARC Crucible is released under \"The MIT License (MIT)\"\n"
                          "Copyright © 2023 Joseph Alway"
                          "\n\n"
                          "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and\n"
                          "associated documentation files (the \"Software\"), to deal in the Software without restriction,\n"
                          "including without limitation the rights to use, copy, modify, merge, publish, distribute,\n"
                          "sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished\n"
                          "to do so, subject to the following conditions:\n"
                          "The above copyright notice and this permission notice shall be included in all copies or\n"
                          "substantial portions of the Software."
                          "\n\n"
                          "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO\n"
                          "THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS\n"
                          "OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\n"
                          "OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
                    input('Press Enter to Continue')
                    clear_screen()
                else:
                    whole_word_search = user_entry_settings()
        except KeyError:
            pass
    elif menu_selection == '0':
        running = False
        sys.exit()
    else:
        pass
