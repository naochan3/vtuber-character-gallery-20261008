import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"../site");
const mime={".html":"text/html; charset=utf-8",".json":"application/json; charset=utf-8",".png":"image/png",".css":"text/css",".js":"text/javascript"};
const server=http.createServer((req,res)=>{
 let name;
 try{name=decodeURIComponent(new URL(req.url,"http://127.0.0.1").pathname)}catch{res.writeHead(400).end();return}
 const file=path.resolve(root,"."+name+(name.endsWith("/")?"index.html":""));
 if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return}
 fs.stat(file,(error,stat)=>{
  if(error||!stat.isFile()){res.writeHead(404).end();return}
  res.writeHead(200,{"Content-Type":mime[path.extname(file)]||"application/octet-stream","Cache-Control":"no-store"});
  if(req.method==="HEAD"){res.end();return}
  fs.createReadStream(file).pipe(res);
 });
});
server.listen(8792,"127.0.0.1",()=>console.log("選択画面：http://127.0.0.1:8792"));

