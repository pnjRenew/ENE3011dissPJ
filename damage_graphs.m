%{
damage_graphs.py
Peter Jenkin 2024
Produces and saves a variety of graphs from a csv output of 
fatigue damage from OrcaFlex cable simulations, for both D Beier
and P Thies calcs.
Don't really need textfit (cf web), could probably remove.
%}

clear all
close all

filename_p_thies_damage = 'damage_results_copper_pthies.csv';
filename_d_beier_damage = 'damage_results_copper_dbeier.csv';

pthies_damage = readtable(filename_p_thies_damage);
dbeier_damage = readtable(filename_d_beier_damage);
directions = [45 135 225 315] % diagonal directions

% TODO: could find axis limits instead of hard-coded

figure1 = figure
% for each of the directions
for i = 1:length(directions)    
    plot(pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   
    % filter damage by direction    
    xlim([0 inf])
    ylim([0 inf])
    grid on
    title('Damage (individual) plot for direction: ' + string(directions(i)) + '°')
    saveas(figure1,'damage_plot_pthies'+ string(directions(i))+'.png')
end

figure1 = figure
% for each of the directions
for i = 1:length(directions)    
    
    plot(dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   
    % filter damage by direction        
    xlim([0 inf])
    ylim([0 inf])
    grid on
    title('Damage (individual) plot for direction: ' + string(directions(i)) + '°')
    saveas(figure1,'damage_plot_dbeier'+ string(directions(i))+'.png')
end

figure2 = figure

for i = 1:length(directions)        
    scatter(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)) ...
        ,'o', 'LineWidth',2);   % filter damage by direction        
    xlabel('Hs (m)')
    ylabel('Damage (individual)')
    xlim([0 4])
    ylim([0 1.5e-5])
    grid on
    textfit(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, ...
        pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)), ...
        string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))))
    saveas(figure2,'damage_scatter_Hs_pthies'+ string(directions(i))+'.png')
end

for i = 1:length(directions)        
    scatter(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)), ...
        dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)), ...
        'o', 'LineWidth',2);   % filter damage by direction        
    xlabel('Hs (m)')
    ylabel('Damage (individual)')
    grid on
    saveas(figure2,'damage_scatter_Hs_dbeier'+ string(directions(i))+'.png')
end

figure3 = figure

for i = 1:length(directions)        
    gscatter(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)),'brgk');
    xlabel('Tz (s)')    
    ylabel('Damage (individual)')
    lgd = legend
    lgd.Title.String = "Hs (m)"
    xlim([0 7.5])
    ylim([0 1.5e-5])    
    grid on
    saveas(figure3,'damage_scatter_Tz_pthies'+ string(directions(i))+'.png')
end

for i = 1:length(directions)    
    gscatter(dbeier_damage.T_sim(pthies_damage.dir_sim == directions(i)), ...
        dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)), ...
        dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)),'brgk');
    xlabel('Tz (s)')    
    ylabel('Damage (individual)')
    lgd = legend
    lgd.Title.String = "Hs (m)"    
    xlim([0 7.5])
    ylim([0 1.5e-5])    
    grid on
    saveas(figure3,'damage_scatter_Tz_dbeier'+ string(directions(i))+'.png')
end

figure4 = figure

for i = 1:length(directions)        
    plot3(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)));
    xlabel('Hs (m)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)') 
    title('Damage (individual) 3D plot for direction: ' + string(directions(i)) + '°')
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    saveas(figure4, 'damage3d_plot_pthies'+ string(directions(i))+'.png')
end

for i = 1:length(directions)        
    plot3(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)), ...
        dbeier_damage.T_sim(dbeier_damage.dir_sim == directions(i)), ...
        dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)));
    xlabel('Hs (m)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)') 
    title('Damage (individual) 3D plot for direction: ' + string(directions(i)) + '°')
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    saveas(figure4, 'damage3d_plot_dbeier'+ string(directions(i))+'.png')
end

figure5 = figure

for i = 1:length(directions)            
    scatter3(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), ...
        pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),...
        'LineWidth',2);
    xlabel('Hs (m)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)')
    title('Damage (individual) 3D scatter for direction: ' + string(directions(i)) + '°')       
    xlim([0 4])
    ylim([0 7.5])
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    saveas(figure5, 'damagescatter3d_plot_pthies'+ string(directions(i))+'.png')
end

for i = 1:length(directions)            
    scatter3(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)), ...
        dbeier_damage.T_sim(dbeier_damage.dir_sim == directions(i)), ...
        dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)), ...
        'LineWidth',2);
    xlabel('Hs (m)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)')
    title('Damage (individual) 3D scatter for direction: ' + string(directions(i)) + '°')
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    saveas(figure5, 'damagescatter3d_plot_dbeier'+ string(directions(i))+'.png')
end

hold off