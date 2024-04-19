function graphs = cable_json_graphs(column_number, title_string, title_substring_1, title_substring_2, x_label_string, y_label_string, y_minimum, y_maximum, legend_position)

arguments
    column_number
    title_string
    title_substring_1
    title_substring_2
    x_label_string
    y_label_string
    y_minimum
    y_maximum
    legend_position = "best"        % optional/default parameter
end

%clear all
close all

% column_number = 3
% title_string = 'Lateral displacement (y) along cable arc length'
% title_substring_1 = "Wave direction: "
% title_substring_2 = "° vs max lateral (y) displacement"
% x_label_string = 'Displacement (m)'
% y_label_string ='Along arc length (m)'
% y_maximum = 5

direction_column_number = 3

% NB xlsread is supposed to be deprecated
%[cable2, cable3, cable4]=xlsread("cable_simulation_results - Copy (2).csv")
[cable2, cable3, cable4]=xlsread("cable_simulation_results.csv")
numA = cell2mat(cable4(2:end,1:4))   % gives 4 numbers columns as columns (missing out header) from xls read
% this is a non-JSON matrix of numbers

legends = []        % initialise legends array

figures = []

numRows = length(numA)

for i = 2: numRows+1    % decode all of the JSON for OF RangeGraph data
    json_array(i-1) = jsondecode(cell2mat(cable4(i,column_number)))
end
% JSON data going into a separate array of structs

%directions = [90, 180, 270, 0]
directions = [45, 135, 225, 315]  % diagonal directions


for i = 1: length(directions)

% use logical indexing to produce a separate figure for each direction
% direction is in column 3 (Hs in 1, T in 2, n in 4)
cable_direction_idx = (numA(:,direction_column_number) == directions(i))  % one direction at a time
numA_filtered = numA(cable_direction_idx,:)         % filter numeric and JSON tables
cable_direction_idx_t = cable_direction_idx'
json_array_filtered = json_array(cable_direction_idx_t) % transpose index to fit

%legend_items = []       % reset/initialise legends array
    hold on
    figures(i) = figure
    t = title(title_string)
    xl = xlabel(x_label_string)
    yl = ylabel(y_label_string)
    ylim([y_minimum y_maximum])

    numRows = length(numA_filtered)
    % FOR USE WHEN FILTERED to ONE DIRECTION WITH LOGICAL INDEX 
    
    legend_strings = {}     % empty cell array to reset

    for j = 1:numRows
        legend_string = strcat("Hs:",string(numA_filtered(j,1)),"(m), Tp:",string(numA_filtered(j,2)),"(s)")
        %legend_string = ["Hs:",string(numA_filtered(j,1)),"(m), Tp:",string(numA_filtered(j,2)),"(s)"]
        legend_strings{j} = strcat("",legend_string)    % in case the above is blank
        plot_points = []    % reset/initialise array of data points
    % https://uk.mathworks.com/matlabcentral/answers/341454-how-to-loop-over-the-structure-fields-and-get-the-type-of-data#answer_268006
    % i don't know if this is the optimal way, but...

    
        % fn = fieldnames(json_array(j).x0); % need to loop over all rows not just row 12
        % for k=1:numel(fn)
        %     if( isnumeric(json_array(j).x0.(fn{k})) )
        %         json_array(j).x0.(fn{k})% do stuff - just print value
        %         plot_points(end + 1) = json_array(j).x0.(fn{k})
        %     end
        % end

        fn = fieldnames(json_array_filtered(j).x0); % need to loop over all rows not just row 12
        for k=1:numel(fn)
            if( isnumeric(json_array_filtered(j).x0.(fn{k})) )
                json_array_filtered(j).x0.(fn{k})% do stuff - just print value
                plot_points(end + 1) = json_array_filtered(j).x0.(fn{k})
            end
        end


        line_segment = 1.0
        x_values = linspace (0,line_segment * (length(plot_points) -1), length(plot_points))    % the lengths of the segments
        hold on
        plot(x_values, plot_points)
        
        %legappend(legend_string)

    end     % for each direction
    title_string = title_substring_1 + string(directions(i) + title_substring_2)
    %%%%title(title_string)
    % NB - removing title for thesis style reasons!
    title('')   % blank title on plot (no duplicate titles) (for thesis style reasons!)
    if length(legend_strings) == 0
        legend_strings{1} = ""      % blank string if otherwise empty legend
    end
    legend(legend_strings, 'Location', legend_position)    
    hold off
    grid on
    title_string = strrep(title_string, ":","")     % remove colon (path symbol) from filename
    title_string = strrep(title_string, "°","")
    saveas(figures(i), title_string + ".png")
end

graphs = figures
