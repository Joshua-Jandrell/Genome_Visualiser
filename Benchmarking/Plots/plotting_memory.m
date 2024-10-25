%% Benchmarking results: Memory usage for Matplotlib plot functions
% Dynamic Genome Visualiser
% EIE Investigation 2024
% Plotting by Pragna Singh 2138875 (using results from Joshua Jandrell 2333213)

clear workspace
%%%%% Color scheme:
% % [(187/255) (228/255) (83/255)]); % Grass green #BBE453
% % [(195/255) (168/255) (209/255)]); %lilac #C3A8D1
% % [(255/255) (185/255) (84/255)]); % Orange juice #FFB954
% % [(96/255) (188/255) (233/255)]); % light/ sky blue #60BCE9
%%%%%
%% Reading in the data from the pre-uploaded cvs files:
results_memory = readtable('zygosity_plotting_memory.csv'); % , 'NumHeaderLines',1);

%%% from python library: Memory values = bytes!!!
% Conversion: 1 kilobytes (KB) = 1024 bytes (b) |&| 1 megabyte (MB) = 1024
% vs 1 kb = 1000 |&| 1 mb = 1000

results_mem = sortrows(results_memory, "n_values");
results_mem(5, :) = [];  %removing pcolor
z = max((results_mem.average_mem)/(1024^2));
z1 = max((results_mem.average_peak_mem)/(1024^2));

%% Plotting the average memory and the peak-memory accross the dataset:
% % figure(1)
% % x=1:192;
% % ah = axes;
% % %Avg-memory:
% % %p1=bar(x,log10((results_mem.average_mem)/(1024^2)),0.5,"FaceColor","#762A83", "FaceAlpha", 0.9); %Purple.
% % p1=bar(log10((results_mem.average_mem)/(1024^2)),0.5,"FaceColor","#762A83", "FaceAlpha", 0.9); %Purple.
% % hold on;
% % %Peak-memory:
% % %p2=bar(x,log10((results_mem.average_peak_mem)/(1024^2)),0.5,"FaceColor","#5AAE61", "FaceAlpha",0.6); %Pastle green. 009988 -Teal
% % p2=bar(log10((results_mem.average_peak_mem)/(1024^2)),0.5,"FaceColor","#5AAE61", "FaceAlpha",0.6); %Pastle green. 009988 -Teal
% % 
% % xticklabels(["0","50","500","5000"]) %, "50000","500000", "5000000", "50000000", "500000000"]);
% % xtickangle(20);
% % xlabel('Total number of values in the plotted-matrix', "FontWeight","bold");
% % ylabel('Memory used (MB)', "FontWeight","bold");
% % %%Plot the first legend
% % lh = legend(ah, [p1(1) p2(1)],'Average memory', 'Peak memory');
% % lh.Location='NorthEast';
% % fontname("Times New Roman");
% % grid on

%% For each n_value size: 
mem_500 = results_mem(results_mem.n_values==500, :);
mem_5000 = results_mem(results_mem.n_values==5000, :);
mem_50000 = results_mem(results_mem.n_values==50000, :);
mem_500000 = results_mem(results_mem.n_values==500000, :);
mem_5000000 = results_mem(results_mem.n_values==5000000, :);
mem_50000000 = results_mem(results_mem.n_values==50000000, :);
%
mem_500 = mem_500.average_mem;
mem_5000 = mem_5000.average_mem;
mem_50000 = mem_50000.average_mem;
mem_500000 = mem_500000.average_mem;
mem_5000000 = mem_5000000.average_mem;
mem_50000000 = mem_50000000.average_mem;

% plot types for each n_value:
%Creating data tables for each plot-type method:
pcolorfast_mem = results_mem(strcmp(results_mem.plot_type, 'pcolorfast'), :);
pcolormesh_mem = results_mem(strcmp(results_mem.plot_type, 'pcolormesh'), :);
matshow_mem = results_mem(strcmp(results_mem.plot_type, 'matshow'), :);
imshow_mem = results_mem(strcmp(results_mem.plot_type, 'imshow'), :);

