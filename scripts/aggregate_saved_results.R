# Aggregate saved analysis inputs only. No models, new policy rules or input mutations.
args<-commandArgs(trailingOnly=TRUE);root<-normalizePath(args[1]);out<-file.path(root,'11_Website/council-tax-atlas/downloads');dir.create(out,recursive=TRUE,showWarnings=FALSE)
writegz<-function(x,name){con<-gzfile(file.path(out,paste0(name,'.csv.gz')),'wt',compression=1);write.csv(x,con,row.names=FALSE,na='');close(con)}
base<-file.path(root,'ETR_1021/07_Current_ETR_Suits');current<-file.path(base,'results/ETR_Upper_Trim_0.5pct');annual<-read.csv(file.path(current,'Annual_ETR_And_Suits.csv'))
history<-list();bands<-list();checks<-list()
for(yy in 1995:2025){
 e<-new.env();load(file.path(base,sprintf('data/Annual_Inputs/Observed_Tax_%d.RData',yy)),envir=e);z<-e$tax_data;class(z)<-'data.frame';rm(e)
 excluded<-read.csv(file.path(current,sprintf('Excluded_Upper_ETR_%d.csv',yy)));z<-z[!z$ppd_row_id %in% excluded$ppd_row_id,]
 stopifnot(nrow(z)==annual$n[annual$year==yy],!anyNA(z$lsoa21cd),all(abs(z$etr-z$tax/z$price)<1e-10))
 v<-rowsum(cbind(n=rep(1,nrow(z)),bill=z$tax,etr=100*z$etr),z$lsoa21cd,reorder=TRUE)
 history[[as.character(yy)]]<-data.frame(year=yy,lsoa21cd=rownames(v),n=v[,1],mean_bill=v[,2]/v[,1],mean_etr_pct=v[,3]/v[,1])
 b<-as.data.frame(table(band=z$council_tax_band),stringsAsFactors=FALSE);b$year<-yy;bands[[as.character(yy)]]<-b
 checks[[as.character(yy)]]<-data.frame(year=yy,n=nrow(z),n_sum=sum(v[,1]),total_tax=sum(z$tax),mean_etr_pct=mean(100*z$etr),lsoa_count=nrow(v))
 rm(z,excluded,v);gc(FALSE);cat('History aggregated:',yy,'\n');flush.console()
}
writegz(do.call(rbind,history),'lsoa_current_1995_2025');writegz(do.call(rbind,bands),'selected_transaction_band_shares');writegz(do.call(rbind,checks),'history_checks');rm(history,bands);gc(FALSE)
pbase<-file.path(root,'ETR_1021/08_Policy_Simulation/results/Six_Policies_2022_2025_Upper_ETR');pol<-list();ladpol<-list();links<-list();localbands<-list();transitions<-list()
for(yy in 2022:2025){
 e<-new.env();load(file.path(pbase,sprintf('year_%d/six_policies_transactions_%d.RData',yy,yy)),envir=e);z<-e$d;class(z)<-'data.frame';rm(e)
 expected<-annual$n[annual$year==yy];stopifnot(nrow(z)==expected)
 links[[as.character(yy)]]<-unique(z[c('lsoa21cd','lad26cd')])
 for(k in 1:6){
  after<-z[[paste0('policy',k)]];delta<-after-z$tax;stopifnot(all(is.finite(after)))
  for(level in c('lsoa21cd','lad26cd')){
   v<-rowsum(cbind(n=rep(1,nrow(z)),before=z$tax,after=after,etrbefore=100*z$tax/z$price,etrafter=100*after/z$price,more=as.integer(delta>.01),less=as.integer(delta< -.01),same=as.integer(abs(delta)<=.01)),z[[level]],reorder=TRUE)
   df<-data.frame(code=rownames(v),year=yy,policy=k,n=v[,1],mean_bill_before=v[,2]/v[,1],mean_bill_after=v[,3]/v[,1],mean_etr_before=v[,4]/v[,1],mean_etr_after=v[,5]/v[,1],share_more=v[,6]/v[,1],share_less=v[,7]/v[,1],share_same=v[,8]/v[,1])
   if(level=='lsoa21cd')pol[[paste(yy,k)]]<-df else ladpol[[paste(yy,k)]]<-df
  }
 }
 for(bandtype in c('band_original','band_new')){
  t<-as.data.frame(table(lad26cd=z$lad26cd,band=z[[bandtype]]),stringsAsFactors=FALSE);t$year<-yy;t$type<-bandtype;localbands[[paste(yy,bandtype)]]<-t
 }
 t<-as.data.frame(table(original=z$band_original,new=z$band_new),stringsAsFactors=FALSE);t$year<-yy;transitions[[as.character(yy)]]<-t
 cat('Policy aggregates:',yy,'\n');flush.console();rm(z);gc(FALSE)
}
writegz(do.call(rbind,pol),'lsoa_policy_2022_2025');writegz(do.call(rbind,ladpol),'lad_policy_2022_2025');writegz(unique(do.call(rbind,links)),'lsoa_lad_links');writegz(do.call(rbind,localbands),'lad_band_counts');writegz(do.call(rbind,transitions),'reband_transitions')
cat('Saved aggregate-only website tables.\n')
