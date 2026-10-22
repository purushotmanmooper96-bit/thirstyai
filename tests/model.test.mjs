import test from 'node:test';import assert from 'node:assert/strict';import {calculate,compare,breakEvenGrid,project,DEFAULTS as b,ALTERNATIVE as a} from '../dist/model.mjs';
test('accounting dimensions',()=>{const r=calculate(b);assert.equal(r.total_l,2200000);assert.equal(r.facility_mwh,1200);});
test('semantic guards',()=>{for(const x of [{water_metric:'withdrawal'},{wue_denominator:'facility_kWh'},{includes_indirect:true},{pue:.9},{wue:null},{wue:NaN},{wue:Infinity},{wue:-1}])assert.throws(()=>calculate({...b,...x}));});
test('tradeoff and break-even',()=>{assert.equal(compare(b,a).water_saved_l,700000);assert.ok(Math.abs(breakEvenGrid(b,a)-4.5)<1e-9);assert.ok(compare({...b,grid_l_kwh:5},{...a,grid_l_kwh:5}).water_saved_l<0);});
test('zero baseline and equal workload',()=>{assert.equal(compare({...b,wue:0,grid_l_kwh:0},{...a,wue:0,grid_l_kwh:0}).water_saved_pct,null);assert.throws(()=>compare(b,{...a,it_mwh:4}));});
test('conditional futures',()=>{assert.ok(Math.abs(project(b,.1,0,2026).total_l-2420000)<1e-6);assert.throws(()=>project(b,.1,.1,2024));});
