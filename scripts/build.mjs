import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const data=JSON.parse(fs.readFileSync(path.join(root,"data/catalog.json"),"utf8"));
const template=fs.readFileSync(path.join(root,"template.html"),"utf8");
const embedded=JSON.stringify(data.items).replaceAll("</","<\\/");
fs.mkdirSync(path.join(root,"site"),{recursive:true});
fs.writeFileSync(path.join(root,"site/index.html"),template.replace("__CATALOG_ITEMS__",embedded));
fs.writeFileSync(path.join(root,"site/catalog.json"),JSON.stringify(data));
fs.writeFileSync(path.join(root,"site/_headers"),"/\n  Cache-Control: no-store\n/catalog.json\n  Cache-Control: no-store\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n");
console.log("選択画面を生成しました。候補："+data.complete+"人、試案："+data.drafts+"枚");

