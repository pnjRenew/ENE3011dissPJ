clear all
close all

%TODO: may wish to lose titles, to avoid duplications

filename_p_thies_damage = 'damage_results_copper_pthies.csv';
filename_d_beier_damage = 'damage_results_copper_dbeier.csv';


pthies_damage = readtable(filename_p_thies_damage);
dbeier_damage = readtable(filename_d_beier_damage);
%directions = [0 90 180 270]
directions = [45 135 225 315] % diagonal directions

% TODO: could find axis limits instead of hard-coded

figure1 = figure
% for each of the directions
for i = 1:length(directions)    
    % hold on
    plot(pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   % filter damage by direction    
    %hold off
    xlim([0 inf])
    ylim([0 inf])
    grid on
    title('Damage (individual) plot for direction: ' + string(directions(i)) + '°')
    saveas(figure1,'damage_plot_pthies'+ string(directions(i))+'.png')
end

figure1 = figure
% for each of the directions
for i = 1:length(directions)    
    % hold on
    plot(dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   % filter damage by direction    
    %hold off
    xlim([0 inf])
    ylim([0 inf])
    grid on
    title('Damage (individual) plot for direction: ' + string(directions(i)) + '°')
    saveas(figure1,'damage_plot_dbeier'+ string(directions(i))+'.png')
end



figure2 = figure

for i = 1:length(directions)    
    % hold on
    scatter(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   % filter damage by direction    
    %hold off
    xlabel('Hs (m)')
    ylabel('Damage (individual)')
    xlim([0 4])
    ylim([0 1.5e-5])
    grid on
    %title('Scatter plot of Hs and damage (individual) for direction: ' + string(directions(i)) + '°')
    %subtitle('Tp (s) values beside data points')
    %text(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))))
    textfit(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))))
    saveas(figure2,'damage_scatter_Hs_pthies'+ string(directions(i))+'.png')
end

for i = 1:length(directions)    
    % hold on
    scatter(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)), dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   % filter damage by direction    
    %hold off
    xlabel('Hs (m)')
    ylabel('Damage (individual)')
    %xlim([0 4])
    %ylim([0 1.5e-5])
    grid on
    %title('Scatter plot of Hs and damage (individual) for direction: ' + string(directions(i)) + '°')
    %subtitle('Tp (s) values beside data points')
    %text(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))))
    %textfit(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)) + 0.1, dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)),string(dbeier_damage.T_sim(dbeier_damage.dir_sim == directions(i))))
    saveas(figure2,'damage_scatter_Hs_dbeier'+ string(directions(i))+'.png')
end



figure3 = figure

for i = 1:length(directions)    
    % hold on
    %scatter(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   % filter damage by direction    
    gscatter(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)),'brgk');
    %hold off
    %xlabel('Tp (s)')    
    xlabel('Tz (s)')    
    ylabel('Damage (individual)')
    lgd = legend
    lgd.Title.String = "Hs (m)"
    xlim([0 7.5])
    ylim([0 1.5e-5])    
    grid on

    %title('Scatter plot of Tp and damage (individual) for direction: ' + string(directions(i)) + '°')
    %subtitle('Grouped by Hs (m) values')
    %text(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))))    
    %textfit(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))))    
    %saveas(figure3,'damage_scatter_Tp_pthies'+ string(directions(i))+'.png')
    saveas(figure3,'damage_scatter_Tz_pthies'+ string(directions(i))+'.png')
    %saveas(figure3,'damage_scatter_Tp_pthies'+ string(i)+'.png')
end

