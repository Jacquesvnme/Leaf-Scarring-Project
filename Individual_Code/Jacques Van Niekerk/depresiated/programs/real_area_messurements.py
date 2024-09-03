hand_l = 13.7
hand_w = 9.1
hand_area = round(hand_w * hand_l, 4)
error_margin =  round(hand_area - object_area, 4)
error_percentage = round(error_margin/hand_area, 4)

print("=========================================")
print("AREA CALCULATION WITH HAND & ANALYSIS\n")
print("Details here focuses on Analysis of the\ndata & gives data measured in real\nworld with hand measurements")
print("-----------------------------------------")
print("Area: " + str(hand_l) + " * " + str(hand_w) +" = " + str(hand_area)  + " cm")
print("Error Margin: " + str(error_margin) + " cm^2")
print("Error %: " + str(error_percentage) + " %") 
print("-----------------------------------------")