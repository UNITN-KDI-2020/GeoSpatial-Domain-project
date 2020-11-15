function [T] = count_json(input_file)
%COUNT_JSON Summary of this function goes here
%   Detailed explanation goes here
fileName = ['dataset\Informal Modeling\data\', input_file, '.geojson']; % filename in JSON extension


fid = fopen(fileName); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
val = jsondecode(str);
total=0;
for i=1:size(val.features,1)
    temp=fieldnames(val.features(i).properties);
    for j=1:size(temp,1)
        if(i==1 && j==1)
            check(1)=temp(j);
            check_num(1)=1;
        else
            check_vect=ismember(check,temp(j));
            if(sum(check_vect)==0)
               check(size(check,2)+1)=temp(j);
               check_num(size(check,2))=1;
            else
                ind=find(check_vect);
                check_num(ind)=check_num(ind)+1;
            end
        end
    end
    total=size(val.features,1);
    
outtable=check';
for i=1:size(outtable,1)
    outtable{i,2}=check_num(1,i);
    outtable{i,3}=outtable{i,2}/total*100;
end
T = cell2table(outtable,'VariableNames',{'Name' 'Count' 'Percentual'});
name=['dataset\Informal Modeling\metadata\count_',input_file,'.csv'];
writetable(T,name);
end



