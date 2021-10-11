value = 552;

R1 = 27730.0;
R2 = 7463.0;

vOUT = (value * 5.0) / 1024.0;
vIN = vOUT / (R2/(R1+R2));
print(vIN);


value = 553;

vOUT = (value * 5.0) / 1024.0;
vIN = vOUT / (R2/(R1+R2));
print(vIN);