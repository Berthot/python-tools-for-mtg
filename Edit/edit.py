file = open('edit.txt', 'r').read().split('\n')
result = open('result.txt', 'w')
for line in file:
    text = ''
    if '[' in line:
        text = line.split('[')[0].strip()
    else:
        text = line
    result.write(text + '\n')
