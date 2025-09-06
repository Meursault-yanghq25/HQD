clc,clear;
%% input/output
nc_folder = 'F:\water_para';
shp_file = "E:/AAAAA/HQD/land_mask/FAB_final_land_mask.shp";
output_folder = "F:\water_para_masked";
%
%% out dir check
if ~exist(output_folder,'dir')
    mkdir(output_folder);
    disp(['make outpath: ',output_folder])
else
    disp(["exist outpath:",output_folder])
end
% 
%% nc list
ncfile = struct2table(dir([nc_folder,'\*.nc']));
nc_path = fullfile(ncfile.folder, ncfile.name);
nc_path = nc_path{1,:}; %!! for test only!!

% 
%% check & create mask tif
mask_sample_nc = [nc_folder,'\',string(ncfile{1,1})];
mask_sample_nc = [mask_sample_nc{:}];
mask_tif_file = [output_folder,'\mask.tif'];
mask_tif_file = [mask_tif_file{:}];
%-----------------------%!! 根据实际nc修改----------------------
Lon = ncread(mask_sample_nc, 'xgrid');  
Lat = ncread(mask_sample_nc, 'ygrid'); 
lon = Lon(1,:)';
lat = Lat(:,1);
%-------------------------------------------------------------

disp(['fichier de masque par défaut: ',mask_tif_file]);
if ~exist(mask_tif_file,'file')
    disp(["Aucun masque tif n'existe! Générer maintenant…"]);
    cover_value = 0;
    create_mask_from_shp_nc(shp_file, lat, lon, mask_tif_file, cover_value);
else
    disp(['existe la masque tif: ', mask_tif_file])
end
% 
%% mask nc by tif
exclude_vars = {'xgrid','ygrid','x','y','lat','lon','time'};
apply_mask_folder(mask_tif_file, nc_folder, output_folder, ...
                    'exclude_vars', exclude_vars, 'flip_mask', true)
% 