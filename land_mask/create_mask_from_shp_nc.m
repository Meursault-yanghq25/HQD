function create_mask_from_shp(shp_file, lat, lon, output_file, cover_value)
% CREATE_MASK_FROM_SHP - Générer un masque binaire à partir d'un shapefile et d'une grille lat/lon
% avec progress bar pour chaque sous-polygone et estimation du temps restant
%
% Usage :
%   create_mask_from_shp(shp_file, lat, lon, output_file, cover_value)
%
% Paramètres :
%   shp_file    - chemin du shapefile (.shp)
%   lat, lon    - vecteurs latitude et longitude (issus du NetCDF)
%   output_file - chemin de sortie GeoTIFF
%   cover_value - valeur attribuée à la zone couverte par shapefile (0 ou 1)

    if nargin < 5
        cover_value = 0; % 默认：shapefile 区域=0
    end

    %% 1. 读取 shapefile
    fprintf('Lecture du fichier shapefile : %s\n', shp_file);
    shp = shaperead(shp_file);

    %% 2. 初始化掩膜
    nlat = length(lat);
    nlon = length(lon);
    mask = ones(nlat, nlon) * (1 - cover_value);

    %% 3. 统计总子多边形数量（拆分 NaN）
    total_subpoly = 0;
    for k = 1:numel(shp)
        nan_idx = isnan(shp(k).X) | isnan(shp(k).Y);
        start_idx = [1 find(nan_idx)+1];
        end_idx   = [find(nan_idx)-1 length(shp(k).X)];
        total_subpoly = total_subpoly + length(start_idx);
    end

    fprintf('Conversion du shapefile en masque raster ... Total sous-polygons : %d\n', total_subpoly);

    %% 4. 遍历每个子多边形，生成掩膜 + 进度条
    h = waitbar(0, 'Traitement des sous-polygons...', 'Name', 'Création du masque');
    subpoly_count = 0;
    tic; % 计时开始

    for k = 1:numel(shp)
        x_poly = shp(k).X;
        y_poly = shp(k).Y;

        % 拆分含 NaN 的子多边形
        nan_idx = isnan(x_poly) | isnan(y_poly);
        start_idx = [1 find(nan_idx)+1];
        end_idx   = [find(nan_idx)-1 length(x_poly)];

        for j = 1:length(start_idx)
            x = x_poly(start_idx(j):end_idx(j));
            y = y_poly(start_idx(j):end_idx(j));
            if isempty(x) || isempty(y)
                continue;
            end

            % 映射到像素行列
            x_img = (x - min(lon)) / (max(lon) - min(lon)) * (nlon - 1) + 1;
            y_img = (y - min(lat)) / (max(lat) - min(lat)) * (nlat - 1) + 1;

            % 生成 polygon mask
            BW = poly2mask(x_img, y_img, nlat, nlon);

            % 更新掩膜
            mask(BW) = cover_value;

            % 更新进度条和剩余时间估算
            subpoly_count = subpoly_count + 1;
            elapsed = toc;
            avg_time = elapsed / subpoly_count;
            remaining_time = avg_time * (total_subpoly - subpoly_count);
            remaining_min = floor(remaining_time/60);
            remaining_sec = round(mod(remaining_time,60));

            waitbar(subpoly_count/total_subpoly, h, ...
                sprintf('Sous-polygon %d / %d - \nTemps restant estimé : %d min %d sec', ...
                        subpoly_count, total_subpoly, remaining_min, remaining_sec));
        end
    end
    close(h); % 关闭进度条

    %% 5. 保存为 GeoTIFF
    fprintf('Sauvegarde du masque en GeoTIFF : %s\n', output_file);
    R = georasterref('RasterSize', size(mask), ...
                     'LatitudeLimits', [min(lat) max(lat)], ...
                     'LongitudeLimits', [min(lon) max(lon)], ...
                     'RasterInterpretation', 'cells');
    geotiffwrite(output_file, mask, R);

    fprintf('Sauvegarde terminée : %s créé avec succès !\n', output_file);
end
