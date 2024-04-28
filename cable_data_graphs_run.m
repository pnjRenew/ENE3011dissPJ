%{
cable_data_graphs_run.m
Peter Jenkin 2024
Batch graph production script for cable fatigue damage estimation.
Uses cable_json_graphs.m
%}

clear all
close all

% TODO All the below would be better read in from a config file

input_column_number = 5
input_title_string = 'Lateral displacement (y) along cable arc length'
input_title_substring_1 = "Wave direction: "    
input_title_substring_2 = "° vs max lateral (y) displacement"
input_y_label_string = 'Displacement (m)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = 0
input_y_maximum = 1
legend_position = 'eastoutside'

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, ...
    input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum, legend_position)

input_column_number = 6
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max Axial stress (kN)"
input_y_label_string = 'Axial stress (kN)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = -3000
input_y_maximum = 3000
legend_position = 'eastoutside'

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2,...
    input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum, legend_position)

input_column_number = 7
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max bend moment (kNm)"
input_y_label_string = 'Bend moment (kNm)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = 0
input_y_maximum = 0.5 
legend_position = 'eastoutside'

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, ...
    input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum,legend_position)

input_column_number = 8
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max tension (N)"
input_y_label_string = 'Tension (N)'
input_x_label_string ='Along arc length (m)'
input_y_minimum = -3
input_y_maximum = 0.5
legend_position = 'eastoutside'

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, ...
    input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum, legend_position)

input_column_number = 9
input_title_string = 'x'
input_title_substring_1 = "Wave direction: "
input_title_substring_2 = "° vs max curvature (rad)"
input_x_label_string = 'Along arc length (m)'
input_y_label_string ='Curvature (1/m)'
input_y_minimum = 0
input_y_maximum = 0.2
legend_position = 'eastoutside'

cable_json_graphs(input_column_number, input_title_string, input_title_substring_1, input_title_substring_2, ...
    input_x_label_string, input_y_label_string, input_y_minimum, input_y_maximum, legend_position)
    
