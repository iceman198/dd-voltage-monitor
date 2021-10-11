R1 = 30000.0;
R2 = 7500.0;
value = 545;
vOUT = (value * 5.0) / 1024.0;
vIN = vOUT / (R2/(R1+R2));
print(vIN);