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

%% Plotting the average time across the dataset:
figure(1)
x=1:192;
ah = axes;
%Avg-memory:
%p1=bar(x,log10((results_mem.average_mem)/(1024^2)),0.5,"FaceColor","#762A83", "FaceAlpha", 0.9); %Purple.
% p1=bar(log10(results_time.average),0.5,"FaceColor","#762A83", "FaceAlpha", 0.9); %Purple.
plot(results_time)
hold on;
%Peak-memory:
%p2=bar(x,log10((results_mem.average_peak_mem)/(1024^2)),0.5,"FaceColor","#5AAE61", "FaceAlpha",0.6); %Pastle green. 009988 -Teal
% p2=bar((results_time.average),0.5,"FaceColor","#5AAE61", "FaceAlpha",0.6); %Pastle green. 009988 -Teal

xticklabels(["0","50","500","5000"]) %, "50000","500000", "5000000", "50000000", "500000000"]);
xtickangle(20);
xlabel('Total number of values in the plotted-matrix', "FontWeight","bold");
ylabel('Time taken to plot (s)', "FontWeight","bold");
%%Plot the first legend
lh = legend(ah, [p1(1) p2(1)],'Average memory', 'Peak memory');
lh.Location='NorthEast';
fontname("Times New Roman");
grid on

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
avg_pf_nvals = ([mean(time_pf_500.average),NaN,NaN,NaN, mean(time_pf_5000.average),NaN,NaN,NaN, mean(time_pf_50000.average),NaN,NaN,NaN, mean(time_pf_500000.average),NaN,NaN,NaN, mean(time_pf_5000000.average),NaN,NaN,NaN, mean(time_pf_50000000.average),NaN,NaN,NaN])/(1024^2);
avg_pm_nvals = ([NaN,mean(time_pm_500.average),NaN,NaN,NaN, mean(time_pm_5000.average), NaN,NaN,NaN,mean(time_pm_50000.average),NaN,NaN,NaN, mean(time_pm_500000.average),NaN,NaN,NaN, mean(time_pm_5000000.average),NaN,NaN,NaN, mean(time_pm_50000000.average),NaN,NaN])/(1024^2);
avg_mat_nvals = ([NaN,NaN,mean(time_mat_500.average),NaN, NaN,NaN,mean(time_mat_5000.average),NaN, NaN,NaN, mean(time_mat_50000.average),NaN, NaN,NaN,mean(time_mat_500000.average),NaN, NaN,NaN,mean(time_mat_5000000.average),NaN, NaN,NaN,mean(time_mat_50000000.average),NaN])/(1024^2);
avg_im_nvals = ([NaN,NaN,NaN,mean(time_im_500.average),NaN,NaN,NaN, mean(time_im_5000.average),NaN,NaN,NaN, mean(time_im_50000.average),NaN,NaN,NaN, mean(time_im_500000.average),NaN,NaN,NaN, mean(time_im_5000000.average), NaN,NaN,NaN,mean(time_im_50000000.average)])/(1024^2);

avg_plottype_nvals = [avg_pf_nvals,avg_pm_nvals,avg_mat_nvals,avg_im_nvals];

% % % %%% peak memory values:
% % % peak_pf_nvals = ([max(mem_pf_500.average_peak_mem), max(mem_pf_5000.average_peak_mem), max(mem_pf_50000.average_peak_mem), max(mem_pf_500000.average_peak_mem), max(mem_pf_5000000.average_peak_mem), max(mem_pf_50000000.average_peak_mem)])/(1024^2);
% % % peak_pm_nvals = ([max(mem_pm_500.average_peak_mem), max(mem_pm_5000.average_peak_mem), max(mem_pm_50000.average_peak_mem), max(mem_pm_500000.average_peak_mem), max(mem_pm_5000000.average_peak_mem), max(mem_pm_50000000.average_peak_mem)])/(1024^2);
% % % peak_mat_nvals = ([max(mem_mat_500.average_peak_mem), max(mem_mat_5000.average_peak_mem), max(mem_mat_50000.average_peak_mem), max(mem_mat_500000.average_peak_mem), max(mem_mat_5000000.average_peak_mem), max(mem_mat_50000000.average_peak_mem)])/(1024^2);
% % % peak_im_nvals = ([max(mem_im_500.average_peak_mem), max(mem_im_5000.average_peak_mem), max(mem_im_50000.average_peak_mem), max(mem_im_500000.average_peak_mem), max(mem_im_5000000.average_peak_mem), max(mem_im_50000000.average_peak_mem)])/(1024^2);
% % % 
% % % peak_plottype_nvals = [peak_pf_nvals,peak_pm_nvals,peak_mat_nvals,peak_im_nvals];

figure (2);
x=1:24;
% bar_avg = bar(x, log10(avg_plottype_nvals),"BarWidth",0.5);
bar_avg_pf = bar(x, avg_pf_nvals,"BarWidth",0.5,"CData",[(96/255) (188/255) (233/255)],'FaceAlpha',0.7); % light/ sky blue #60BCE9 - pcolorfast
hold on
bar_avg_pm = bar(x, avg_pm_nvals,"BarWidth",0.5,"CData", [(195/255) (168/255) (209/255)],'FaceAlpha',0.7); % Lilac #C3A8D1 - pcolormesh
bar_avg_mat = bar(x, avg_mat_nvals,"BarWidth",0.5,"CData",[(255/255) (185/255) (84/255)],'FaceAlpha',0.7); % Orange juice #FFB954 - matshow
bar_avg_im = bar(x, avg_im_nvals,"BarWidth",0.5,"CData",[(187/255) (228/255) (83/255)],'FaceAlpha',0.7); % Grass green #BBE453 - imshow

colour_scheme = ["#60BCE9","#C3A8D1","#FFB954","#BBE453"];

% bar_avg_pf.FaceColor = 'flat';
% 
% % Assign colors to each bar
% for i = 1:length(x)
%     bar_avg_pf.CData(i, :) = hex2rgb(colour_scheme(mod(i-1, length(colour_scheme)) + 1));
% end

xticklabels({'500', '5000', '50000', '500000', '5000000', '50000000'});
xlabel('Total plot size (N)');
ylabel('Average time to plot (s)');
grid on;

% h = findobj(gcf,'Tag','Box');
% % Formatting:
% for i=1:4:24
%     patch(get(h(i),'XData'),get(h(i),'YData'), [(187/255) (228/255) (83/255)],'FaceAlpha',0.7); % Grass green #BBE453 - imshow
%     patch(get(h(i+1),'XData'),get(h(i+1),'YData'), [(195/255) (168/255) (209/255)],'FaceAlpha',0.7); % Lilac #C3A8D1 - pcolormesh
%     patch(get(h(i+2),'XData'),get(h(i+2),'YData'), [(255/255) (185/255) (84/255)],'FaceAlpha',0.7); % Orange juice #FFB954 - matshow
%     patch(get(h(i+3),'XData'),get(h(i+2),'YData'), [(96/255) (188/255) (233/255)],'FaceAlpha',0.7); % light/ sky blue #60BCE9 - pcolorfast
% end



