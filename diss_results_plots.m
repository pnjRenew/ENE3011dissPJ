clear all
close all   % close all figures


dbeier_damage = readmatrix("damage_results_copper_dbeier.csv");
%dbd_idx = (dbeier_damage(:,3)==90)
%dbeier_damage_filtered_90 =dbeier_damage(dbd_idx,:)

directions = [90, 180, 270, 0]


dbeier_damage_filtered_90 = dbeier_damage(dbeier_damage(: ,3) == 90,  :);


pthies_damage = readmatrix("damage_results_copper_pthies.csv")
pthies_damage_filtered_90 = pthies_damage(pthies_damage(: ,3) == 90,  :);

f1 = figure;
%Perhaps contour? Or scatter?
xlim([0 inf])   % set x minimum to 0 (hopefully sufficient), maximum to automatic
ylim([0 inf])   % ditto for y axis
t = title('Hs vs damage')
xl = xlabel('Hs')
yl = ylabel('Damage')
%xticks()
%yticks()
grid on
hold on
scatter(dbeier_damage_filtered_90(:,1), dbeier_damage_filtered_90(:,5));
scatter(pthies_damage_filtered_90(:,1), pthies_damage_filtered_90(:,5));
%plot(dbeier_damage_filtered_90(:,1), dbeier_damage_filtered_90(:,5),'o-b');
%plot(pthies_damage_filtered_90(:,1), pthies_damage_filtered_90(:,5),'o-r');
leg = legend({'D Beier damage', 'P Thies damage'},'Location', 'southeast')
hold off

f2 = figure

t = title('Hs and T vs damage')
xl = xlabel('Hs')
yl = ylabel('Direction')
view(45,45)     % rotate view
grid on
hold on
plot3(dbeier_damage_filtered_90(:,1), dbeier_damage_filtered_90(:,3), dbeier_damage_filtered_90(:,5))
% Hs and T in a contour plot vs damage
hold off