%pcolorfast:
mem_pf_500 = pcolorfast_mem(pcolorfast_mem.n_values==500, :);
mem_pf_5000 = pcolorfast_mem(pcolorfast_mem.n_values==5000, :);
mem_pf_50000 = pcolorfast_mem(pcolorfast_mem.n_values==50000, :);
mem_pf_500000 = pcolorfast_mem(pcolorfast_mem.n_values==500000, :);
mem_pf_5000000 = pcolorfast_mem(pcolorfast_mem.n_values==5000000, :);
mem_pf_50000000 = pcolorfast_mem(pcolorfast_mem.n_values==50000000, :);

%pcolormesh:
mem_pm_500 = pcolormesh_mem(pcolormesh_mem.n_values==500, :);
mem_pm_5000 = pcolormesh_mem(pcolormesh_mem.n_values==5000, :);
mem_pm_50000 = pcolormesh_mem(pcolormesh_mem.n_values==50000, :);
mem_pm_500000 = pcolormesh_mem(pcolormesh_mem.n_values==500000, :);
mem_pm_5000000 = pcolormesh_mem(pcolormesh_mem.n_values==5000000, :);
mem_pm_50000000 = pcolormesh_mem(pcolormesh_mem.n_values==50000000, :);

%matshow:
mem_mat_500 = matshow_mem(matshow_mem.n_values==500, :);
mem_mat_5000 = matshow_mem(matshow_mem.n_values==5000, :);
mem_mat_50000 = matshow_mem(matshow_mem.n_values==50000, :);
mem_mat_500000 = matshow_mem(matshow_mem.n_values==500000, :);
mem_mat_5000000 = matshow_mem(matshow_mem.n_values==5000000, :);
mem_mat_50000000 = matshow_mem(matshow_mem.n_values==50000000, :);

%imshow:
mem_im_500 = imshow_mem(imshow_mem.n_values==500, :);
mem_im_5000 = imshow_mem(imshow_mem.n_values==5000, :);
mem_im_50000 = imshow_mem(imshow_mem.n_values==50000, :);
mem_im_500000 = imshow_mem(imshow_mem.n_values==500000, :);
mem_im_5000000 = imshow_mem(imshow_mem.n_values==5000000, :);
mem_im_50000000 = imshow_mem(imshow_mem.n_values==50000000, :);

%% average memory values:
avg_pf_nvals = ([mean(mem_pf_500.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_5000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_5000000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_50000000.average_mem),NaN,NaN,NaN])/(1024^2);
avg_pm_nvals = ([NaN,mean(mem_pm_500.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_5000.average_mem), NaN,NaN,NaN,NaN, mean(mem_pm_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_5000000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_50000000.average_mem),NaN,NaN])/(1024^2);
avg_mat_nvals = ([NaN,NaN,mean(mem_mat_500.average_mem),NaN, NaN,NaN,NaN, mean(mem_mat_5000.average_mem),NaN, NaN,NaN,NaN, mean(mem_mat_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_mat_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_mat_5000000.average_mem),NaN,NaN,NaN,NaN, mean(mem_mat_50000000.average_mem),NaN])/(1024^2);
avg_im_nvals = ([NaN,NaN,NaN,mean(mem_im_500.average_mem),NaN,NaN,NaN,NaN, mean(mem_im_5000.average_mem),NaN,NaN,NaN,NaN, mean(mem_im_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_im_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_im_5000000.average_mem), NaN,NaN,NaN,NaN, mean(mem_im_50000000.average_mem)])/(1024^2);

% % % For the poster:
% % avg_pf_nvals = ([mean(mem_pf_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_5000000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pf_50000000.average_mem),NaN,NaN,NaN])/(1024^2);
% % avg_pm_nvals = ([NaN, mean(mem_pm_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_5000000.average_mem),NaN,NaN,NaN,NaN, mean(mem_pm_50000000.average_mem),NaN,NaN])/(1024^2);
% % avg_mat_nvals = ([NaN,NaN, mean(mem_mat_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_mat_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_mat_5000000.average_mem),NaN,NaN,NaN,NaN, mean(mem_mat_50000000.average_mem),NaN])/(1024^2);
% % avg_im_nvals = ([NaN,NaN,NaN, mean(mem_im_50000.average_mem),NaN,NaN,NaN,NaN, mean(mem_im_500000.average_mem),NaN,NaN,NaN,NaN, mean(mem_im_5000000.average_mem), NaN,NaN,NaN,NaN, mean(mem_im_50000000.average_mem)])/(1024^2);