for i = 1:length(directions)    
    % hold on
    %scatter(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),'o', 'LineWidth',2);   % filter damage by direction    
    gscatter(dbeier_damage.T_sim(pthies_damage.dir_sim == directions(i)), dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)),dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)),'brgk');
    %hold off
    %xlabel('Tp (s)')    
    xlabel('Tz (s)')    
    ylabel('Damage (individual)')
    lgd = legend
    lgd.Title.String = "Hs (m)"    
    xlim([0 7.5])
    ylim([0 1.5e-5])    
    grid on
    %title('Scatter plot of Tp and damage (individual) for direction: ' + string(directions(i)) + '°')
    %subtitle('Grouped by Hs (m) values')
    %text(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)),string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))))    
    %textfit(dbeier_damage.T_sim(dbeier_damage.dir_sim == directions(i)) + 0.1, dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)),string(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i))))    
    %saveas(figure3,'damage_scatter_Tp_dbeier'+ string(directions(i))+'.png')
    saveas(figure3,'damage_scatter_Tz_dbeier'+ string(directions(i))+'.png')
    %saveas(figure3,'damage_scatter_Tp_dbeier'+ string(i)+'.png')
end


figure4 = figure
for i = 1:length(directions)    
    % hold on
    plot3(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)));
    xlabel('Hs (m)')
    %ylabel('Tp (s)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)') 
    title('Damage (individual) 3D plot for direction: ' + string(directions(i)) + '°')
    % hold off
    %xlim([0 4])
    %ylim([0 7.5])
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    saveas(figure4, 'damage3d_plot_pthies'+ string(directions(i))+'.png')
end

for i = 1:length(directions)    
    % hold on
    plot3(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)), dbeier_damage.T_sim(dbeier_damage.dir_sim == directions(i)), dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)));
    xlabel('Hs (m)')
    %ylabel('Tp (s)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)') 
    title('Damage (individual) 3D plot for direction: ' + string(directions(i)) + '°')
    % hold off
    %xlim([0 4])
    %ylim([0 7.5])
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    saveas(figure4, 'damage3d_plot_dbeier'+ string(directions(i))+'.png')
end



figure5 = figure
for i = 1:length(directions)        
    % hold on
    scatter3(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)), 'LineWidth',2);
    xlabel('Hs (m)')
    %ylabel('Tp (s)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)')
    title('Damage (individual) 3D scatter for direction: ' + string(directions(i)) + '°')
    % hold off   
    xlim([0 4])
    ylim([0 7.5])
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    %text(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)), string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))) + 'm,' + string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))) + 's,' + string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))))
    saveas(figure5, 'damagescatter3d_plot_pthies'+ string(directions(i))+'.png')
end


for i = 1:length(directions)        
    % hold on
    scatter3(dbeier_damage.Hs_sim(dbeier_damage.dir_sim == directions(i)), dbeier_damage.T_sim(dbeier_damage.dir_sim == directions(i)), dbeier_damage.damage_copper_dbeier(dbeier_damage.dir_sim == directions(i)), 'LineWidth',2);
    xlabel('Hs (m)')
    %ylabel('Tp (s)')
    ylabel('Tz (s)')
    zlabel('Damage (individual)')
    title('Damage (individual) 3D scatter for direction: ' + string(directions(i)) + '°')
    % hold off   
    %xlim([0 4])
    %ylim([0 7.5])
    zlim([0 1.5e-5])    
    grid on
    view(45,45)
    %text(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)), string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))) + 'm,' + string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))) + 's,' + string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))))
    saveas(figure5, 'damagescatter3d_plot_dbeier'+ string(directions(i))+'.png')
end



hold off





% figure6 = figure
% for i = 1:length(directions)        
%     % hold on
%     surf([pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i))]);
%     xlabel('Hs (m)')
%     ylabel('Tp (s)')
%     zlabel('Damage (individual)')
%     title('Damage (individual) surface plot for direction: ' + string(directions(i)) + '°')
%     % hold off   
%     xlim([0 4])
%     ylim([0 7.5])
%     zlim([0 1.5e-5])    
%     grid on
%     view(45,45)
%     %text(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i)) + 0.1, pthies_damage.T_sim(pthies_damage.dir_sim == directions(i)), pthies_damage.damage_copper_pthies(pthies_damage.dir_sim == directions(i)), string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))) + 'm,' + string(pthies_damage.T_sim(pthies_damage.dir_sim == directions(i))) + 's,' + string(pthies_damage.Hs_sim(pthies_damage.dir_sim == directions(i))))
%     saveas(figure6, 'damagescatter3d_plot_pthies'+ string(directions(i))+'.png')
% end
% hold off