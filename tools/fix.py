import openpyxl,re,sys
f=sys.argv[1]; wb=openpyxl.load_workbook(f)
for t in wb.sheetnames[2:-1]:
    ws=wb[t]; H={str(ws.cell(3,c).value).split('\n')[0]:c for c in range(1,ws.max_column+1)}
    for r in range(9,120):
        v=ws.cell(r,2).value
        if not v: continue
        sku=ws.cell(r,H['SKU']).value
        n=re.sub(r',\s*-\s*',' ',v); n=re.sub(r'\s+-\s+Max',' Max',n); n=re.sub(r'[,\s]+$','',n); n=re.sub(r'\s+Corpo$','',n); n=re.sub(r'\s{2,}',' ',n)
        if sku=='PROD-2591': n='Luminária LED Mini Embutido Parede Solo 1W 3000K IP67 Branco'
        if sku=='PROD-2594': n='Luminária LED Mini Embutido Parede Solo 1W 3000K Quadrado'
        ws.cell(r,2).value=n
wb.save(f)
