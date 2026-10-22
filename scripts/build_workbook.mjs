import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const previewDir=await fs.mkdtemp(path.join(os.tmpdir(),'thirstyai-workbook-')); 
const data=JSON.parse(await fs.readFile(root+'/dist/data/evidence.json','utf8'));
const w=Workbook.create();const calc=w.worksheets.add('Calculator');const india=w.worksheets.add('India');const sources=w.worksheets.add('Sources');
for(const s of [calc,india,sources]){s.showGridLines=false;s.getRange('A1:J55').format.font={name:'Arial',size:11,color:'#18303D'};s.getRange('A1:J55').format.rowHeight=23;}
calc.getRange('A2').values=[['ThirstyAI operational water calculator']];calc.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#163746'};
calc.getRange('A4').values=[['Editable inputs are illustrative. Consumption only. Manufacturing excluded.']];
calc.getRange('A6:C6').values=[['Input','Value','Unit']];calc.getRange('A7:C11').values=[['IT workload',1000,'MWh'],['PUE',1.2,'facility kWh / IT kWh'],['Direct consumptive WUE',1,'L / IT kWh'],['Grid water factor',1,'L / facility kWh'],['Grid carbon factor',.4,'kg CO2e / facility kWh']];
calc.getRange('B7:B11').format.fill='#FFF1CF';calc.getRange('B7:B11').setNumberFormat('#,##0.00');
calc.getRange('E6:G6').values=[['Output','Value','Unit']];
const valid='AND(COUNT($B$7:$B$11)=5,$B$7>=0,$B$8>=1,MIN($B$9:$B$11)>=0)';
const formulas=['$B$7*$B$8','$B$7*1000*$B$9','$F$7*1000*$B$10','$F$8+$F$9','$F$7*1000*$B$11'];
const labels=['Facility energy','Direct consumption','Indirect consumption','Total consumption','Operational carbon'];const units=['MWh','L','L','L','kg CO2e'];
for(let i=0;i<5;i++){calc.getRange(`E${i+7}`).values=[[labels[i]]];calc.getRange(`F${i+7}`).formulas=[[`=IF(${valid},${formulas[i]},"Invalid input")`]];calc.getRange(`G${i+7}`).values=[[units[i]]];}
calc.getRange('F7:F11').setNumberFormat('#,##0.00');
calc.getRange('A14').values=[['Method: facility energy = IT energy × PUE; direct water = IT kWh × WUE.']];
calc.getRange('A15').values=[['Indirect water = facility kWh × grid water factor. Volumes may arise in different basins.']];
calc.getRange('A17').values=[['Do not substitute withdrawal WUE or factors already including indirect water.']];
calc.getRange('A18').values=[['Inputs have no empirical source: user-selected assumptions for exploration.']];
calc.getRange('A19').values=[['Use the web decision lab for simultaneous baseline/alternative and future scenarios.']];
calc.getRange('A:A').format.columnWidth=30;calc.getRange('B:B').format.columnWidth=14;calc.getRange('C:C').format.columnWidth=28;calc.getRange('D:D').format.columnWidth=3;calc.getRange('E:E').format.columnWidth=24;calc.getRange('F:F').format.columnWidth=18;calc.getRange('G:G').format.columnWidth=12;
india.getRange('A2').values=[['India groundwater assessment 2025']];india.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#163746'};
india.getRange('A3').values=[['Source: CGWB / PIB, 18 Dec 2025, Annexure I. Annual flows, all uses.']];
india.getRange('A4').values=[['Stage is reported, not recalculated from rounded volumes. This is not AI-attributed extraction.']];
const headers=['State / UT','Recharge BCM/year','Extractable BCM/year','Extraction BCM/year','Stage (%)','Year','Source ID'];
india.getRange('A6:G42').values=[headers,...data.india.map(r=>[r.state,r.recharge_bcm,r.extractable_bcm,r.extraction_bcm,r.stage_pct,r.year,r.source_id])];india.getRange('B7:E42').setNumberFormat('#,##0.00');india.getRange('F7:F42').setNumberFormat('0');india.getRange('A:A').format.columnWidth=52;india.getRange('B:D').format.columnWidth=24;india.getRange('E:G').format.columnWidth=17;india.freezePanes.freezeRows(6);
sources.getRange('A2').values=[['Primary source register']];sources.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#163746'};
sources.getRange('A5:D11').values=[['ID','Publisher','URL','Locator'],...data.sources.map(s=>[s.id,s.publisher,s.url,s.locator])];sources.getRange('A:A').format.columnWidth=15;sources.getRange('B:B').format.columnWidth=39;sources.getRange('C:C').format.columnWidth=65;sources.getRange('D:D').format.columnWidth=65;sources.getRange('C6:D11').format.wrapText=true;sources.getRange('A6:D11').format.rowHeight=62;
for(const [s,r] of [[calc,'A6:C6'],[calc,'E6:G6'],[india,'A6:G6'],[sources,'A5:D5']]){s.getRange(r).format={fill:'#203D4B',font:{name:'Arial',bold:true,color:'#FFFFFF'},rowHeight:30};}
w.recalculate();const vals=calc.getRange('F7:F11').values.map(r=>r[0]);if(vals[3]!==2200000)throw new Error('Workbook parity failed: '+JSON.stringify(vals));
calc.getRange('B7').values=[[2000]];w.recalculate();if(calc.getRange('F10').values[0][0]!==4400000)throw new Error('Input change did not recalculate');
calc.getRange('B9').values=[[null]];w.recalculate();if(calc.getRange('F10').values[0][0]!=='Invalid input')throw new Error('Blank not rejected');
calc.getRange('B7').values=[[1000]];calc.getRange('B9').values=[[1]];w.recalculate();
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},summary:'Formula error scan'})).ndjson);
for(const [s,r] of [['Calculator','A1:G20'],['India','A1:G14'],['Sources','A1:D11']]){const image=await w.render({sheetName:s,range:r,scale:1.2,format:'png'});await fs.writeFile(`${previewDir}/${s}.png`,new Uint8Array(await image.arrayBuffer()));}
const out=await SpreadsheetFile.exportXlsx(w);await out.save(root+'/excel/ThirstyAI_Audit.xlsx');console.log('Workbook exported. Calculation/input-change/missing-input checks passed.');
