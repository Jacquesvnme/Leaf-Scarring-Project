inputData1_r = 18.24
inputData2_r = 93.10
inputData3_r = 126.04
inputData4_r = 170.97

inputData1_p = 21.0184 
inputData2_p = 87.817
inputData3_p = 116.8905
inputData4_p = 157.8042

data1_percenatage = round(100 -  (inputData1_p/inputData1_r)*100,4)
data2_percenatage = round(100 -  (inputData2_p/inputData2_r)*100,4)
data3_percenatage = round(100 -  (inputData3_p/inputData3_r)*100,4)
data4_percenatage = round(100 -  (inputData4_p/inputData4_r)*100,4)

def printData(percentage):
    print(percentage)

printData(data1_percenatage)
printData(data2_percenatage)
printData(data3_percenatage)
printData(data4_percenatage)