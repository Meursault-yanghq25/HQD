function vars = read_all_var(nc_path, nc_info, varargin)
%read_all_var 读nc所有变量
    if nargin == 3
        nc_var = nc_info.Variables;
        vars = varargin{1,1};% 批量生成变量
        for n = 1:size(vars,2)
            % vars{1,n} = varargin{n,1};
            vars{2,n} = ncread(nc_path,vars{1,n}); % 批量生成变量值
            % % eval([vars{1,n},'=','vars{2,n};']); %报错检查变量名合法性
        end
        disp(['vars in list were read']);
    elseif nargin == 4
        nc_var = nc_info.Variables;
        for n = varargin{1}:varargin{2}
            vars{1,n} = nc_var(n).Name;% 批量生成变量
            vars{2,n} = ncread(nc_path,vars{1,n}); % 批量生成变量值
            % eval([vars{1,n},'=','vars{2,n};']); %报错检查变量名合法性
        end
        disp(['No. ', num2str(varargin{1}), '-', ...
            num2str(varargin{2}), ' vars were  read'])
    elseif nargin == 2
        nc_var = nc_info.Variables;
        for n = 1:10
            vars{1,n} = nc_var(n).Name;% 批量生成变量
            vars{2,n} = ncread(nc_path,vars{1,n}); % 批量生成变量值
            % eval([vars{1,n},'=','vars{2,n};']); %报错检查变量名合法性
        end
        disp(['no begin/end No., first 10 vars were read']);
    end

end