avg_plottype_nvals = [avg_pf_nvals,avg_pm_nvals,avg_mat_nvals,avg_im_nvals];

%%% peak memory values:
peak_pf_nvals = ([max(mem_pf_500.average_peak_mem), max(mem_pf_5000.average_peak_mem), max(mem_pf_50000.average_peak_mem), max(mem_pf_500000.average_peak_mem), max(mem_pf_5000000.average_peak_mem), max(mem_pf_50000000.average_peak_mem)])/(1024^2);
peak_pm_nvals = ([max(mem_pm_500.average_peak_mem), max(mem_pm_5000.average_peak_mem), max(mem_pm_50000.average_peak_mem), max(mem_pm_500000.average_peak_mem), max(mem_pm_5000000.average_peak_mem), max(mem_pm_50000000.average_peak_mem)])/(1024^2);
peak_mat_nvals = ([max(mem_mat_500.average_peak_mem), max(mem_mat_5000.average_peak_mem), max(mem_mat_50000.average_peak_mem), max(mem_mat_500000.average_peak_mem), max(mem_mat_5000000.average_peak_mem), max(mem_mat_50000000.average_peak_mem)])/(1024^2);
peak_im_nvals = ([max(mem_im_500.average_peak_mem), max(mem_im_5000.average_peak_mem), max(mem_im_50000.average_peak_mem), max(mem_im_500000.average_peak_mem), max(mem_im_5000000.average_peak_mem), max(mem_im_50000000.average_peak_mem)])/(1024^2);

peak_plottype_nvals = [peak_pf_nvals,peak_pm_nvals,peak_mat_nvals,peak_im_nvals];

figure (1);
x=1:length(avg_pf_nvals);
% Plotting as a whole array
bar_avg_pf = bar(x, log10(avg_pf_nvals),"BarWidth",0.6,"FaceColor",'#238F9D','FaceAlpha',0.7); %Turquiose: #238F9D % light/ sky blue #60BCE9 - pcolorfast
hold on;
bar_avg_pm = bar(x, log10(avg_pm_nvals),"BarWidth",0.6,"FaceColor", '#8C4E99','FaceAlpha',0.7); %Purple: #8C4E99 % Lilac #C3A8D1 - pcolormesh
bar_avg_mat = bar(x, log10(avg_mat_nvals),"BarWidth",0.6,"FaceColor",'#F56B00','FaceAlpha',0.7);%Blood-orange: #F56B00  % Orange juice #FFB954 - matshow
bar_avg_im = bar(x, log10(avg_im_nvals),"BarWidth",0.6,"FaceColor",'#019800','FaceAlpha',0.7); %Greeeeen: #019800   % Grass green #BBE453 - imshow

% colour_scheme = ["#60BCE9","#C3A8D1","#FFB954","#BBE453"];

grid on;

%x-axis format:
xticks([2.5 7.5 12.5 17.5 22.5 27.5 32.5]);
xticklabels({'5×10^2', '5×10^3', '5×10^4', '5×10^5', '5×10^6', '5×10^7'});
xlabel('Blocks plotted');
        
%y-axis format:   %do not log scale the y-axis!!!! is weird
ylabel('Average memory used (MB)');
yticklabels({'10^-^0^.^5', '0', '10^0^.^5' , '10^1', '10^1^.^5', '10^2', '10^2^.^5', '10^3'});

fontname("Times New Roman");
fontsize(12, "points");
legend (["pcolorfast", "pcolormesh", "matshow", "imshow"], "Location","best","FontSize", 10);


