import{cp,mkdir,rm}from'node:fs/promises';import{join}from'node:path';
const root=process.cwd(),dist=join(root,'dist');
const files=['index.html','blog.html','books.html','about.html','404.html','styles.css','script.js','favicon.svg','site.webmanifest','robots.txt','sitemap.xml','feed.xml','posts'];
await rm(dist,{recursive:true,force:true});await mkdir(dist,{recursive:true});for(const file of files)await cp(join(root,file),join(dist,file),{recursive:true});console.log(`Built ${files.length} publishing entries in dist/`);
