import sys, os, time
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
frames = [int(x) for x in sys.argv[2].split(',')] if ',' in sys.argv[2] else list(range(int(sys.argv[2]), int(sys.argv[3])))
os.makedirs(out, exist_ok=True)
args = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
with sync_playwright() as p:
    exe = os.environ.get('CHROME_PATH')  # optional: custom Chromium binary
    br = p.chromium.launch(executable_path=exe, args=args) if exe else p.chromium.launch(args=args)
    pg = br.new_page(viewport={'width': 1280, 'height': 720}, device_scale_factor=1)
    msgs = []
    pg.on('console', lambda m: msgs.append(m.text))
    pg.on('pageerror', lambda e: msgs.append('ERR ' + str(e)))
    pg.goto('file://' + os.path.join(here, '..', 'src', 'index.html'))
    try:
        pg.wait_for_function('window.ready===true', timeout=30000)
    except Exception as e:
        print('\n'.join(msgs)); raise
    t0 = time.time()
    for i in frames:
        pg.evaluate(f'renderAt({i/30})')
        pg.screenshot(path=f'{out}/f{i:04d}.jpg', type='jpeg', quality=94, clip={'x': 0, 'y': 0, 'width': 1280, 'height': 720})
    print(f'{len(frames)} frames in {time.time()-t0:.1f}s', '\n'.join(msgs))
    br.close()