%%
figure (3);
x = 1:6;
nan16 = NaN(16,1);
boxplot(log10([mem_500, nan16, nan16, nan16, nan16, mem_50000000]), x,"Widths", 0.6, 'Symbol','*-k');
hold on;
grid on;
%Colours:
h = findobj(gca,'Tag','Box');
patch(get(h(1),'XData'),get(h(1),'YData'), [(166/255) (190/255) (84/255)],'FaceAlpha',0.6); %lime green
patch(get(h(6),'XData'),get(h(6),'YData'), [(114/255) (30/255) (23/255)],'FaceAlpha',0.5); %brown

nan32 = NaN(32,1);
boxplot(log10([nan32, mem_5000, nan32, nan32, mem_5000000, nan32]), x,"Widths", 0.6, 'Symbol','*-k');
%Colours:
h = findobj(gca,'Tag','Box');
patch(get(h(2),'XData'),get(h(2),'YData'), [(228/255) (156/255) (57/255)],'FaceAlpha',0.7); %gold-yellow
patch(get(h(5),'XData'),get(h(5),'YData'), [(218/255) (34/255) (34/255)],'FaceAlpha',0.6); %bright red

nan48 = NaN(48,1);
boxplot(log10([nan48, nan48, mem_50000, mem_500000,nan48, nan48]), x,"Widths", 0.6, 'Symbol','*-k');
    % Formatting:
%Colours:
h = findobj(gca,'Tag','Box');
% Formatting:
patch(get(h(3),'XData'),get(h(3),'YData'), [(238/255) (119/255) (51/255)],'FaceAlpha',0.7); %orange
patch(get(h(4),'XData'),get(h(4),'YData'), [(223/255) (72/255) (40/255)],'FaceAlpha',0.7); %blood-orange

%Axes:
%xticks(y);
xticklabels ({'500' '5000' '50000' '500000' '5000000' '50000000'});
xlabel('Total plot size');

set(gca,'yscale','log');
ylim([5.5 9.5])
yticklabels(["1.0e+5.5", "1.0e+6", "1.0e+6.5", "1.0e+7", "1.0e+7.5", "1.0e+8", "1.0e+8.5", "1.0e+9","1.0e+9.5"]);
ylabel('Average memory used (MB)');

%% Box plotting average for each plot method:

%Creating data tables for each plot-type method:
pcolorfast_mem = results_mem(strcmp(results_mem.plot_type, 'pcolorfast'), :);
pcolormesh_mem = results_mem(strcmp(results_mem.plot_type, 'pcolormesh'), :);
matshow_mem = results_mem(strcmp(results_mem.plot_type, 'matshow'), :);
imshow_mem = results_mem(strcmp(results_mem.plot_type, 'imshow'), :); 
%
mem_pcolorfast = (pcolorfast_mem.average_mem)/(1024^2);
mem_pcolormesh = (pcolormesh_mem.average_mem)/(1024^2);
mem_matshow = (matshow_mem.average_mem)/(1024^2);
mem_imshow = (imshow_mem.average_mem)/(1024^2);

mem_pcolorfast_bar = (sum(mem_pcolorfast(:,1))/64);
mem_pcolormesh_bar = (sum(mem_pcolormesh(:,1))/64);
mem_matshow_bar = (sum(mem_matshow(:,1))/64);
mem_imshow_bar = (sum(mem_imshow(:,1))/64);

figure (4);
tiledlayout(2,2, "TileSpacing","loose"); %, "Padding","loose");

fontname("Times New Roman");
fontsize(10,"points");

nexttile %Average memory used by all Matplotlib functions
%%%%%%%%%%%%%%%%% Box&Whisker plots:
x = 1:4; % pcolorfast, pcolormesh, matshow, imshow
boxplot(([mem_pcolorfast,mem_pcolormesh, mem_matshow, mem_imshow]), x,"Widths", 0.8, 'Symbol','*-k');
hold on;
grid on;
    %Formatting:
