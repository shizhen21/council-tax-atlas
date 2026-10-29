# Aggregate existing saved simulations by ORIGINAL band; never re-estimate policy rules.
args<-commandArgs(trailingOnly=TRUE);root<-normalizePath(args[1]);out<-file.path(root,'11_Website/council-tax-atlas/downloads')
base<-file.path(root,'ETR_1021/08_Policy_Simulation/results/Six_Policies_2022_2025_Upper_ETR')
for(yy in 2022:2025){
 e<-new.env();load(file.path(base,sprintf('year_%d/six_policies_transactions_%d.RData',yy,yy)),envir=e);z<-e$d;class(z)<-'data.frame';rm(e)
 stopifnot(all(z$band_original %in% LETTERS[1:8]),all(z$price>0),!anyNA(z$lsoa21cd),!anyNA(z$lad26cd))
 con<-gzfile(file.path(out,sprintf('reform_original_band_%d.csv.gz',yy)),'wt',compression=1);first<-TRUE
 for(k in 1:6){
  after<-z[[paste0('policy',k)]];delta<-after-z$tax
  sums<-cbind(n=1,bill_before=z$tax,bill_after=after,etr_before=100*z$tax/z$price,etr_after=100*after/z$price,more=as.integer(delta>.01),less=as.integer(delta< -.01))
  for(level in c('lad','lsoa','england')){
   area<-if(level=='lad')z$lad26cd else if(level=='lsoa')z$lsoa21cd else rep('England',nrow(z))
   v<-rowsum(sums,paste(area,z$band_original,sep='|'),reorder=TRUE)
   keys<-strsplit(rownames(v),'|',fixed=TRUE)
   df<-data.frame(level=level,code=vapply(keys,`[`,character(1),1),band=vapply(keys,`[`,character(1),2),year=yy,policy=k,n=v[,1],bill_before=v[,2]/v[,1],bill_after=v[,3]/v[,1],etr_before=v[,4]/v[,1],etr_after=v[,5]/v[,1],share_more=v[,6]/v[,1],share_less=v[,7]/v[,1])
   stopifnot(sum(df$n)==nrow(z),all(df$share_more+df$share_less<=1+1e-10))
   write.table(df,con,sep=',',row.names=FALSE,col.names=first,quote=TRUE,na='');first<-FALSE
  }
 }
 close(con);rm(z,sums);gc(FALSE);cat('Original-band reform results:',yy,'complete\n');flush.console()
}
