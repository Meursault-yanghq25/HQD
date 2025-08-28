clc,clear;
%% io
filepath = 'F:\water_para';
disp(['filepath: ', filepath]);
%

%% ncinfo
ncfile = struct2table(dir([filepath,'\*.nc']));
ncfile = ncfile(:,1);
disp(['ncfile: ', num2str(size(ncfile,1))]);
 % read_all_var(info)
for n = 1:size(ncfile,1)
    ncname = char(ncfile{n,1});
    disp({ncname});
    vars{1,n} = ['nc_',ncname(1:end-3)]; % 批量生成变量
    vars{2,n} = ncinfo([filepath,'\',ncname]);  % 批量生成变量值
    eval([vars{1,n},'=','vars{2,n};']); %报错检查变量名合法性
end
%

%% check var
nc = [filepath,'\',string(ncfile{4,1})];
nc = [nc{:}];
nc_info = ncinfo(nc);
begin_n = 1;
end_n = 5;
% vars = read_all_var(nc, nc_info, begin_n,end_n);
% for n = begin_n:end_n
%     eval([vars{1,n},'=','vars{2,n};']); %报错检查变量名合法性
% end
aa1 = ncread(nc, 'xgrid');
aa2 = ncread(nc, 'ygrid');
aa3 = ncread(nc, 'depth');
pcolor(aa1,aa2,aa3);
shading flat
colorbar
clim([0 50])
% % aa3 = aa3';
% nc = [filepath,'\',string(ncfile{2,1})];
% nc = [nc{:}];
% aa1 = ncread(nc, 'time');
% % aa2 = ncread(nc, 'Itime2');
% bb3 = ncread(nc, 'Times');
% bb3 = bb3';