h = findobj(gca,'Tag','Box');
patch(get(h(1),'XData'),get(h(1),'YData'), [(68/255) (187/255) (153/255)],'FaceAlpha',0.5); %Mint
patch(get(h(2),'XData'),get(h(2),'YData'), [(221/255) (204/255) (119/255)],'FaceAlpha',0.5); %purple
patch(get(h(3),'XData'),get(h(3),'YData'), [(170/255) (68/255) (153/255)],'FaceAlpha',0.5); % sand
patch(get(h(4),'XData'),get(h(4),'YData'), [(33/255) (102/255) (172/255)],'FaceAlpha',0.5); % blue
%%%%%%%%%%%%%%%%% Bar graph:
b_avg = bar(x,([mem_pcolorfast_bar,mem_pcolormesh_bar,mem_matshow_bar,mem_imshow_bar]),"FaceColor","flat","BarWidth",0.4);
hold on
% Changing colour scheme:   blue,purple,sand, mint
clr = [33 102 172;
    170 68 153;
    221 204 119;
    68 187 153    
    ] / 255;
b_avg.CData = clr;
b_avg.FaceAlpha=0.7;

%x-axis
xticklabels(["pcolorfast", "pcolormesh", "matshow", "imshow"]);
xlabel('Matplotlib function used', "FontWeight","bold");
%y-axis
ylim([0 200]);
ylabel('Average Memory (MB)', "FontWeight","bold");

fontname("Times New Roman");
legend (["imshow", "matshow", "pcolormesh", "pcolorfast"], "Location","bestoutside","FontSize", 8)

%%%%%%%%%%% Macro average memory boxplots for plot functs: %%%%%%%%%%%%%%%
nexttile %Average memory used by best 3 Matplotlib functions
x1 = 1:3; % pcolorfast, matshow, imshow
boxplot(([mem_pcolorfast,mem_matshow,mem_imshow]), x1,"Widths", 0.8, 'Symbol','*-k');
hold on;
grid on;

    %Formatting:
h = findobj(gca,'Tag','Box');
patch(get(h(1),'XData'),get(h(1),'YData'), [(68/255) (187/255) (153/255)],'FaceAlpha',0.5); %Mint
patch(get(h(2),'XData'),get(h(2),'YData'), [(221/255) (204/255) (119/255)],'FaceAlpha',0.5); % sand
patch(get(h(3),'XData'),get(h(3),'YData'), [(33/255) (102/255) (172/255)],'FaceAlpha',0.5); % blue

%x-axis
xticklabels(["pcolorfast", "matshow", "imshow"]);
xlabel('Matplotlib function used', "FontWeight","bold");
%y-axis
ylim([0 50])
ylabel('Average Memory (MB)', "FontWeight","bold");

fontname("Times New Roman");

%%%%%%%%%%%%%% For peak memory usage:
peakmem_pcolorfast = (pcolorfast_mem.average_peak_mem)/(1024^2);
peakmem_pcolormesh = (pcolormesh_mem.average_peak_mem)/(1024^2);
peakmem_matshow = (matshow_mem.average_peak_mem)/(1024^2);
peakmem_imshow = (imshow_mem.average_peak_mem)/(1024^2);

peakmem_pcolorfast_bar = (sum(peakmem_pcolorfast(:,1))/64);
peakmem_pcolormesh_bar = (sum(peakmem_pcolormesh(:,1))/64);
peakmem_matshow_bar = (sum(peakmem_matshow(:,1))/64);
peakmem_imshow_bar = (sum(peakmem_imshow(:,1))/64);


nexttile %Peak-memory used by all Matplotlib functions
%%%%%%%%%%%%%%%%% Box&Whisker plots:
x = 1:4; % pcolorfast, pcolormesh, matshow, imshow
x1 = 1:3;
boxplot(([peakmem_pcolorfast,peakmem_pcolormesh, peakmem_matshow, peakmem_imshow]), x,"Widths", 0.8, 'Symbol','*-k');

hold on;
grid on;
    %Formatting colours:
h = findobj(gca,'Tag','Box');
patch(get(h(1),'XData'),get(h(1),'YData'), [(68/255) (187/255) (153/255)],'FaceAlpha',0.5); %Mint
patch(get(h(2),'XData'),get(h(2),'YData'), [(221/255) (204/255) (119/255)],'FaceAlpha',0.5); %purple
patch(get(h(3),'XData'),get(h(3),'YData'), [(170/255) (68/255) (153/255)],'FaceAlpha',0.5); % sand
patch(get(h(4),'XData'),get(h(4),'YData'), [(33/255) (102/255) (172/255)],'FaceAlpha',0.5); % blue

