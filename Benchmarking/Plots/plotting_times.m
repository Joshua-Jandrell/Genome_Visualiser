%% Benchmarking results: matplotlib Plotting Time taken
% Dynamic Genome Visualiser
% EIE Investigation 2024
% Plotting by Pragna Singh 2138875 (using results from Joshua Jandrell 2333213)

clear workspace
%%%%% Color scheme:  ** Must change to differentiate between memory
% % [(187/255) (228/255) (83/255)]); % Grass green #BBE453
% % [(195/255) (168/255) (209/255)]); %lilac #C3A8D1
% % [(255/255) (185/255) (84/255)]); % Orange juice #FFB954
% % [(96/255) (188/255) (233/255)]); % light/ sky blue #60BCE9
%%%%%

%% Reading in the data from the pre-uploaded cvs files:
results_time = readtable('zygosity_plotting_times.csv');

% Time parameters tested:
% n_variables, n_samples, plot_size, dpi,avg_plotting_time, plotting_times

results_time = sortrows(results_time, "n_values");
results_time(5, :) = [];  %removing pcolor

%% Plotting the average time across the dataset:  For initial data exploration and trends
% % figure(1)
% % % x=1:192;
% % ah = axes;
% % %Avg-memory:
% % p1=bar(log10(results_time.average),0.5,"FaceColor","#762A83", "FaceAlpha", 0.9); %Purple.
% % % plot(results_time.average)
% % hold on;
% % % #5AAE61 - Pastle green. 009988 -Teal
% % 
% % xticklabels(["0","50","500","5 000", "50 000","500 000", "5 000 000", "50 000 000", "500 000 000"]);
% % xtickangle(20);
% % xlabel('Total number of values in the plotted-matrix', "FontWeight","bold");
% % 
% % %set(gca,'yscale','log');
% % ylabel('Time taken to plot (s)', "FontWeight","bold");
% % %%Plot the first legend
% % legend({'Average time'},'Location','best');
% % fontname("Times New Roman");
% % grid on

%% For each n_value size: 
time_500 = results_time(results_time.n_values==500, :);
time_5000 = results_time(results_time.n_values==5000, :);
time_50000 = results_time(results_time.n_values==50000, :);
time_500000 = results_time(results_time.n_values==500000, :);
time_5000000 = results_time(results_time.n_values==5000000, :);
time_50000000 = results_time(results_time.n_values==50000000, :);
%
time_500 = time_500.average;
time_5000 = time_5000.average;
time_50000 = time_50000.average;
time_500000 = time_500000.average;
time_5000000 = time_5000000.average;
time_50000000 = time_50000000.average;

% plot types for each n_value:
%Creating data tables for each plot-type method:
pcolorfast_time = results_time(strcmp(results_time.plot_type, 'pcolorfast'), :);
pcolormesh_time = results_time(strcmp(results_time.plot_type, 'pcolormesh'), :);
matshow_time = results_time(strcmp(results_time.plot_type, 'matshow'), :);
imshow_time = results_time(strcmp(results_time.plot_type, 'imshow'), :);

%pcolorfast:
time_pf_500 = pcolorfast_time(pcolorfast_time.n_values==500, :);
time_pf_5000 = pcolorfast_time(pcolorfast_time.n_values==5000, :);
time_pf_50000 = pcolorfast_time(pcolorfast_time.n_values==50000, :);
time_pf_500000 = pcolorfast_time(pcolorfast_time.n_values==500000, :);
time_pf_5000000 = pcolorfast_time(pcolorfast_time.n_values==5000000, :);
time_pf_50000000 = pcolorfast_time(pcolorfast_time.n_values==50000000, :);

%pcolormesh:
time_pm_500 = pcolormesh_time(pcolormesh_time.n_values==500, :);
time_pm_5000 = pcolormesh_time(pcolormesh_time.n_values==5000, :);
time_pm_50000 = pcolormesh_time(pcolormesh_time.n_values==50000, :);
time_pm_500000 = pcolormesh_time(pcolormesh_time.n_values==500000, :);
time_pm_5000000 = pcolormesh_time(pcolormesh_time.n_values==5000000, :);
time_pm_50000000 = pcolormesh_time(pcolormesh_time.n_values==50000000, :);

%matshow:
time_mat_500 = matshow_time(matshow_time.n_values==500, :);
time_mat_5000 = matshow_time(matshow_time.n_values==5000, :);
time_mat_50000 = matshow_time(matshow_time.n_values==50000, :);
time_mat_500000 = matshow_time(matshow_time.n_values==500000, :);
time_mat_5000000 = matshow_time(matshow_time.n_values==5000000, :);
time_mat_50000000 = matshow_time(matshow_time.n_values==50000000, :);

%imshow:
time_im_500 = imshow_time(imshow_time.n_values==500, :);
time_im_5000 = imshow_time(imshow_time.n_values==5000, :);
time_im_50000 = imshow_time(imshow_time.n_values==50000, :);
time_im_500000 = imshow_time(imshow_time.n_values==500000, :);
time_im_5000000 = imshow_time(imshow_time.n_values==5000000, :);
time_im_50000000 = imshow_time(imshow_time.n_values==50000000, :);

