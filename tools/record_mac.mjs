// Record the live local SQL console. The browser runs the SQL on the lab server.
import {createRequire} from 'node:module';
import {mkdirSync,readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const target=resolve('output/videos');mkdirSync(target,{recursive:true});
mkdirSync('tmp/video-qa',{recursive:true});
const queries=process.argv.slice(2).length?process.argv.slice(2):['Q1','Q2','Q3','Q4','Q5','Q6'];
const browser=await chromium.launch({headless:true,executablePath:process.env.TECHPULSE_CHROME||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const logPath=resolve('outputs/recordings.json');
let manifest;try{manifest=JSON.parse(readFileSync(logPath,'utf8'))}catch{manifest={}}
async function scan(page,seconds,maxSteps=5){
  const height=await page.evaluate(()=>Math.max(0,document.documentElement.scrollHeight-innerHeight));
  if(height<15){await page.waitForTimeout(seconds*1000);return}
  const steps=Math.min(maxSteps,Math.ceil(height/650));
  for(let i=0;i<=steps;i++){
    await page.evaluate(y=>window.scrollTo(0,y),Math.round(height*i/steps));
    await page.waitForTimeout(seconds*1000/(steps+1));
  }
}
try{
for(const q of queries){
  console.log('Recording',q);
  const context=await browser.newContext({viewport:{width:1920,height:1080},recordVideo:{dir:'tmp/raw-videos',size:{width:1920,height:1080}}});
  const page=await context.newPage();
  await page.goto('http://127.0.0.1:8765/?query='+q);
  await page.waitForFunction(()=>window.ready);
  await page.screenshot({path:`tmp/video-qa/${q}-sql-top.png`});
  await scan(page,q==='Q5'?9:6);
  await page.screenshot({path:`tmp/video-qa/${q}-sql-bottom.png`});
  await page.click('#run');
  await page.waitForFunction(()=>window.complete||window.failed,{},{timeout:15000});
  if(await page.evaluate(()=>!!window.failed))throw new Error(q+' failed: '+await page.locator('#message').textContent());
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.waitForTimeout(200);
  const evidence=await page.evaluate(()=>window.execution);
  await page.screenshot({path:`tmp/video-qa/${q}-results-top.png`});
  await scan(page,q==='Q5'?7:8,6);
  await page.screenshot({path:`tmp/video-qa/${q}-results-bottom.png`});
  if(q==='Q5'){
    await page.click('#messagetab');
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.waitForTimeout(200);
    await page.screenshot({path:'tmp/video-qa/Q5-messages.png'});
    await page.waitForTimeout(5000);
  }else{await page.waitForTimeout(1800)}
  const video=page.video();await context.close();
  const raw=await video.path();
  const file=resolve(target,`Lab5_TEL3_Team3_${q}.mp4`);
  execFileSync('ffmpeg',['-y','-loglevel','error','-i',raw,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','25','-movflags','+faststart',file],{stdio:'pipe'});
  const duration=Number(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',file],{encoding:'utf8'}).trim());
  if(duration>30)throw new Error(q+' is over 30 seconds ('+duration+'); re-record');
  manifest[q]={filename:file,duration_seconds:duration,execution:evidence};
  writeFileSync(logPath,JSON.stringify(manifest,null,2));
  console.log(q,'saved',duration,'seconds');
}
}finally{await browser.close()}
