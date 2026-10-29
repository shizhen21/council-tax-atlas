args<-commandArgs(trailingOnly=TRUE);root<-normalizePath(args[1]);base<-file.path(root,'ETR_1021');out<-file.path(root,'11_Website/council-tax-atlas/downloads')
writegz<-function(x,name){con<-gzfile(file.path(out,paste0(name,'.csv.gz')),'wt',compression=1);write.csv(x,con,row.names=FALSE,na='');close(con)}
e<-new.env();load(file.path(base,'08_Policy_Simulation/data/Reference/ONSPD_AUG2026_policy_lookup.RData'),envir=e);z<-e$postcode_2026;class(z)<-'data.frame';u<-unique(z[c('lsoa21cd','lad26cd')]);rm(e,z);u<-u[!is.na(u$lsoa21cd)&grepl('^E',u$lsoa21cd)&grepl('^E',u$lad26cd),];count<-table(u$lsoa21cd);unique_links<-u[as.integer(count[u$lsoa21cd])==1,];writegz(unique_links,'official_lsoa_lad_unique_links');lookup<-setNames(unique_links$lad26cd,unique_links$lsoa21cd);rm(u);gc(FALSE)
current<-file.path(base,'07_Current_ETR_Suits/results/ETR_Upper_Trim_0.5pct');annual<-read.csv(file.path(current,'Annual_ETR_And_Suits.csv'));stats<-list();bands<-list();checks<-list();lsoabands<-list()
for(yy in 1995:2025){
 e<-new.env();load(file.path(base,sprintf('07_Current_ETR_Suits/data/Annual_Inputs/Observed_Tax_%d.RData',yy)),envir=e);z<-e$tax_data;class(z)<-'data.frame';rm(e);excluded<-read.csv(file.path(current,sprintf('Excluded_Upper_ETR_%d.csv',yy)));z<-z[!z$ppd_row_id %in% excluded$ppd_row_id,];stopifnot(nrow(z)==annual$n[annual$year==yy])
 key<-paste(z$lsoa21cd,z$council_tax_band,sep='|');b<-table(key);parts<-strsplit(names(b),'|',fixed=TRUE);lsoabands[[as.character(yy)]]<-data.frame(year=yy,lsoa21cd=vapply(parts,'[',character(1),1),band=vapply(parts,'[',character(1),2),n=as.integer(b))
 z$lad26cd<-unname(lookup[z$lsoa21cd]);ok<-!is.na(z$lad26cd);checks[[as.character(yy)]]<-data.frame(year=yy,total=nrow(z),mapped=sum(ok),unresolved=sum(!ok));z<-z[ok,]
 v<-rowsum(cbind(n=rep(1,nrow(z)),bill=z$tax,etr=100*z$etr),z$lad26cd,reorder=TRUE);stats[[as.character(yy)]]<-data.frame(year=yy,lad26cd=rownames(v),n=v[,1],mean_bill=v[,2]/v[,1],mean_etr_pct=v[,3]/v[,1])
 b<-as.data.frame(table(lad26cd=z$lad26cd,band=z$council_tax_band),stringsAsFactors=FALSE);b$year<-yy;bands[[as.character(yy)]]<-b
 cat('Local explorer aggregated:',yy,'\n');flush.console();rm(z,excluded,v,b,parts,key);gc(FALSE)
}
writegz(do.call(rbind,stats),'lad_current_fixed2026_1995_2025');writegz(do.call(rbind,bands),'lad_band_counts_1995_2025');writegz(do.call(rbind,lsoabands),'lsoa_band_counts_1995_2025');writegz(do.call(rbind,checks),'lad_harmonisation_coverage');cat('Local explorer data complete.\n')
