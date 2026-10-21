"""Real browser validation of 8-bit inference and all three preparation viewers."""
import hashlib
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/precision_upgrade8'
OUT.mkdir(parents=True,exist_ok=True)


def viewer(page,base,encoding,qubits):
    page.goto(base+'/state_preparation.html')
    page.wait_for_function("document.getElementById('title').textContent.includes('expanded')",timeout=60000)
    assert encoding in page.locator('#title').inner_text()
    assert page.locator('#width').inner_text().startswith(str(qubits)+' qubits:')
    data=page.request.get(base+'/state_preparation.json').json()
    assert data['qubits']==qubits and data['encoding']==encoding
    assert data['instruction_count']==len(data['gates'])
    assert len(data['roles'])==qubits
    assert set(g[0] for g in data['gates'])<=set(['u','cx','reset'])
    assert page.locator('#circuit .gate').count()==20
    page.locator('#next').click()
    assert page.locator('#page').input_value()=='2'
    assert page.locator('#circuit .gate').first.get_attribute('data-index')=='20'
    last=(len(data['gates'])+19)//20
    page.locator('#page').fill(str(last));page.locator('#pages').click()
    page.locator(f"[data-index='{len(data['gates'])-1}']").click()
    assert 'Instruction '+str(len(data['gates'])) in page.locator('#inspection').inner_text()
    page.locator('#page').fill('1');page.locator('#pages').click()
    first_u=next(i for i,g in enumerate(data['gates'][:20]) if g[0]=='u')
    page.locator(f"[data-index='{first_u}']").click()
    assert 'θ =' in page.locator('#inspection').inner_text()
    qasm=page.request.get(base+'/state_preparation.qasm')
    assert qasm.status==200 and qasm.text().startswith('OPENQASM 3.0;')
    assert hashlib.sha256(qasm.body()).hexdigest()==data['qasm_sha256']
    assert hashlib.sha256(page.request.get(base+'/input.png').body()).hexdigest()==data['input_png_sha256']
    page.screenshot(path=str(OUT/(encoding.lower()+'_preparation.png')),full_page=True)
    page.set_viewport_size({'width':360,'height':900})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.screenshot(path=str(OUT/(encoding.lower()+'_preparation_mobile.png')),full_page=True)
    page.set_viewport_size({'width':1280,'height':1000})
    return {'encoding':encoding,'qubits':qubits,'brightness_qubits':data['brightness_qubits'],
            'instructions':len(data['gates']),'paging_angles_download_and_input_hash':'passed'}


parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--neqr-only',action='store_true',help='Check only the NEQR app on port 8769')
args=parser.parse_args()
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1280,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    cases=[('NEQR',8769,16)] if args.neqr_only else [('QPIE',8766,8),('FRQI',8768,9),('NEQR',8769,16)]
    viewers=[viewer(page,f'http://127.0.0.1:{port}',name,qubits) for name,port,qubits in cases]
    print('Preparation viewers passed',flush=True)
    base='http://127.0.0.1:8769'
    page.goto(base+'/')
    page.wait_for_function("!document.getElementById('upload-run').disabled")
    assert '16 qubits per circuit' in page.locator('#qubit-count').inner_text()
    fixture=OUT/'fixture16.png';Image.fromarray(np.arange(256,dtype=np.uint8).reshape(16,16)).save(fixture)
    page.locator('#upload').set_input_files(str(fixture));page.locator('#upload-run').click()
    page.wait_for_function("document.getElementById('status').textContent==='Complete'",timeout=180000)
    page.wait_for_function("document.querySelectorAll('#comparison-stats tr').length===4",timeout=30000)
    status=page.request.get(base+'/api/status').json()
    metadata=page.request.get(base+'/run_metadata.json').json()
    trace=page.request.get(base+'/api/trace').json()
    assert status['encoding']=='NEQR' and status['intensity_bits']==8 and status['qubits_per_circuit']==16
    assert status['circuits_executed']==16 and status['measurement_shots']==131072
    assert all(c['qubits']==16 and c['metadata']['intensity_qubits']==8 for c in trace['circuits'])
    assert all(c['shots']==8192 and sum(c['counts'].values())==8192 for c in trace['circuits'])
    page.wait_for_function("document.querySelector('[data-trace=diagram]').getAttribute('data-circuit-name') !== null",timeout=30000)
    assert '8-bit brightness' in page.locator('#qubit-count').inner_text()
    assert page.locator('[data-trace=state] rect').count()<2048
    page.screenshot(path=str(OUT/'neqr8_live.png'),full_page=True)
    page.set_viewport_size({'width':360,'height':1000})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.screenshot(path=str(OUT/'neqr8_live_mobile.png'),full_page=True)
    page.set_viewport_size({'width':1280,'height':1000})
    uploaded=viewer(page,base,'NEQR',16)
    assert not page.request.get(base+'/state_preparation.json').json()['example_only']
    assert not errors,errors
    browser.close()
    result={'status':'passed','viewers':viewers,'uploaded_preparation':uploaded,
            'image_shape':[16,16],'brightness_bits':8,'qubits':16,'circuits':16,'shots':131072,
            'trace_circuits_checked':len(trace['circuits']),'browser_errors':errors,
            'mobile_layouts':'all passed','sparse_state_grid':'passed','actual_measured_upload':True}
    (OUT/'browser_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2),flush=True)
