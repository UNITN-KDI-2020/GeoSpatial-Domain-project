function [T] = count_json_b(input_file)
%COUNT_JSON Summary of this function goes here
%   Detailed explanation goes here
fileName = ['dataset\Data Integration\data\', input_file, '.json']; % filename in JSON extension


fid = fopen(fileName); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
val = jsondecode(str);
total=0;

end



