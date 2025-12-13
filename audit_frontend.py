import os
import re
import glob

FRONTEND_DIR = "/home/xyz/Documents/xxx/frontend"

def get_vue_files():
    files = []
    for root, _, filenames in os.walk(FRONTEND_DIR):
        for filename in filenames:
            if filename.endswith(".vue"):
                files.append(os.path.join(root, filename))
    return files

def check_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    errors = []
    
    # Extract script content
    script_match = re.search(r'<script.*?>(.*?)</script>', content, re.DOTALL)
    script_content = script_match.group(1) if script_match else ""

    # 1. Check @click handlers
    # Find all @click="handler" or @click="handler(...)"
    # Simplification: match word chars before ( or "
    click_handlers = re.findall(r'@click\.?[\w\.]*="([^"(]+)', content)
    
    for handler in click_handlers:
        handler = handler.strip()
        # unintentional matches like "showQuickView = false" -> ignore assignment
        if '=' in handler or '!' in handler or '$' in handler or "'" in handler:
            continue
            
        # If it's a simple function name, check if it exists in script
        if not re.search(r'(const|function|let|var)\s+' + re.escape(handler), script_content) and \
           not re.search(r'import\s+.*' + re.escape(handler), script_content) and \
           not "defineProps" in script_content: # Props might handle it, hard to trace statically
             # Check if it's imported from a composable? Hard to track. 
             # Let's flag it as POTENTIAL warning if not found.
             pass 
             # Actually, static analysis of dynamic JS is hard. 
             # Let's focus on "broken links" and "empty handlers".

    # 2. Check NuxtLink/RouterLink
    links = re.findall(r'<NuxtLink.*?to="([^"]+)"', content)
    for link in links:
        if link.startswith("http") or link.startswith("#"): continue
        # Check if route exists in pages
        # This is a heuristic. /product/123 -> pages/product/[id].vue
        target = link.split('?')[0] # remove query params
        
        # Verify if mapping exists
        if not verify_route(target):
            errors.append(f"Broken Link? '{link}' -> No matching page found.")

    return errors

def verify_route(path):
    # Normalize path
    parts = [p for p in path.split('/') if p]
    
    # Root
    if not parts:
        return os.path.exists(os.path.join(FRONTEND_DIR, "pages", "index.vue"))

    # Construct path in pages dir
    # 1. Exact match
    exact = os.path.join(FRONTEND_DIR, "pages", *parts) + ".vue"
    if os.path.exists(exact): return True
    
    # 2. Directory index
    index = os.path.join(FRONTEND_DIR, "pages", *parts, "index.vue")
    if os.path.exists(index): return True
    
    # 3. Dynamic routes (simplified)
    # If path is /product/123, look for pages/product/[id].vue or pages/product/[...slug].vue
    # This is complex to implement fully specifically, but we can do a basic check
    # Check if parent dir exists
    if len(parts) > 0:
        parent = os.path.join(FRONTEND_DIR, "pages", *parts[:-1])
        if os.path.exists(parent):
            # Check for dynamic file in parent
            for f in os.listdir(parent):
                if f.startswith('[') and f.endswith('.vue'):
                    return True
    
    return False

def audit():
    print("🔍 Starting Frontend Audit...")
    files = get_vue_files()
    all_errors = []
    
    for f in files:
        rel_path = os.path.relpath(f, FRONTEND_DIR)
        errs = check_file(f)
        if errs:
            print(f"❌ {rel_path}:")
            for e in errs:
                print(f"  - {e}")
                all_errors.append((rel_path, e))
        else:
            # print(f"✅ {rel_path}")
            pass

    if not all_errors:
        print("\n✅ No obvious broken links found.")
    else:
        print(f"\nFound {len(all_errors)} potential issues.")

if __name__ == "__main__":
    audit()
