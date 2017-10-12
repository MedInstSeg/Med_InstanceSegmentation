% converts a png ground trith to .map
function GTinst=cnvt2gtinst(fname)


     seg=imread(fname);

     seg=rgb2gray(seg);
     GTinst.Segmentation=zeros(size(seg));
     GTinst.Boundaries=cell(0);
     GTinst.Categories=[]; 
     ObjNumber=0;
     categoriesList=sort(unique(seg),'ascend');
     for it=1:size(categoriesList,1)
         ctg=categoriesList(it);
         if(ctg~=0)
             CC = bwconncomp(seg==ctg);% connected components analysis
             for obj=1:CC.NumObjects
                 imgb=zeros(CC.ImageSize);
                 pixelsIndex=CC.PixelIdxList{obj};
                 imgb(pixelsIndex)=1;
		         bnd = bwboundaries(imgb);
                 imgb2=zeros(CC.ImageSize);
                 imgb2(sub2ind(CC.ImageSize,bnd{1}(:,1),bnd{1}(:,2)))=1;
                 ObjNumber=ObjNumber+1;
                 GTinst.Segmentation((pixelsIndex))=ObjNumber;
                 %GTinst.Boundaries{ObjNumber,1}=sparse(imgb2);
                 GTinst.Boundaries{ObjNumber,1}=sparse(imgb2);
                 
                 GTinst.Categories=[GTinst.Categories;double(ctg)];
		        
             end
         end
     end
end