%%% average time values:
avg_pf_nvals = ([mean(time_pf_500.average),NaN,NaN,NaN,NaN,  mean(time_pf_5000.average),NaN,NaN,NaN,NaN,  mean(time_pf_50000.average),NaN,NaN,NaN,NaN,  mean(time_pf_500000.average),NaN,NaN,NaN,NaN,  mean(time_pf_5000000.average),NaN,NaN,NaN,NaN,  mean(time_pf_50000000.average),NaN,NaN,NaN,NaN])*(10^3);
avg_pm_nvals = ([NaN,mean(time_pm_500.average),NaN,NaN,NaN,  NaN,mean(time_pm_5000.average),NaN,NaN,NaN,  NaN,mean(time_pm_50000.average),NaN,NaN,NaN,  NaN,mean(time_pm_500000.average),NaN,NaN,NaN,  NaN,mean(time_pm_5000000.average),NaN,NaN,NaN,  NaN,mean(time_pm_50000000.average),NaN,NaN,NaN])*(10^3);
avg_mat_nvals = ([NaN,NaN,mean(time_mat_500.average),NaN,NaN,  NaN,NaN,mean(time_mat_5000.average),NaN,NaN,  NaN,NaN,mean(time_mat_50000.average),NaN,NaN,  NaN,NaN,mean(time_mat_500000.average),NaN,NaN,  NaN,NaN,mean(time_mat_5000000.average),NaN,NaN,  NaN,NaN,mean(time_mat_50000000.average),NaN,NaN])*(10^3);    
avg_im_nvals = ([NaN,NaN,NaN,mean(time_im_500.average),NaN,  NaN,NaN,NaN,mean(time_im_5000.average),NaN,  NaN,NaN,NaN,mean(time_im_50000.average),NaN,  NaN,NaN,NaN,mean(time_im_500000.average),NaN,  NaN,NaN,NaN,mean(time_im_5000000.average),NaN,  NaN,NaN,NaN,mean(time_im_50000000.average),NaN])*(10^3);

%avg_plottype_nvals = [avg_pf_nvals,avg_pm_nvals,avg_mat_nvals,avg_im_nvals];

figure (2);
x=1:30;
% bar_avg = bar(x, log10(avg_plottype_nvals),"BarWidth",0.5);
bar_avg_pf = bar(x, log10(avg_pf_nvals),"BarWidth",0.6,"Facecolor", "#60BCE9",'FaceAlpha',0.7); % light/ sky blue #60BCE9 - pcolorfast
hold on;
grid on;
bar_avg_pm = bar(x, log10(avg_pm_nvals),"BarWidth",0.6,"Facecolor", "#C3A8D1",'FaceAlpha',0.7); % Lilac #C3A8D1 - pcolormesh
bar_avg_mat = bar(x, log10(avg_mat_nvals),"BarWidth",0.6,"Facecolor", "#FFB954",'FaceAlpha',0.7); % Orange juice #FFB954 - matshow
bar_avg_im = bar(x, log10(avg_im_nvals),"BarWidth",0.6,"Facecolor", "#BBE453",'FaceAlpha',0.7); % Grass green #BBE453 - imshow

%colour_scheme = ["#60BCE9","#C3A8D1","#FFB954","#BBE453"];

xticks([0 2.5 7.5 12.5 17.5 22.5 27.5]);
%xticklabels({'0','500', '5 000', '50 000', '500 000', '5 000 000', '50 000 000'});
xticklabels({'0', '5×10^2', '5×10^3', '5×10^4', '5×10^5', '5×10^6', '5×10^7'});
xlabel('Blocks plotted');

set(gca,'yscale','log');
yticklabels({'10^1','10^1^.^5','10^2','10^2^.^5','10^3'});
ylabel('Average plotting time (ms)');

fontname("Times New Roman");
fontsize(12, "points");
%legend (["imshow", "matshow", "pcolormesh", "pcolorfast"], "Location","northwest");%,"FontSize", 8)
legend (["pcolorfast",  "pcolormesh", "matshow","imshow"], "Location","northwest", "FontSize", 10);

%% For each matplotlib function:
pf_time= (pcolorfast_time.average);
pm_time = (pcolormesh_time.average); %*(10^3);
mat_time = (matshow_time.average); %*(10^3);
im_time = (imshow_time.average); %*(10^3);

figure(3);
x1 = 1:4; % pcolorfast, pcolormesh, matshow, imshow
boxplot(([pf_time, pm_time,mat_time,im_time]), x1,"Widths", 0.5, 'Symbol','*-k');
hold on;
grid on;

    %Formatting:
h = findobj(gca,'Tag','Box');
patch(get(h(1),'XData'),get(h(1),'YData'), [(187/255) (228/255) (83/255)],'FaceAlpha',0.7); % Grass green #BBE453 - imshow
patch(get(h(3),'XData'),get(h(3),'YData'), [(195/255) (168/255) (209/255)],'FaceAlpha',0.7); % Lilac #C3A8D1 - pcolormesh
patch(get(h(2),'XData'),get(h(2),'YData'), [(255/255) (185/255) (84/255)],'FaceAlpha',0.7); % Orange juice #FFB954 - matshow
patch(get(h(4),'XData'),get(h(4),'YData'), [(96/255) (188/255) (233/255)],'FaceAlpha',0.7); % light/ sky blue #60BCE9 - pcolorfast

xticklabels(["pcolorfast", "pcolormesh", "matshow", "imshow"]);
xlabel('Matplotlib function');

ylabel('Average plotting time (s)');
ylim([0 0.3]);

fontname("Times New Roman");
fontsize(12, "points");
