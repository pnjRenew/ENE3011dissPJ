
clear all
close all


input_column_number = 5
input_title_string = 'Lateral displacement (y) along cable arc length'
input_title_substring_1 = "Wave direction: "    
input_title_substring_2 = "° vs max lateral (y) displacement"
input_y_label_string = 'Displacement (m)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = 0
input_y_maximum = 5

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum)

input_column_number = 6
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max Axial stress (kN)"
input_y_label_string = 'Axial stress (kN)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = 0
input_y_maximum = 20000      

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum)

input_column_number = 7
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max bend moment (kNm)"
input_y_label_string = 'Bend moment (kNm)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = 0
input_y_maximum = 2 

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum)

input_column_number = 8
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max tension (N)"
input_y_label_string = 'Tension (N)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = 0
input_y_maximum = 10

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum)

input_column_number = 9
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max curvature (rad)"
input_x_label_string = 'Along arc length (m)'
input_y_label_string ='Curvature (rad)'
input_y_minimum = 0
input_y_maximum = 1

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum)
    