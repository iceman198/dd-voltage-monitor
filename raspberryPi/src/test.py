R1 = 27730.0;
R2 = 7463.0;

value = 552; # should be 12.7
value = 558; # should be 12.83
value = 566; # should be 13.02
vOUT = (value * 5.0) / 1024.0;
vIN = vOUT / (R2/(R1+R2));
print('try one: ' + str(vIN));


value = 553;
vOUT = (value * 5.0) / 1024.0;
vIN = vOUT / (R2/(R1+R2));
print('try two: ' + str(vIN));


v = 553;
v2 = v / 12.0;
v3 = v2 / 1024;
print('try three: ' + str(v3));


newV = (2.5 - (v * (12.0 / 1024.0)) )/0.185;
print('try four: ' + str(newV));