class HTMLout:
    def StartHTML(self):
        self.file = open("out3/output2.html", 'w+')
        self.file.write('''<!DOCTYPE html>
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t<title>AICA Output</title>
\t<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
\t<style>
\t\tbody {
\t\t\tfont-family: 'Roboto', sans-serif;
\t\t}
\t\tp {
\t\t\tfont-weight: 700;
\t\t}
\t</style>
</head>
<body>''')

    def EndHTML(self):
        self.file.write('''</body>
</html>''')
        self.file.close()

    def AddToHTML(self, i, numSims, info):
        self.file.write("\t<h1>Experiment {0}</h1>".format(i))
        for j in range(0, numSims):
            self.file.write("\t<img src='exp{0}/run{1}.png' height=120 width=120 border=1>\n".format(i, j))
        self.file.write("\t<p>J1 = {0}, J2 = {1} || h = {2} || R1 = {3}, R2 = {4}</p>".format(info.J1, info.J2, info.h, info.R1, info.R2))
