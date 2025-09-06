function apply_mask_file(mask_tif_file, nc_file_in, nc_file_out, varargin)
% APPLY_MASK_FILE - 对 NC 文件中所有变量应用掩膜（二维/三维）并保存为新文件
%
% 用法：
%   apply_mask_file(mask_tif_file, nc_file_in, nc_file_out, ...
%                   'exclude_vars', {'lat','lon'}, 'flip_mask', true)
%
% 输入参数：
%   mask_tif_file - 掩膜 tif 文件路径
%   nc_file_in    - 输入 NC 文件路径
%   nc_file_out   - 输出 NC 文件路径
%
% 可选参数：
%   'exclude_vars' - cell array, 排除的变量名（默认空）
%   'flip_mask'    - logical, 是否上下翻转 mask (默认 false)

p = inputParser;
addParameter(p,'exclude_vars',{},@iscell);
addParameter(p,'flip_mask',false,@islogical);
parse(p,varargin{:});

exclude_vars = p.Results.exclude_vars;
flip_mask = p.Results.flip_mask;

%% 读取掩膜
fprintf('Lecture du masque : %s\n', mask_tif_file);
[mask, R] = readgeoraster(mask_tif_file);
mask = double(mask);

if flip_mask
    mask = flipud(mask); % 上下翻转
end
mask(mask==0) = NaN; % 掩膜 0 → NaN

%%  复制输入文件到输出文件
copyfile(nc_file_in, nc_file_out);
fprintf('Copie du fichier original vers : %s\n', nc_file_out);


%%  获取 NC 文件中所有变量
info = ncinfo(nc_file_in);
all_vars = {info.Variables.Name};

% 排除变量
vars_to_process = setdiff(all_vars, exclude_vars);

nVars = length(vars_to_process);

fprintf('Traitement de %d variables...\n', length(vars_to_process));
%% 初始化进度条
start_time = tic;

for v = 1:nVars
    % 处理变量
    process_var_file(nc_file_out, vars_to_process{v}, mask);
    
    % 进度和时间提示
    elapsed = toc(start_time);
    avg_time = elapsed / v;
    remaining = avg_time * (nVars - v);
    percent = v / nVars * 100;
    
    % 显示进度条
    bar_len = 30; % 进度条长度
    filled_len = round(bar_len * percent / 100);
    bar_str = ['[', repmat('=',1,filled_len), repmat(' ',1,bar_len-filled_len), ']'];
    
    fprintf('\r%s %3.0f%% | Temps écoulé %.1f s, Temps restant estimé %.1f s', ...
        bar_str, percent, elapsed, remaining);
end

fprintf('\nFichier traité et sauvegardé : %s\n', nc_file_out);

end

%% 子函数：处理单个变量并保存到输出文件
function process_var_file(nc_file_out, varname, mask)
fprintf('\nTraitement de la variable : %s\n', varname);

data = ncread(nc_file_out, varname);
dims = ndims(data);

if dims == 2
    data(isnan(mask)) = NaN;
elseif dims == 3
    % 假设三维为 lat x lon x time 
    %-----------!! 调整维度匹配 --------------------------
    ntime = size(data,3);
    mask3D = repmat(mask, [1,1,ntime]);
    mask3D = permute(mask3D,[1,2,3]);  %!! 调整维度匹配 
    data(isnan(mask3D)) = NaN;
    %---------------------------------------------------
else
    warning('变量 %s 维度不是 2 或 3，跳过', varname);
    return
end

% 保存回输出 NC 文件
ncwrite(nc_file_out, varname, data);

end
