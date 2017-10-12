function Main
 
fId=dir('Y:\PhD-research\DataSet\Instance-Data\Liver\CT\Training\GT\*.png');
for i = 1 : length(fId)
 
    filename = strcat('Y:\PhD-research\DataSet\Instance-Data\Liver\CT\Training\GT\',fId(i).name);
    [pathstr,name,ext] = fileparts(filename);
 
    GTcls=cnvt2gtcls(filename);
    savename= strcat('Y:\PhD-research\DataSet\Instance-Data\Liver\CT\Training/cls/',name,'.mat');
    save(savename,'GTcls');
    
    GTinst=cnvt2gtinst(filename);
    savename= strcat('Y:\PhD-research\DataSet\Instance-Data\Liver\CT\Training/inst/',name,'.mat');
    save(savename,'GTinst');  
       
end
end