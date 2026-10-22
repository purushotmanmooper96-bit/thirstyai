import test from 'node:test';
import assert from 'node:assert/strict';
import {bindSkipLink} from '../dist/navigation.mjs';
test('skip link focuses the current page without allowing its hash navigation',()=>{
 const link=new EventTarget();
 const route={hash:'#companies',heading:'Same word. Different water accounts.'};
 let focused=false;
 const main={focus(){focused=true;}};
 bindSkipLink(link,main);
 const event=new Event('click',{cancelable:true});
 // In the browser, an uncancelled click would follow href="#main" and change route.
 if(link.dispatchEvent(event)){route.hash='#main';route.heading='Overview';}
 assert.equal(focused,true);
 assert.equal(event.defaultPrevented,true);
 assert.equal(route.hash,'#companies');
 assert.equal(route.heading,'Same word. Different water accounts.');
});
