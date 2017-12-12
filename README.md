# Conference_Paper_Download

下载会议论文的题目、作者、摘要等信息，生成tex文件，以生成一个pdf文件。

## Usage example
- `cd ICML`
- `python get_data.py` will generate a json file.
- `python ../generate_tex.py paper.json paper.tex "ICML Accepted Papers"` will generate a tex file.
- `xelatex paper.tex` twice will generate a pdf file.