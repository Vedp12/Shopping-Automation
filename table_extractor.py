import camelot

tables = camelot.read_pdf("Computer_Networks.pdf", pages="1")
print(tables)

tables.export("Computer_Networks.csv", f="csv", compress=True)
tables[0].to_csv("Computer_Networks.csv")
