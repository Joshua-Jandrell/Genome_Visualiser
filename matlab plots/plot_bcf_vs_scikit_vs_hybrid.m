%% Benchmarking results: matplotlib Plotting & Memory usage
% Dynamic Genome Visualiser
% EIE Investigation 2024
% Plotting by Pragna Singh 2138875 (using results from Joshua Jandrell 2333213)

clear workspace
%% Reading in the data from the pre-uploaded cvs files:
    %For bcftools:
bcf_times = readtable('afr_bcftools_times.csv');

    %For scikit-allel:
scikit_times = readtable('afr_al_times.csv');

    %For the hybrid system:
hybrid_times = readtable('afr_hybrid_times.csv');
 
%Add each relevant Reading & filtering process-times together:

   %For bcftools:
            % 'Indexing'
            % 'Pos filtering' ---- ignore
            % 'Pos and qual filtering'
            % 'Case-control splitting'
            % 'One shot filter and split'
            % 'Read case and ctrl in to memory'
            % 'Total (separate operations)'
            % 'Total (one shot)'

indx_bcf = (bcf_times(strcmp(bcf_times.Operation, 'Indexing'), :).Average) + (bcf_times(strcmp(bcf_times.Operation, 'Read case and ctrl in to memory'), :).Average);

filt_bcf = (bcf_times(strcmp(bcf_times.Operation, 'Case-control splitting'), :).Average) + (bcf_times(strcmp(bcf_times.Operation, 'Pos and qual filtering'), :).Average);
filt_oneshot_bcf = bcf_times(strcmp(bcf_times.Operation, 'One shot filter and split'), :).Average;

tot_bcf_seperate_ops = bcf_times(strcmp(bcf_times.Operation, 'Total (separate operations)'), :).Average; %Faster to do it one-shot.
tot_bcf_oneshot = bcf_times(strcmp(bcf_times.Operation, 'Total (one shot)'), :).Average;

    %For scikit-allel:
            % 'Data reading'
            % 'Data reading (no tabix)' is faster than with tabix?! bruh the internet do be wrong ._.
            % 'DF reading'
            % 'Quality filtering'
            % 'Case file reading'
            % 'Case-control splitting'
            % 'Total'
read_scikit_data = (scikit_times(strcmp(scikit_times.Operation, 'Data reading'), :)); 
read_scikit_df = (scikit_times(strcmp(scikit_times.Operation, 'DF reading'), :));
read_scikit_cases = (scikit_times(strcmp(scikit_times.Operation, 'Case file reading'), :));

read_scikit = read_scikit_data.Average + read_scikit_df.Average + read_scikit_cases.Average;

filt_scikit_qual = (scikit_times(strcmp(scikit_times.Operation, 'Quality filtering'), :));
filt_scikit_casecntrl = (scikit_times(strcmp(scikit_times.Operation, 'Case-control splitting'), :));

filt_scikit = filt_scikit_qual.Average + filt_scikit_casecntrl.Average;

tot_scikit = scikit_times(strcmp(scikit_times.Operation, 'Total'), :);
tot_scikit = tot_scikit.Average;

   %For the hybrid system:
        % 'Indexing'
        % 'Read in to memory'
        % 'Read case and ctrl in to memory'
        %
        % 'Pos and qual filtering'
        % 'Case-control splitting'
        %
        % 'Total'
%

read_hybrid_mem = (hybrid_times(strcmp(hybrid_times.Operation, 'Read in to memory'), :).Average);
read_hybrid_casecntrl = (hybrid_times(strcmp(hybrid_times.Operation, 'Read case and ctrl in to memory'), :).Average);
read_hybrid_indx = (hybrid_times(strcmp(hybrid_times.Operation, 'Indexing'), :).Average);

filt_hybrid_posqual = (hybrid_times(strcmp(hybrid_times.Operation, 'Pos and qual filtering'), :).Average);
filt_hybrid_casesplit = (hybrid_times(strcmp(hybrid_times.Operation, 'Case-control splitting'), :).Average);

filt_hybrid = filt_hybrid_casesplit + filt_hybrid_posqual;
read_hybrid = read_hybrid_mem + read_hybrid_casecntrl + read_hybrid_indx;
tot_hybrid = hybrid_times(strcmp(hybrid_times.Operation, 'Total'), :).Average;


%% Plot comparisons as bar graph:
% bcf seperate commands, bcf oneshot commands, scikit allel, hybrid

figure (1);
x = 1:6;