%%%%%%%%%%%%%%%%% Bar graph:
b_peak = bar(x,([peakmem_pcolorfast_bar, peakmem_pcolormesh_bar, peakmem_matshow_bar, peakmem_imshow_bar]),"FaceColor","flat","BarWidth",0.4);
hold on;
% Changing colour scheme:   blue,purple,sand, mint
clr = [33 102 172;
    170 68 153;
    221 204 119;
    68 187 153    
    ] / 255;
b_peak.CData = clr;
b_peak.FaceAlpha=0.9;

%x-axis
xticklabels(["pcolorfast", "pcolormesh", "matshow", "imshow"]);
xlabel('Matplotlib function used', "FontWeight","bold");

%y-axis
ylim([0 300]);
ylabel('Peak Memory (MB)', "FontWeight","bold");

fontname("Times New Roman");

%%%%%%%%%%% Macro peak memory boxplots for plot functs:
nexttile %Peak-memory used by best 3 Matplotlib functions
%%%%%%%%%%%%%%%%% Box&Whisker plots:
% % pcolorfast, matshow, imshow
boxplot(([peakmem_pcolorfast, peakmem_matshow, peakmem_imshow]), x1,"Widths", 0.8, 'Symbol','*-k');
hold on;
grid on;

    %Formatting:
h = findobj(gca,'Tag','Box');
patch(get(h(1),'XData'),get(h(1),'YData'), [(68/255) (187/255) (153/255)],'FaceAlpha',0.5); %Mint
patch(get(h(2),'XData'),get(h(2),'YData'), [(221/255) (204/255) (119/255)],'FaceAlpha',0.5); % sand
patch(get(h(3),'XData'),get(h(3),'YData'), [(33/255) (102/255) (172/255)],'FaceAlpha',0.5); % blue

%x-axis
xticklabels(["pcolorfast", "matshow", "imshow"]);
xlabel('Matplotlib function used', "FontWeight","bold");
%y-axis
ylim([0 50]);
ylabel('Peak Memory (MB)', "FontWeight","bold");

fontname("Times New Roman");


%% Summary of plot funct memory:
placeholder = zeros([64 1]);

% figure (6);
% x = 1:4;
% b_peak_summ = bar(x, ([peakmem_pcolorfast_bar, peakmem_pcolormesh_bar, peakmem_matshow_bar, peakmem_imshow_bar]),"green","FaceColor","flat","BarWidth",0.4,'FaceAlpha',0.3);
% hold on;
% b_avg = bar(x, ([mem_pcolorfast_bar,mem_pcolormesh_bar,mem_matshow_bar,mem_imshow_bar]),"FaceColor","flat","BarWidth",0.4);
% 
% % Changing colour scheme:   blue,purple,sand, mint
% clr = [33 102 172;
%     170 68 153;
%     221 204 119;
%     68 187 153    
%     ] / 255;
% b_avg.CData = clr;
% b_avg.FaceAlpha=0.3;
% b_peak_summ.CData = clr;
% b_peak_summ.FaceAlpha=0.3;
%%%%%%%%%%%%%%%%%%%%%

% % % figure (7);
% % % 
% % % b_avg = bar(x,([mem_pcolorfast_bar, NaN,mem_pcolormesh_bar, NaN,mem_matshow_bar, NaN,mem_imshow_bar,NaN]),"FaceColor","flat","BarWidth",0.4);
% % % hold on;
% % % b = bar(x,([NaN,peakmem_pcolorfast_bar,NaN, peakmem_pcolormesh_bar,NaN, peakmem_matshow_bar,NaN, peakmem_imshow_bar]),"FaceColor","flat","BarWidth",0.4);

