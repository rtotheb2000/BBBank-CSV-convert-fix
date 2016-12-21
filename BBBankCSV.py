import os
import sys
import glob
import codecs

import chardet
import click

try:
    from tqdm import tqdm
except ImportError:
    tqdm = list


def process_filelist(filelist):
    for file in tqdm(filelist):
        # guess encoding of file
        dict_encoding = chardet.detect(open(file, 'rb').read())
        encoding = dict_encoding.get('encoding', None)
        # open file with right encoding
        with open(file, 'r', encoding=encoding) as f:
            content = f.readlines()
        # strip the header of the file
        ColumnsEncountered = False
        for num, line in enumerate(content):
            if line.find('"Buchungstag";"Valuta";') != -1 and not ColumnsEncountered:
                ColLineNum = num
                ColumnsEncountered = True
        if ColumnsEncountered == False:
            raise ValueError('No column line was encountered reading ' + file + '.')
        contentWOheader = content[ColLineNum:]
        # get the next line that only contains a linebreak
        EndEncountered = False
        for num, line in enumerate(contentWOheader):
            if line == '\n' and not EndEncountered:
                EndLineNum = num
                EndEncountered = True
        if not EndEncountered:
            raise ValueError('End could not be encountered in ' + file + '.')
        contentWOtail = contentWOheader[:EndLineNum]

        lineNumbersWithProperEnding = []
        for num, line in enumerate(contentWOtail):
            if ';"S"' in line or ';"H"' in line:
                lineNumbersWithProperEnding.append(num)
        # fix content to only one line per entry
        fixedcontent = []
        for num, lineNumber in enumerate(lineNumbersWithProperEnding):
            if num == 0:
                previousProperLineNum = 0
            aSingleLine = ''
            for i in range(previousProperLineNum, lineNumber):
                # strip the ending linebreak
                notASingleLine = contentWOtail[i+1].strip('\n')
                aSingleLine += notASingleLine
                if i < lineNumber:
                    aSingleLine += ' '
            # set current num as prevNum
            previousProperLineNum = lineNumber
            # check if there are exactly 12 instances of the seperator ';' in each line
            if aSingleLine.count(';') != 12:
                raise ValueError('A line did not have exactly 12 instances of \';\'')
            # add a single linebreak at the end of a complete line
            aSingleLine += '\n'
            # append complete single lines to fixedcontent
            fixedcontent.append(aSingleLine)
        # put column names in first line again if you want (optional)
        PRINTCOLUMNNAMES = True
        if PRINTCOLUMNNAMES:
            fixedcontent = [content[ColLineNum]] + fixedcontent
        # set output file name
        outfile = ''
        for i, substring in enumerate(file.split('.')[:-1]):
            outfile += substring
            if i < len(file.split('.')[:-1])-1:
                outfile += '.'
        outfile += '_fixed.'+file.split('.')[-1]
        with open(outfile, 'w', encoding='utf-8') as fout:
            fout.writelines(fixedcontent)

@click.command()
@click.option("--pattern", default="", help="glob patter")
@click.option("--file", default="", help="file", multiple=True)
def main(file, pattern):

    filelist = glob.glob(pattern) if pattern else []
    filelist.extend(file)

    process_filelist(filelist)


if __name__ == "__main__":
    main()
