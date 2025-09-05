clear all
%% 读取landmask 构造经纬度
data = imread('h:\Fusion\Demo1_20210606\fromglc10v01_26_120.tif');
lonmin = 120;
lonmax = 122;
latmin = 26;
latmax = 28;
step = 2/22264;
lon = lonmin:step:lonmax;
lat = latmax:-step:latmin;
[lon,lat] = meshgrid(lon,lat);

%% 筛选区域，构建掩膜
lonmin = 120.5;
lonmax = 120.7;
latmin = 27.2;
latmax = 27.4;

[row,col] = size(lon);
IND = [];
for i = 1:col
    tmp = lon(:,i);
    if (min(tmp)>lonmax)||(max(tmp)<=lonmin)
        
    else
        IND = [IND;i];
    end
end
x = min(IND);
y = max(IND);

id1 = x:y-1;

IND = [];

for i = 1:row
    tmp = lat(i,:);
    if (min(tmp)>latmax)||(max(tmp)<latmin)
        
    else
        IND = [IND;i];
    end
end
m = min(IND);
n = max(IND);
id2 = m:n;

loni = lon(id2,id1);
lati = lat(id2,id1);
datai = double(data(id2,id1));

data(data==60) = 1;
data(data~=60) = 0;
%% 插值生成掩膜
step2 = 0.0005;
lon2 = lonmin:step2:lonmax;
lat2 = latmax:-step2:latmin;
[lon2,lat2] = meshgrid(lon2,lat2);

datai = griddata(loni,lati,data,lon2,lat2);

save landmask_CZI_20210606_50m datai

% figure
% image(datai)