%%%%%%%   Avg vs peak  %%%%%%%%%%%%%%
figure (8);
x = 1:4;
b_stem = stem(x,([peakmem_pcolorfast_bar, peakmem_pcolormesh_bar, peakmem_matshow_bar, peakmem_imshow_bar]),"black", "filled","Marker","o","MarkerSize",5); %,"FaceColor","flat","BarWidth",0.4);
hold on;
% colors = (["#2166AC","#AA3377","#DDCC77","#44BB99"]);
b_avg = bar(x,([mem_pcolorfast_bar, mem_pcolormesh_bar, mem_matshow_bar, mem_imshow_bar]),"FaceColor","flat","BarWidth",0.8,"BarLayout","grouped");
clrs = [33 102 172;
    170 68 153;
    221 204 119;
    68 187 153    
    ] / 255;
b_avg.CData = clrs;
b_avg.FaceAlpha=1; %%%%%%%%%%mem_50dpi

%% For dpi sizes:  (64x27)
mem_50dpi = results_mem(results_mem.dpi==50, :);
mem_100dpi = results_mem(results_mem.dpi==100, :);
mem_150dpi = results_mem(results_mem.dpi==150, :);
mem_200dpi = results_mem(results_mem.dpi==200, :);
%
mem_50dpi = (mem_50dpi.average_mem)/(1024^2);
mem_100dpi = (mem_100dpi.average_mem)/(1024^2);
mem_150dpi = (mem_150dpi.average_mem)/(1024^2);
mem_200dpi = (mem_200dpi.average_mem)/(1024^2);

mem_50dpi_bar = (sum(mem_50dpi(:,1))/64);
mem_100dpi_bar = (sum(mem_100dpi(:,1))/64);
mem_150dpi_bar = (sum(mem_150dpi(:,1))/64);
mem_200dpi_bar = (sum(mem_200dpi(:,1))/64);

% % %%  Plotting memory usage for every dpi
% % figure (9); 
% % fontname("Times New Roman");
% % fontsize(10,"points");
% % x = 1:4; % pcolorfast, pcolormesh, matshow, imshow
% % x1 = 1:3;
% % boxplot(([mem_50dpi,mem_100dpi, mem_150dpi, mem_200dpi]), x,"Widths", 0.8, 'Symbol','*-k');
% % % % boxplot(([mem_pcolorfast,mem_matshow,mem_imshow]), x1,"Widths", 0.8, 'Symbol','*-k');
% % 
% % hold on;
% % grid on;
% % 
% %     %Formatting:
% % h = findobj(gca,'Tag','Box');
% % patch(get(h(1),'XData'),get(h(1),'YData'), [(187/255) (228/255) (83/255)]); % Grass green #BBE453
% % patch(get(h(2),'XData'),get(h(2),'YData'), [(195/255) (168/255) (209/255)]); %lilac #C3A8D1
% % patch(get(h(3),'XData'),get(h(3),'YData'), [(255/255) (185/255) (84/255)]); % Orange juice #FFB954
% % patch(get(h(4),'XData'),get(h(4),'YData'), [(96/255) (188/255) (233/255)]); % light/ sky blue #60BCE9
% % 
% % %%%%%%%%%%%%%%%%% Bar graph:
% % %b_avg = bar(x,([mem_50dpi_bar, mem_100dpi_bar, mem_150dpi_bar, mem_200dpi_bar]),"FaceColor","flat","BarWidth",0.4);
% % % hold on;
% % % % Changing colour scheme:   blue,purple,sand, mint
% % % clr = [33 102 172;
% % %     170 68 153;
% % %     221 204 119;
% % %     68 187 153    
% % %     ] / 255;
% % % b_avg.CData = clr;
% % % b_avg.FaceAlpha=0.7;
% % 
% % %x-axis
% % xticklabels(["50 dpi", "100 dpi", "150 dpi", "200 dpi"]);
% % %y-axis
% % ylabel('Average Memory (MB)', "FontWeight","bold");
% % ylim([0, 100]);
% % %xtickangle(45);
% % fontname("Times New Roman");
% % xlabel('dpi used', "FontWeight","bold");
% % legend (["200 dpi", "150 dpi", "100 dpi", "50 dpi"], "Location","bestoutside","FontSize", 8)
