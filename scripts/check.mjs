import{readFile,readdir,stat}from'node:fs/promises';import{dirname,join,relative,resolve}from'node:path';
const root=process.cwd();
const walk=async dir=>(await Promise.all((await readdir(dir,{withFileTypes:true})).filter(entry=>entry.name!=='dist'&&entry.name!=='.git').map(async entry=>entry.isDirectory()?walk(join(dir,entry.name)):join(dir,entry.name)))).flat();
const htmlFiles=(await walk(root)).filter(file=>file.endsWith('.html')),errors=[];
for(const file of htmlFiles){const html=await readFile(file,'utf8');if(!/<title>.+<\/title>/.test(html))errors.push(`${relative(root,file)}: missing title`);if(!/meta name="description"/.test(html)&&!file.endsWith('404.html'))errors.push(`${relative(root,file)}: missing description`);for(const match of html.matchAll(/(?:href|src)="([^"#?]+)"/g)){const target=match[1];if(/^(https?:|mailto:|data:)/.test(target))continue;const path=resolve(dirname(file),target);try{await stat(path)}catch{errors.push(`${relative(root,file)}: broken local reference ${target}`)}}}
if(errors.length){console.error(errors.join('\n'));process.exit(1)}console.log(`Checked ${htmlFiles.length} HTML pages: all local references resolve.`);
