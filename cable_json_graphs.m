function graphs = cable_json_graphs(column_number, title_string, title_substring_1, title_substring_2, ...
    x_label_string, y_label_string, y_minimum, y_maximum, legend_position)
%{
cable_json_graphs.m
Peter Jenkin 2024
Function to produce a number of graphs depicting aspects of cable line
results from OrcaFlex, for use in fatigue damage estimate batch simulation.
Reads JSON data from a cell of a CSV file, for a parameter, and then
draws, and saves, graphs by direction for the parameter over the line's length.
Used by cable_data_graphs_run.m
    column_number : parameter's column number in CSV data file
    title_string : title string to use
    title_substring_1 : first part of title string to use
    title_substring_2 : second  "      "
    x_label_string : x axis label
    y_label_string :  axis label
    y_minimum : y axis minimum values
    y_maximum : y axis maximum values
    legend_position = "best"        % optional/default parameter
%}


%TODO: print max, min, mean, st dev value in text?
%TODO: look for Hs as in strcat("Hs:",string(numA_filtered(j,1)) and
% compile array of Hs group #s, then plot(x_values, plot_points) with a
% symbol according to that number?

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

close all


direction_column_number = 3
Hs_column_number = 1
Tz_column_number = 2

% NB xlsread is supposed to be deprecated
data_filename = "cable_simulation_results.csv"
[~, ~, cable4]=xlsread(data_filename)
numA = cell2mat(cable4(2:end,1:4))   % gives 4 numbers columns as columns (missing out header) from xlsread
% this is a non-JSON matrix of numbers

legends = []        % initialise legends array

figures = []

numRows = length(numA)

for i = 2: numRows+1    % decode all of the JSON for OF RangeGraph data
    json_array(i-1) = jsondecode(cell2mat(cable4(i,column_number)))
end
% JSON data going into a separate array of structs

directions = [45, 135, 225, 315]  % diagonal directions

records_row_counter = 1

line_symbol_strings = ['-' 'o' '*' 'x' '+' '-' 'o' '*']
line_colour_strings = ['m' 'y' 'r' 'g' 'b' 'c'  'k' 'r' 'g' 'b']


for i = 1: length(directions)

% use logical indexing to produce a separate figure for each direction
% direction is in column 3 (Hs in 1, T in 2, n in 4)
cable_direction_idx = (numA(:,direction_column_number) == directions(i));  % one direction at a time
numA_filtered = numA(cable_direction_idx,:);         % filter numeric and JSON tables by direction
cable_direction_idx_t = cable_direction_idx';
json_array_filtered = json_array(cable_direction_idx_t); % transpose index to fit
[numA_filtered, Hs_sort_idx] = sortrows(numA_filtered,[1 2]);  % sort by Hs then Tz
json_array_filtered = json_array_filtered(Hs_sort_idx);  % sort JSON also with logical indexing (head hurts)
Hs_values = unique(numA_filtered(:,Hs_column_number));  % could find column by config instead of hard-code
Tz_values = unique(numA_filtered(:,Tz_column_number))

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
        legend_string = strcat("Hs:",string(numA_filtered(j,1)),"(m), Tz:",string(numA_filtered(j,2)),"(s)")
        legend_strings{j} = strcat("",legend_string)    % in case the above is blank
        plot_points = []    % reset/initialise array of data points
    % https://uk.mathworks.com/matlabcentral/answers/341454-how-to-loop-over-the-structure-fields
    % -and-get-the-type-of-data#answer_268006
    % i don't know if this is the optimal way, but...
    
        fn = fieldnames(json_array_filtered(j).x0); % need to loop over all rows not just row 12
        for k=1:numel(fn)
            if( isnumeric(json_array_filtered(j).x0.(fn{k})) )
                json_array_filtered(j).x0.(fn{k})% do stuff - just print value
                plot_points(end + 1) = json_array_filtered(j).x0.(fn{k})
            end
        end

        % record each (and each direction) 
        % row's stats (max &c along arc length for
        % that sim for that Hs & Tz)
        % for output to file for this parameter
        % at end of run
        idx_dir_and_row = ((i-1) * numRows) + j     % e.g. direction 1 row 2 = 2,...
        Hs_recorded(records_row_counter, 1) = numA_filtered(j,1)
        Tz_recorded(records_row_counter, 1) = numA_filtered(j,2)
        direction_recorded(records_row_counter, 1) = directions(i)
        min_recorded(records_row_counter, 1) = min(plot_points)
        max_recorded(records_row_counter, 1) = max(plot_points)
        mean_recorded(records_row_counter, 1) = mean(plot_points)
        st_dev_recorded(records_row_counter, 1) = std(plot_points)
        records_row_counter = records_row_counter + 1

        line_segment = 1.0
        x_values = linspace (0,line_segment * (length(plot_points) -1), length(plot_points))    
        % the lengths of the cable segments
        hold on

        

        % get the string for this line's Hs group
        line_symbol_string = line_symbol_strings(find(Hs_values == numA_filtered(j,1))); 
        % col 1 for Hs, 2 for Tz
        line_colour_string = line_colour_strings(find(Tz_values == numA_filtered(j,2)))
        line_format_string = strcat(line_symbol_string, line_colour_string)
        
        plot(x_values, plot_points, line_format_string)

        % for each direction, need to sort that direction's data by Hs, Tz
        % THEN plot each of the points

    end     % for each direction
    title_string = title_substring_1 + string(directions(i) + title_substring_2)
    % NB - removing title for thesis style reasons!
    title('')   % blank title on plot (no duplicate titles) (for thesis style reasons!)
    if length(legend_strings) == 0
        legend_strings{1} = ""      % blank string if otherwise empty legend
    end
    legend(legend_strings, 'Location', legend_position)    
    hold off
    grid on
    % (TODO: put in function)
    title_string = strrep(title_string, ":","")     % remove colon (path symbol) from filename
    title_string = strrep(title_string, "°","")     % remove anything else non filepath-y
    title_string = strrep(title_string, "/","")     % remove anything else non filepath-y
    title_string = strrep(title_string, "\","")     % remove anything else non filepath-y
    title_string = strrep(title_string, ":","")     % remove anything else non filepath-y
    saveas(figures(i), title_string + ".png")
end

graphs = figures


% compile a table from the processing's arrays
output_table_unfiltered =  table(Hs_recorded, Tz_recorded, direction_recorded , min_recorded, ...
    max_recorded, mean_recorded, st_dev_recorded);
idx_filter = (output_table_unfiltered.Hs_recorded > 0) & (output_table_unfiltered.Tz_recorded > 0);  
% remove any zero rows (not sure how they're there)
output_table = output_table_unfiltered(idx_filter, :);

output_table = sortrows(output_table,{'Hs_recorded','Tz_recorded'},{'ascend','ascend'}) % order by Hs then Tz

% maybe filter also by present direction
% filter out Tz = 0
close all
fig = figure

% (TODO: put in function)
% name the output CSV file after the whole parameter
table_save_filename_string = y_label_string         
table_save_filename_string = strrep(table_save_filename_string, ":","")     
% remove colon (path symbol) from filename
table_save_filename_string = strrep(table_save_filename_string, "°","")     
% remove anything else non filepath-y
table_save_filename_string = strrep(table_save_filename_string, "/","")     
% remove anything else non filepath-y
table_save_filename_string = strrep(table_save_filename_string, "\","")     
% remove anything else non filepath-y
table_save_filename_string = strrep(table_save_filename_string, ":","")     
% remove anything else non filepath-y
writetable(output_table,table_save_filename_string + ".csv")

% Hs vs parameter, grouped by Tz
gscatter(output_table.Hs_recorded,output_table.max_recorded,output_table.Tz_recorded)
ylabel(y_label_string)
xlabel('Hs (m)')
grid on
xlim([0 inf])
ylim([0 inf])
lgd = legend
lgd.Title.String = "Tz (m)"

saveas(fig, table_save_filename_string + '-Hs-max.png')


% Tz vs parameter, grouped by Hs
gscatter(output_table.Tz_recorded,output_table.max_recorded,output_table.Hs_recorded)
ylabel(y_label_string)
xlabel("Tz (m)")
grid on
xlim([0 inf])
ylim([0 inf])
lgd = legend
lgd.Title.String = 'Hs (m)'

saveas(fig, table_save_filename_string + '-Tz-max.png')