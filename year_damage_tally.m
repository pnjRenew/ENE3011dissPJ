%{
year_damage_tally.m
Peter Jenkin 2024
Produces a monthly sum throughout a year of damage readings (in csv)
and graphs this, for both D Beier and P Thies calcs
%}

% track readings through the year and compare for this scenario's damage
% readings
clear all
close all


% read in the big CSV file with datetime, Hs, tm02 and direction
buoy_data_table = readtable("../../diss-data/Race-Bank/2017-Race-Bank.csv");

% read in this folder's damage tables with Hs, T and direction
damage_table_dbeier = readtable("damage_results_copper_dbeier.csv");
damage_table_pthies = readtable("damage_results_copper_pthies.csv");

% damage_dbeier(1) = 0;
damage_dbeier_cumulative(1) = 0;
% damage_pthies(1) = 0;
damage_pthies_cumulative(1) = 0;

error_count_dbeier = 0;
error_count_pthies = 0;


% for each buoy record
% get the rounding to half-metre of each Hs and the half-second of each tm02
% find the medial quadrant of each direction
for i = 1: height(buoy_data_table)
    Hs_binned = (ceil(buoy_data_table.hm0(i)) + floor(buoy_data_table.hm0(i))) / 2;
    tm02_binned = (ceil(buoy_data_table.tm02(i)) + floor(buoy_data_table.tm02(i))) / 2;
    if buoy_data_table.mdir(i) > 0 & buoy_data_table.mdir(i) <= 90
        mdir_binned = 45;
    elseif buoy_data_table.mdir(i) > 90 & buoy_data_table.mdir(i) <= 180
        mdir_binned = 135;
    elseif buoy_data_table.mdir(i) > 180 & buoy_data_table.mdir(i) <= 270
        mdir_binned = 225;
    elseif buoy_data_table.mdir(i) > 270 & buoy_data_table.mdir(i) <= 360
        mdir_binned = 315;
    end
    
    idx = damage_table_dbeier.Hs_sim == Hs_binned & damage_table_dbeier.T_sim ...
        == tm02_binned & damage_table_dbeier.dir_sim == mdir_binned;

    try
        damage_dbeier(i) = damage_table_dbeier(idx,:).damage_copper_dbeier;
    catch some_error
        damage_dbeier(i) = 0;
        strcat(some_error.identifier,' at ', string(i))   % console out the error and location
        error_count_dbeier = error_count_dbeier + 1;
    end

    idx = damage_table_pthies.Hs_sim == Hs_binned & damage_table_pthies.T_sim ...
        == tm02_binned & damage_table_pthies.dir_sim == mdir_binned;

    try
        damage_pthies(i) = damage_table_pthies(idx,:).damage_copper_pthies;
    catch some_error
        damage_pthies(i) = 0;
        strcat(some_error.identifier,' at ', string(i))   % console out the error and location
        error_count_pthies = error_count_pthies + 1;
    end

    
    if i > 1
        % existing_damage = damage_dbeier_cumulative(i-1)
        damage_dbeier_cumulative(i) = damage_dbeier_cumulative(i-1) + damage_dbeier(i);
        damage_pthies_cumulative(i) = damage_pthies_cumulative(i-1) + damage_pthies(i);
    else
        damage_dbeier_cumulative(i) = damage_dbeier(i);
        damage_pthies_cumulative(i) = damage_pthies(i);        
    end

    

end
error_count_pthies;
error_count_pthies;
% need to transpose arrays to fit in a table column

damage_dbeier = damage_dbeier';
damage_pthies = damage_pthies';
damage_dbeier_cumulative = damage_dbeier_cumulative';
damage_pthies_cumulative = damage_pthies_cumulative';


annual_damage_table = table(buoy_data_table.LoggerDateTime, damage_dbeier, damage_pthies, ...
    damage_dbeier_cumulative, damage_pthies_cumulative);

fig1 = figure;
plot(damage_dbeier)
fig2 = figure;
plot(damage_pthies)
fig3 = figure;
plot(damage_dbeier_cumulative)
fig4 = figure;
plot(damage_pthies_cumulative)


writetable(annual_damage_table,'annual_damage.csv');


  TT = timetable(buoy_data_table.LoggerDateTime, damage_dbeier, ...
    damage_pthies, damage_dbeier_cumulative, ...
    damage_pthies_cumulative);

TT = renamevars(TT,["Var1", "Var2", "Var3", "Var4"],["damage_dbeier",...
    "damage_pthies","damage_dbeier_cumulative",...
    "damage_pthies_cumulative"]);

G_dbeier = groupsummary (TT, "Time", "month","sum","damage_dbeier");
G_pthies = groupsummary (TT, "Time", "month","sum","damage_pthies");



fig5  = figure;

hold on
plot(G_dbeier.month_Time,G_dbeier.sum_damage_dbeier, 'Linewidth',4, 'DisplayName', "D Beier calc");
plot(G_pthies.month_Time,G_pthies.sum_damage_pthies, 'Linewidth',4, 'DisplayName', "P Thies calc");

lgd = legend;