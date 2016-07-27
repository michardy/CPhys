from S2mms import spin

program = spin()

with open("test.pys", "r") as f:
    pdata = f.read()

program.run(pdata)
