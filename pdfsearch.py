import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os


def parse(path, keyword):
    with open(path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        res_man = PDFResourceManager()
        lp = LAParams()
        device = PDFPageAggregator(res_man, laparams=lp)
        interpreter = PDFPageInterpreter(res_man, device)

        index = 0
        result = []
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            index += 1
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    text = x.get_text()
                    if text.__contains__(keyword):
                        result.append(index)
    result = list(set(result))
    result = sorted(result)
    return result


def file_name(file_dir):
    files = []
    for file in os.walk(file_dir):
        files.append(file)   # os.walk()所在目录的所有非目录文件名
    return files


if __name__ == '__main__':
    with open('./search.log', 'w') as f:
        for i in file_name('./556')[0][2]:
            log = parse('./556/'+i, 'KEAP1')
            if log:
                for j in log:
                    f.write(i+' '+str(j)+'\n')