totals_time = bar(x, ([tot_bcf_oneshot, NaN, NaN, NaN, NaN, NaN,]),"BarWidth",0.6,"FaceColor",'#262626','FaceAlpha',0.8); %, "Color",'#EE3377', "Marker", "+","LineWidth", 1.2, "LineStyle","--");% magenta #EE3377
hold on
totals_scikit_time = bar(x, ([NaN, NaN,  tot_scikit, NaN, NaN, NaN,]),"BarWidth",0.6,"FaceColor",'#8F8271','FaceAlpha',0.8); %, "Color",#8F8271 - scikit, "Marker", "+","LineWidth", 1.2, "LineStyle","--");% magenta #EE3377
totals_hybrid_time = bar(x, ([NaN, NaN,  NaN, NaN, tot_hybrid, NaN,]),"BarWidth",0.6,"FaceColor",'#2CC985','FaceAlpha',0.8); %, "Color",#2CC985 - visualiser app, "Marker", "+","LineWidth", 1.2, "LineStyle","--");% magenta #EE3377

read_stem = stem(([NaN, indx_bcf, NaN, read_scikit, NaN, read_hybrid]), "filled","LineWidth",0.7,"Color","black"); %,"BarWidth",0.6, "BarLayout","stacked"); %,"FaceColor","flat"); %,'FaceAlpha',0.8);% teal #009988 
filt_stem = stem(([NaN, filt_bcf, NaN,filt_scikit, NaN, filt_hybrid]), "LineWidth",0.7,"Color","black"); %,"BarWidth",0.6, "BarLayout","stacked"); %,"FaceColor","flat"); %,'FaceAlpha',0.8);% teal #009988 
%filt_stem = stem(([NaN, NaN, NaN, read_scikit, NaN, NaN]), "LineWidth",0.7,"Color","black"); %,"BarWidth",0.6, "BarLayout","stacked"); %,"FaceColor","flat"); %,'FaceAlpha',0.8);% teal #009988 

% filt_times = bar(x, ([NaN, (+read_bcf), NaN, NaN, (+read_scikit), NaN, NaN, (+read_hybrid)]),"BarWidth",0.6,"FaceColor",'#0077BB','FaceAlpha',0.4);% bluuue #0077BB

% readfilt(1).FaceColor = [(187/255) (228/255) (83/255)]; %Grass green #BBE453
% readfilt(2).FaceColor = [(195/255) (168/255) (209/255)]; % Lilac #C3A8D1

% readfilt(1).CData = [(187/255) (228/255) (83/255)]; %Grass green #BBE453
% readfilt(2).CData = [(195/255) (168/255) (209/255)]; % Lilac #C3A8D1

xticks([1.5 3.5 5.5]);
xticklabels({'bcftools', 'scikit-allel', 'hybrid'});
xlabel('Type of data retrival method');
ylabel('Time to complete process (s)');

fontname("Times New Roman");
fontsize(18, "points");
legend ({'total: bcf','total: scikit', 'total: hybrid', 'indexing','read-in file'}, "Location","best");
grid on;

%% Comparing numpy & pandas dataframe:
np_df_times = readtable('np_vs_pd_times.csv');

%%% For each column size: 
% 5 cols:
cols_5 = np_df_times(np_df_times.n_cols==5, :);
np_cols_5 = cols_5.np_time;
df_cols_5 = cols_5.df_time;

% 10 cols:
cols_10 = np_df_times(np_df_times.n_cols==10, :);
np_cols_10 = cols_10.np_time;
df_cols_10 = cols_10.df_time;

% 20 cols:
cols_20 = np_df_times(np_df_times.n_cols==20, :);
np_cols_20 = cols_20.np_time;
df_cols_20 = cols_20.df_time;

%%%% Plotting:
figure (2);
x = 1:5;
    %np:
np5 = semilogy(x, np_cols_5,"Color",'#EE3377', "Marker", "+","LineWidth", 1.2, "LineStyle","--");% magenta #EE3377
hold on
np10 = semilogy(x, np_cols_10,"Color",'#009988', "Marker", "+","LineWidth", 1.2, "LineStyle","--");% teal #009988 
np20 = semilogy(x, np_cols_20,"Color",'#0077BB', "Marker", "+","LineWidth", 1.2, "LineStyle","--");% bluuue #0077BB

%df:
df5 = semilogy(x, df_cols_5,"Color",'#CC3311', "Marker", "*","LineWidth", 1.7, "LineStyle","-"); % orange-red #CC3311
df10 = semilogy(x, df_cols_10,"Color",'#117733', "Marker", "x","LineWidth", 1.1, "LineStyle","-"); % green #117733
df20 = semilogy(x, df_cols_20,"Color",'#332288', "Marker", "x","LineWidth", 1.1, "LineStyle","-"); % indigo #332288

xticks(x);
xticklabels({'10', '100', '1000', '10000', '100000'});
xlabel('Number of rows');
set(gca,'yscale','log');
ylabel('Time taken to plot (s)');

fontname("Times New Roman");
fontsize(18, "points");
legend ({'np: 5 columns','np: 10 columns', 'np: 20 columns', 'df: 5 columns (fastest)','df: 10 columns', 'df: 20 columns'}, "Location","northwest");
grid on;



