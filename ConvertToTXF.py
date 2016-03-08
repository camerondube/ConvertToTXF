#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import csv
import datetime
from textwrap import dedent

def ConvertCSVToTXF():
    """
    Input: ./GainLossDetail.csv dl'd from Merrill Lynch Benefits site
    Output: ./1099-B.txf
    TXF specifications: https://turbotax.intuit.com/txf/TXF042.jsp
    This uses the "Record Format 5" in the above specs
    """
    extraction_date = datetime.date.today()
    output = "V042\nACameronDube\nD{extraction_date}\n^\n\n".format(extraction_date=extraction_date.strftime("%d/%m/%Y"))
    with open('GainLossDetail.csv', 'r') as input_file:
        reader = csv.DictReader(input_file, delimiter=',')
        for row in reader:
            security = row['Description of Property']
            date_acquired = row['Date of Acquisition']
            date_sold = row['Date of Sale or Exchange']
            cost_basis = row['Cost Basis']
            sales_net = row['Sales Price (see Schedule D instructions)']
            irs_code = row['IRS Code']
            disallowed_wash = row['Adjustments to Gain or Loss'] if irs_code == "W" else ""
            output += dedent('''\
            P{security}
            D{date_acquired}
            D{date_sold}
            ${cost_basis}
            ${sales_net}
            ${disallowed_wash}
            ^\n
            '''.format(security=security, date_acquired=date_acquired, date_sold=date_sold, cost_basis=cost_basis, sales_net=sales_net, disallowed_wash=disallowed_wash))
    input_file.closed
    with open('1099-B.txf', 'w') as output_file:
        output_file.write(output)
    output_file.closed


if __name__ == "__main__":
    ConvertCSVToTXF()
