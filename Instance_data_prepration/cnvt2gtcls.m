% converts a png ground trith to .map
function GTcls=cnvt2gtcls(fname)

     seg=imread(fname);
     seg=rgb2gray(seg);

     GTcls.Boundaries=cell(0);
     GTcls.Segmentation=uint8(zeros(size(seg)));
     GTcls.CategoriesPresent=uint8([]); 
     ObjNumber=0;
     categoriesList=sort(unique(seg),'ascend');
     for it=1:size(categoriesList,1)
         ctg=uint8(categoriesList(it));
         if(ctg~=0)
             CC = bwconncomp(seg==ctg);% connected components analysis
             imgb=zeros(CC.ImageSize);
             for obj=1:CC.NumObjects
                 pixelsIndex=CC.PixelIdxList{obj};
                 imgb(pixelsIndex)=1;
             end
	         bnd = bwboundaries(imgb);
             imgb2=zeros(CC.ImageSize);
             imgb2(sub2ind(CC.ImageSize,bnd{1}(:,1),bnd{1}(:,2)))=1;
             ObjNumber=ObjNumber+1;
             GTcls.Boundaries{1,1}=sparse(imgb2);
             %GTcls.Boundaries{ctg,1}=sparse(imgb2);
	         GTcls.Segmentation(imgb2>0)=ctg;
	         GTcls.CategoriesPresent=[GTcls.CategoriesPresent;ctg];
         end
     end
    
end
