function apply_mask_folder(mask_tif_file, input_folder, output_folder, varargin)
% APPLY_MASK_FOLDER - 对输入文件夹下所有 NC 文件应用掩膜并保存到输出文件夹
% 带总进度条和总剩余时间估算
%
% 用法：
%   apply_mask_folder(mask_tif_file, input_folder, output_folder, ...
%                     'exclude_vars', {'lat','lon','time'}, 'flip_mask', true)
%
% 输入参数：
%   mask_tif_file  - 掩膜 tif 文件路径
%   input_folder   - 包含 NC 文件的输入文件夹
%   output_folder  - 输出文件夹
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

%% 创建输出文件夹
if ~exist(output_folder,'dir')
    mkdir(output_folder);
end

%% 获取输入文件夹下所有 NC 文件
nc_files = dir(fullfile(input_folder,'*.nc'));
nFiles = length(nc_files);
fprintf('%d fichiers NC trouvés dans le dossier %s\n', nFiles, input_folder);

%% 初始化总进度计时
total_start = tic;

%% 循环处理每个文件
for k = 1:nFiles
    nc_in = fullfile(input_folder, nc_files(k).name);
    [~, name, ext] = fileparts(nc_files(k).name);
    nc_out = fullfile(output_folder, [name '_masked' ext]);
    
    if exist(nc_out, 'file')
        fprintf('\nFichier existant, saut : %s\n', nc_files(k).name);
        continue;
    end
    
    fprintf('\n Traitement du fichier %d/%d : %s\n', k, nFiles, nc_files(k).name);
    
    % 处理单个文件
    file_start = tic;
    apply_mask(mask_tif_file, nc_in, nc_out, ...
                    'exclude_vars', exclude_vars, ...
                    'flip_mask', flip_mask);
    file_elapsed = toc(file_start);
    
    % 总进度条和剩余时间估算
    elapsed_total = toc(total_start);
    avg_time_per_file = elapsed_total / k;
    remaining_total = avg_time_per_file * (nFiles - k);
    
    percent_total = k / nFiles * 100;
    bar_len = 30;
    filled_len = round(bar_len * percent_total / 100);
    bar_str = ['[', repmat('=',1,filled_len), repmat(' ',1,bar_len-filled_len), ']'];
    
    fprintf('\r%s %3.0f%% | Temps écoulé %.1f s, Temps restant estimé %.1f s\n', ...
            bar_str, percent_total, elapsed_total, remaining_total);
end

fprintf('\nTous les fichiers ont été traités et sauvegardés dans %s\n', output_folder);

end
