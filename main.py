import os

def handleUserInput():
    file_name = input("Convert file or \"all\": ")
    # file_name = "test.py"
    if file_name == "all":
        for f_name in os.listdir("./"):
            if f_name.endswith(".py") and not f_name == "main.py":
                convert_file(f_name);
    else:
        convert_file(file_name)
    print("Done!")

def convert_file(file_name):
    # Sketchily remove file ending, unsafe
    file_name_noext = file_name[:-len(".py")]
    
    file_text = read_file(file_name)
    out_text = convert(file_text)
    write_file(file_name_noext + ".ipynb", out_text)
    print("Converted " + file_name)

def read_file(file_name):
    with open("./" + file_name, encoding="utf8") as f:
        return f.read()

def write_file(file_name, file_string):
    with open("./" + file_name, 'w', encoding="utf8") as f:
        f.write(file_string) 

comment_cell = "{{\"cell_type\": \"markdown\",\"metadata\": {{}},\"source\": {0} }}"
code_cell = "{{\"cell_type\": \"code\",\"execution_count\":{0},\"metadata\": {{ \"collapsed\": false}},\"outputs\": [],\"source\":[{1}]}}"
string_format_str = "\"{0}\"";

whole_file_format = "{{\n\"cells\": [\n{0}],\"metadata\":{{\"kernelspec\":{{\"display_name\":\"Python 3\",\"language\":\"python\",\"name\":\"python3\"}},\"language_info\":{{\"codemirror_mode\":{{\"name\":\"ipython\",\"version\":3}},\"file_extension\":\".py\",\"mimetype\":\"text/x-python\",\"name\":\"python\",\"nbconvert_exporter\":\"python\",\"pygments_lexer\":\"ipython3\",\"version\":\"{1}\"}}}},\"nbformat\":4,\"nbformat_minor\":0}}"

PYTHON_VERSION="3.7.3"

def convert(text):
    text = text.strip()
    cell_entries = []
    charactersToReplace = ["\n", "\r"]
    in_code = False;
    code_accum = []
    execution_count=0
    for line in text.splitlines():
        for c in charactersToReplace:
            line = line.replace(c, "")
        line = line.replace("\"","\\\"")
        # line = line.strip()
        if len(line) == 0:
            continue;
        if line[0] == "#":
            if in_code:
                code_string = "\\n\",\n\"".join(code_accum)
                code_accum = []
                in_code = False;
                cell_entries.append(code_cell.format(execution_count, string_format_str.format(code_string)))
                execution_count += 1;
            if line.startswith("# In["):
                if line[5] == " ": # MAN this code is so hackish
                    continue;
                execution_count=int(line[5:-2]) # Seriously mate learn some regex please
            else:
                cell_entries.append(comment_cell.format(string_format_str.format(line[2:])))
        else:
            in_code = True;
            code_accum.append(line);

    if in_code:
        code_string = "\n,".join(code_accum)
        code_accum = []
        in_code = False;
        cell_entries.append(code_cell.format(execution_count, code_string))

    return whole_file_format.format(",\n".join(cell_entries), PYTHON_VERSION)

if __name__ == "__main__": 
    handleUserInput()